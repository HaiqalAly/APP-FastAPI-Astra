from fastapi import FastAPI
from app.db.connection import init_db
from contextlib import asynccontextmanager

# Lifespan events to initialize the database connection
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    await init_db()
    yield

    print("Shutting down...")

app = FastAPI(
    lifespan=lifespan
)

@app.get("/")
def root():
    return {"message": "Hello, World!"}