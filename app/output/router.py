import inject
from fastapi import APIRouter, Depends

from app.core.repositories.cache_firestore_repo_impl import CacheQueriesRepo
from app.logic.query_generator_ai.index import QueryGeneratorAIUC


order_assigner_router = APIRouter()


@order_assigner_router.post("")
async def get_data(query: dict):
    question = query.get("question")
    uc = inject.instance(QueryGeneratorAIUC)
    response = await uc.execute(question)
    return response


@order_assigner_router.post("/mark_as_good")
async def get_data(query: dict):
    hash = query.get("hash")
    cache_queries_repo = inject.instance(CacheQueriesRepo)
    response = await cache_queries_repo.set_is_valid(hash)
    return response

