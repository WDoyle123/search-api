from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from app.db import SessionLocal, engine
from app.models import Base, Events, Hotels
from app.routes import search


Base.metadata.create_all(bind=engine)


def seed_initial_data() -> None:
    session = SessionLocal()

    try:
        session.merge(
            Events(
                eventID=1,
                latitude=51.5007,
                longitude=-0.1246,
            )
        )

        hotels = [
            Hotels(hotelID=101, latitude=51.5033, longitude=-0.1195),
            Hotels(hotelID=102, latitude=51.5094, longitude=-0.1183),
            Hotels(hotelID=103, latitude=51.4952, longitude=-0.1469),
            Hotels(hotelID=104, latitude=51.5155, longitude=-0.0720),
            Hotels(hotelID=105, latitude=51.4700, longitude=-0.4543),
        ]

        for hotel in hotels:
            session.merge(hotel)

        session.commit()
    finally:
        session.close()


seed_initial_data()

app = FastAPI(
    title="Search API",
    docs_url="/v1/docs",
    redoc_url="/v1/redoc",
    openapi_url="/v1/openapi.json",
    description=(
        "**GitHub Repository:** [WDoyle123/search-api](https://github.com/WDoyle123/search-api)"
    ),
)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_400(request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={"detail": exc.errors()})

api_router = APIRouter(prefix="/v1")
api_router.include_router(search.router)

app.include_router(api_router)
