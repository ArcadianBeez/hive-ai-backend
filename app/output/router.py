import inject
from fastapi import APIRouter, Depends
from app.logic.query_generator_ai.index import QueryGeneratorAIUC
from security.key_validator import validate_apikey_request

order_assigner_router = APIRouter()


@order_assigner_router.post("")
async def get_data(query: dict, _=Depends(validate_apikey_request)):
    instruction = query.get("instruction")

    uc = inject.instance(QueryGeneratorAIUC)
    response = await uc.execute(instruction)
    return response
