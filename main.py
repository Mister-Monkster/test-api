import uvicorn
from fastapi import FastAPI
from src.app.api.routers.router import router as api

app = FastAPI()

app.include_router(api)

if __name__ == "__main__":
    uvicorn.run(app)
