import inject
from loguru import logger
from pydantic import ValidationError

# Inject Configured Dependencies
from app.output import app_router
from app.config import di_configuration

inject.configure(di_configuration)

from fastapi import FastAPI
from starlette.middleware.gzip import GZipMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.responses import Response, JSONResponse, PlainTextResponse
from starlette.requests import Request

app = FastAPI(title="API Sources - Python", version="0.0.1")
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.include_router(app_router, prefix="/api/v1")

ALLOWED_ORIGINS = '*'  # or 'foo.com', etc.

logger.info("Hello World!")


# handle CORS preflight requests
@app.options('/{rest_of_path:path}', include_in_schema=False)
async def preflight_handler(request: Request, rest_of_path: str) -> Response:
    response = Response()
    response.headers['Access-Control-Allow-Origin'] = ALLOWED_ORIGINS
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type, Api-Key'
    return response


# set CORS headers
@app.middleware("http")
async def add_CORS_header(request: Request, call_next):
    response = await call_next(request)
    response.headers['Access-Control-Allow-Origin'] = ALLOWED_ORIGINS
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type , Api-Key'
    return response


@app.exception_handler(500)
async def add_CORS_header_500(request: Request, call_next):
    response = JSONResponse(content={"detail": "something went wrong :("}, status_code=500)
    response.headers['Access-Control-Allow-Origin'] = ALLOWED_ORIGINS
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type , Api-Key'
    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=500)


@app.on_event("startup")
# Code to be run when the server starts.
async def startup_event():
    pass


@app.get("/ping")
async def ping():
    return JSONResponse({"message": "pong"})


@app.get("/")
async def home():
    return JSONResponse("Hello World")
