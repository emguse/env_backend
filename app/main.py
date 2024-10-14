import json

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
import uvicorn

from models import ReceiveEnv
from config import BaseConfig
from cruds import insert_env_data
from db import create_tables

config = BaseConfig()


app = FastAPI(title=config.PROJECT_NAME)


class RemoveDuplicateHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        headers = request.headers.mutablecopy()
        if headers.getlist("content-type"):
            content_type = headers.getlist("content-type")[0]
            headers["content-type"] = content_type

        request._headers = headers

        response = await call_next(request)
        return response


app.add_middleware(RemoveDuplicateHeadersMiddleware)


@app.get("/")
async def root():
    return {"message": "Hello. World!"}


@app.get("/hello")
async def hello():
    return {"message": "Hello. World!"}


@app.post("/post-env4")
async def post_test(env_data: ReceiveEnv):
    print(env_data)
    insert_env_data(env_data.timestamp, env_data.sensor_id, "temperature", env_data.temperature)
    insert_env_data(env_data.timestamp, env_data.sensor_id, "humidity", env_data.humidity)
    insert_env_data(env_data.timestamp, env_data.sensor_id, "pressure", env_data.pressure)
    return {"env_data": env_data}


@app.post("/post-test")
async def post_test(request: Request):
    header = request.headers
    body = await request.body()
    body_json = json.loads(body)
    print(header)
    print(body_json)
    return {"body": body_json}


if __name__ == "__main__":
    create_tables()
    uvicorn.run(app, host="0.0.0.0", port=8000)
