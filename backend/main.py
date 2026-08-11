from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.routers import user
from app.routers import bangumi

from app.models.anime import AnimeCollection

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],  # Vue开发服务器
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    user.router,
    prefix="/user",
    tags=["User"]
)

app.include_router(
    bangumi.router,
    prefix="/bangumi",
    tags=["bangumi"]
)
