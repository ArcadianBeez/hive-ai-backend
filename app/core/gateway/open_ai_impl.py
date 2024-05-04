import abc

from openai import OpenAI


class OpenAIGateway(abc.ABC):
    @abc.abstractmethod
    def get_response_for_question(self, prompt: str, context: str) -> str:
        pass


class OpenAIGatewayImpl(OpenAIGateway):
    def __init__(self, api_token: str):
        self.api_token = api_token

    def get_response_for_question(self, prompt: str, context: str) -> str:
        client = OpenAI(api_key=self.api_token)
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
