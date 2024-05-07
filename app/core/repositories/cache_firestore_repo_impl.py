import abc
import hashlib
from typing import Optional

from google.cloud import firestore
from pydantic import BaseModel


class CacheItem(BaseModel):
    hash: str
    query: str
    question: str
    is_valid: bool


class CacheQueriesRepo(abc.ABC):
    @abc.abstractmethod
    async def get_by_question(self, question: str) -> CacheItem:
        pass

    @abc.abstractmethod
    async def save(self, question: str, query: str) -> str:
        pass

    @abc.abstractmethod
    async def set_is_valid(self, hash: str):
        pass


class CacheFirestoreRepoImpl(CacheQueriesRepo):
    collection = "queries_cache_repo"
    log_bind = {"repository": "queries_cache_repo"}

    def __init__(self, firestore_client: firestore.AsyncClient):
        self.client: firestore.AsyncClient = firestore_client
        self.collection = firestore_client.collection(self.collection)

    async def get_by_question(self, question: str) -> CacheItem:
        hash_doc = self.generate_hash(question)
        query = (self.collection
                 .where('is_valid', '==', True)
                 .where('hash', '==', hash_doc))
        result_query = query.stream()

        docs = [CacheItem(**doc.to_dict()) async for doc in result_query]
        if len(docs) > 0:
            return docs[0]

        return None

    async def save(self, question: str, query: str) -> str:
        hash_doc = self.generate_hash(question)
        cache_item = CacheItem(hash=hash_doc, query=query, question=question, is_valid=False)
        await self.collection.document(hash_doc).set(cache_item.dict())
        return hash_doc

    async def set_is_valid(self, hash: str):
        doc_ref = self.collection.document(hash)
        await doc_ref.update({
            'is_valid': True
        })
        return hash

    @staticmethod
    def generate_hash(input_string):
        sha_signature = hashlib.sha256()
        sha_signature.update(input_string.encode())
        return sha_signature.hexdigest()
