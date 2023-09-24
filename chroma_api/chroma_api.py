from fastapi import FastAPI
from kdh_repository import *

api = FastAPI()
init_db()


@api.get('/search')
def search_by_request(query: str, size: int):
    return {"result": search(query, size)}
