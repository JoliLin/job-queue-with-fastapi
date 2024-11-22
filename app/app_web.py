import pathlib
import sys

cur = pathlib.Path(__file__).resolve().parent

import os
import uvicorn

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

load_dotenv(dotenv_path=".env")
load_dotenv()

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/", StaticFiles(directory="{}/html".format(cur.parent), html=True), name="ui")

@app.get("/")
async def main():
    return FileResponse("{}/html/index.html".format(cur))


if __name__ == '__main__':
    uvicorn.run(
        'app_web:app',
        host='0.0.0.0',
        port=int(os.environ['WEB_PORT']),
        reload=True,
    )
