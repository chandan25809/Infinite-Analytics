from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from projects.auth_app import auth
from projects.binance_app import binance
from projects.weather_app import weather
import secrets

app = FastAPI()
secret_key = secrets.token_urlsafe(32)

app.add_middleware(
    SessionMiddleware,
    secret_key=secret_key
)

app.mount("/static", StaticFiles(directory="./projects/auth_app/static"), name="static")

@app.get("/health")
def healthcheck():
    return {"status": "ok"}

app.include_router(prefix = "/auth_app", router=auth.router)
app.include_router(prefix = "/binance", router=binance.app)
app.include_router(prefix="/weather",router=weather.router)