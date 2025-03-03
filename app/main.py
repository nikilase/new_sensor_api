import secrets

from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.api.router import router as api_router
from app.conf.config import allowed_hosts
from app.openweather.models.sqlite import init_db
from app.openweather.router import router as ow_router
from app.website.router import router as website_router

app = FastAPI(
    title="API for former Sensorwebsite",
    description="Ability to send well structured sensor data from luftdaten.info sensor node to my influx database. "
    "Only BME280 and DS18B20 sensor values currently supported. "
    "This is a private API/Mini Website made by Niklas Eichenberg",
    contact={
        "name": "nikilase",
        "url": "https://github.com/nikilase",
    },
    version="1.0.0",
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        nonce = secrets.token_hex(16)
        request.state.nonce = nonce
        response: Response = await call_next(request)
        csp = (
            "default-src 'self'; "
            f"script-src 'self' 'nonce-{nonce}' https://ajax.googleapis.com https://cdn.jsdelivr.net; "
            f"style-src 'self' 'nonce-{nonce}' https://cdn.jsdelivr.net; "
            "font-src https://cdn.jsdelivr.net; "
            "img-src 'self' data:; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "form-action 'self'; "
            "frame-ancestors 'self'; "
            "connect-src 'self'; "
            "media-src 'self'; "
            "frame-src 'self'; "
            "worker-src 'self'; "
            "manifest-src 'self';"
        )
        response.headers["Content-Security-Policy"] = csp.encode(
            "ascii", "ignore"
        ).decode("ascii")
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=()"
        return response


app.add_middleware(SecurityHeadersMiddleware)

# ToDo: TEST AND COMPLETE THIS REFACTOR

# ToDo: Add correct return codes in routers, especially when errored
# ToDo: Move from Tmux to Systemd


@app.on_event("startup")
async def startup_event():
    init_db()


app.include_router(website_router, tags=["website"])
app.include_router(api_router, tags=["apiv1"])
app.include_router(ow_router, tags=["openweather"])
