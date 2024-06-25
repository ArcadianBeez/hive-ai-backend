import abc
import datetime
import json
import re

import inject

from app.core.gateway.open_ai_impl import OpenAIGateway
from app.core.repositories.cache_firestore_repo_impl import CacheQueriesRepo
from app.core.repositories.models.all_tables_repo import HiveQueriesRepo


class QueryGeneratorAIUC(abc.ABC):
    @abc.abstractmethod
    def execute(self, query: str):
        pass


class QueryGeneratorAIUCImpl(QueryGeneratorAIUC):
    hive_queries_repo: HiveQueriesRepo = inject.attr(HiveQueriesRepo)
    openai_gateway: OpenAIGateway = inject.attr(OpenAIGateway)
    cache_repo: CacheQueriesRepo = inject.attr(CacheQueriesRepo)

    async def execute(self, question: str):
        find_cache = await self.cache_repo.get_by_question(question)

        if find_cache:
            data_response = await self.hive_queries_repo.fetch_by_query(find_cache.query)
            return {
                "hash": find_cache.hash,
                "data_result": [response.dict() for response in data_response]
            }
        context = self.read_file("app/logic/query_generator_ai/orders_context.md")
        considerations = self.read_file("app/logic/query_generator_ai/orders_considerations.md")

        context_str = f"my tables is this: {context} and you should consider the following: {considerations}"
        current_year = datetime.datetime.now().year
        considerations_str = self.build_query_considerations(current_year)

        prompt = f"Generate a query based on the following question: {question}\nand you should consider the following points: {considerations_str}"
        generated_query = self.generate_query(prompt, context_str)

        cleaned_json = self.clean_and_parse_json(generated_query)
        if cleaned_json is None:
            return "Invalid query generated, please try again."


        if not self.is_valid_query(cleaned_json['query']):
            return "Invalid query generated, please try again."

        data_response = await self.hive_queries_repo.fetch_by_query(cleaned_json['query'])
        actions = self.get_actions_by_entity(cleaned_json['mainEntity'])
        saved_hash = await self.cache_repo.save(question, cleaned_json['query'])
        return {
            "hash": saved_hash,
            "data_result": [response.dict() for response in data_response],
            "actions": actions,
        }

    def get_actions_by_entity(self, entity):
        actions = self.read_file("app/logic/query_generator_ai/actions.json")
        actions_json = self.clean_and_parse_json(actions)
        actions = actions_json.get(entity, [])
        return actions

    def clean_and_parse_json(self, text):

        # Eliminar espacios en blanco y tabulaciones
        cleaned_text = re.sub(r'\s*([{:,}\[\]])\s*', r'\1', text)

        try:
            # Intentar analizar el texto como JSON
            json_data = json.loads(cleaned_text)
            return json_data
        except json.JSONDecodeError as e:
            print(f"Error al analizar JSON: {e}")
            return None

    def read_file(self, file_path):
        with open(file_path) as file:
            return file.read()

    def build_query_considerations(self, current_year):
        current_date = datetime.datetime.now().date()
        return (
                "-ever include id of the main table in the select clause, "
                "ever include name of restaurant or driver when query ask for delivery or store"
                "-ever return the SQL query only as answer, "
                "-ever use LIMIT 20, "
                "-when query includes a name ever use LIKE %%, "
                "-ever use the column name in the select clause, "
                "-ever put the table name in select and where clause, "
                "-ever convert the dates output to string, "
                "-ever not include names or id when query require a sum of all"
                "-created_at and updated_at could be ambiguous, so use the table name before the column name, "
                f"when query does not specify the year of the date, use {current_year} as default year."
                "ever put name accord query of the columns in the select clause with spaces as normal label, "
                "when query said some of number or numero, use count() function, "
                "when query said some ranking use sum() function, "
                "when query indicates a date today use:" + str(current_date)

        )

    def generate_query(self, prompt, context_str):
        response = self.openai_gateway.get_response_for_question(prompt=prompt, context=context_str)
        return response.replace("```sql", "").replace("```", "")

    def build_response_html(self, template, data_response):
        response_data = [response.dict() for response in data_response]
        return template.replace("[]", json.dumps(response_data, default=self.default_converter))

    def save_html(self, html_content):
        with open("data_generated.html", "w") as file:
            file.write(html_content)

    def default_converter(self, o):
        if isinstance(o, datetime.date):
            return o.isoformat()

    def is_valid_query(self, query):
        return "UPDATE" not in query and "DELETE" not in query and "DROP" not in query
