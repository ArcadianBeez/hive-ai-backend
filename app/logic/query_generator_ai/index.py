import abc
import datetime
import json

import inject

from app.core.gateway.open_ai_impl import OpenAIGateway
from app.core.repositories.models.all_tables_repo import HiveQueriesRepo


class QueryGeneratorAIUC(abc.ABC):
    @abc.abstractmethod
    def execute(self, query: str):
        pass


class QueryGeneratorAIUCImpl(QueryGeneratorAIUC):
    hive_queries_repo: HiveQueriesRepo = inject.attr(HiveQueriesRepo)
    openai_gateway: OpenAIGateway = inject.attr(OpenAIGateway)

    async def execute(self, query: str):
        context = self.read_file("app/logic/query_generator_ai/orders_context.md")
        considerations = self.read_file("app/logic/query_generator_ai/orders_considerations.md")
        data_tables_template = self.read_file("app/logic/query_generator_ai/templates/data_tables.html")

        context_str = f"my tables is this: {context} and you should consider the following: {considerations}"
        current_year = datetime.datetime.now().year
        considerations_str = self.build_query_considerations(current_year)

        prompt = f"Generate a query based on the following question: {query}\nand you should consider the following points: {considerations_str}"
        generated_query = self.generate_query(prompt, context_str)

        print(generated_query)

        if not self.is_valid_query(generated_query):
            return "Invalid query generated, please try again."

        data_response = await self.hive_queries_repo.fetch_by_query(generated_query)
        response_html = self.build_response_html(data_tables_template, data_response)
        self.save_html(response_html)
        return response_html

    def read_file(self, file_path):
        with open(file_path) as file:
            return file.read()

    def build_query_considerations(self, current_year):
        return (
            "-ever return the SQL query only as answer, "
            "-ever use LIMIT 20, "
            "-when query includes a name ever use LIKE %%, "
            "-ever use the column name in the select clause, "
            "-ever put the table name in select and where clause, "
            "-ever convert the dates output to string, "
            "-created_at and updated_at could be ambiguous, so use the table name before the column name, "
            f"when query does not specify the year of the date, use {current_year} as default year."
            "ever put name accord query of the columns in the select clause with spaces as normal label, "
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
