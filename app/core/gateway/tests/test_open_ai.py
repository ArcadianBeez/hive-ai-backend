import pytest
from decouple import config
from app.core.gateway.open_ai_impl import OpenAIGatewayImpl


@pytest.mark.skipif(config("LIVE_TESTS", cast=bool, default=False) is False, reason="Live tests are disabled")
@pytest.mark.asyncio
async def test_get_response_for_question():
    openai_gateway = OpenAIGatewayImpl(api_key=config("OPENAI_API_KEY"))
    context = "You are a helpful calculator assistant."
    prompt = "What is the sum of 2, 3, and 4?"
    response = openai_gateway.get_response_for_question(prompt, context)
    print(response)
    assert response is not None  # Or other appropriate assertions
