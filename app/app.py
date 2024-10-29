import pathlib
import sys

cur = pathlib.Path(__file__).resolve().parent
sys.path.append('{}/'.format(cur.parent))
sys.path.append('{}/app'.format(cur.parent))

import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app_async import router as router_async

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_async)


def main():
    uvicorn.run(
        'app:app',
        host='0.0.0.0',
        port=5566,
        reload=True,
    )

#if __name__ == '__main__':
#    main()
