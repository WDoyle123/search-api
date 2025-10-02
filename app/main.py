from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.db import engine
from app.models import Base


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Search API",
    docs_url="/v1/docs",
    redoc_url="/v1/redoc",
    openapi_url="/v1/openapi.json",
)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix="/v1")

@api_router.get("/", response_class=HTMLResponse)
async def read_root():
    return HTMLResponse(content="<h1>Search API</h1>", status_code=200)

app.include_router(api_router)


