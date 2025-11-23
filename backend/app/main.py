from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.settings import settings
from app.database import create_db_and_tables

app = FastAPI(title="Aerostats API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api import auth, public, admin

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(public.router, tags=["public"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])

from app.seed import seed

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    seed()

@app.get("/")
def read_root():
    return {"message": "Aerostats API is running"}
