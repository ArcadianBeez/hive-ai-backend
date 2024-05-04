import abc


class QueryGeneratorAIUC(abc.ABC):
    @abc.abstractmethod
    def generate_query(self, query: str):
        pass


class QueryGeneratorAIUCImpl(QueryGeneratorAIUC):
    def generate_query(self, query: str):
        return query
