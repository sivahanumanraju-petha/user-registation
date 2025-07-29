from fastapi import FastAPI
from auth.user_routes import router as user_router
from utils.logger import init_logger

app = FastAPI(title= "user_registation")
init_logger()
app.include_router(user_router, prefix="/auth")