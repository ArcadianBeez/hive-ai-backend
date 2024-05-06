import abc
import json

import inject

from app.core.gateway.open_ai_impl import OpenAIGatewayImpl, OpenAIGateway
from app.core.repositories.models.all_tables_repo import HiveQueriesRepo


class QueryGeneratorAIUC(abc.ABC):
    @abc.abstractmethod
    def execute(self, query: str):
        pass


class QueryGeneratorAIUCImpl(QueryGeneratorAIUC):
    hive_queries_repo: HiveQueriesRepo = inject.attr(HiveQueriesRepo)
    openai_gateway: OpenAIGateway = inject.attr(OpenAIGateway)

    async def execute(self, query: str):
        with open("app/logic/query_generator_ai/orders_context.json") as f:
            context = json.loads(f.read())

        with open("app/logic/query_generator_ai/templates/data_tables.html") as f:
            data_tables_template = f.read()

        context_str = "my table is this: " + context["sql_structure"] + " and the data is this: " + context[
            "description"]

        generated_query_prompt = "Generate a query based on the following question: " + query + " and only return the sql query as answer. use DATE(CONVERT_TZ(CURDATE(), 'UTC', 'America/Guayaquil')) for dates, and ever LIMIT 20"

        generated_query = self.openai_gateway.get_response_for_question(prompt=generated_query_prompt,
                                                                        context=context_str)
        data_response = await self.hive_queries_repo.fetch_by_query(generated_query)
        response_dict=[response.dict() for response in data_response]
        response_html = data_tables_template.replace("[]",json.dumps(response_dict),)
        with open("data_generated.html", "w") as f:
            f.write(response_html)
        return response_html
