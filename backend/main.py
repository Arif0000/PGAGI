from fastapi import FastAPI
from backend.api.routes import router

app = FastAPI(title="AI Interview System")
app.include_router(router)
