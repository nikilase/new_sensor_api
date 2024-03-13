from fastapi import FastAPI

from app.api.router import router as api_router
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

# ToDo: TEST AND COMPLETE THIS REFACTOR

# ToDo: Add correct return codes in routers, especially when errored
# ToDo: Move from Tmux to Systemd


@app.on_event("startup")
async def startup_event():
    init_db()


app.include_router(website_router, tags=["website"])
app.include_router(api_router, tags=["apiv1"])
app.include_router(ow_router, tags=["openweather"])
