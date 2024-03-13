from fastapi import APIRouter, Request

from app.api.calculations import (
    extract_and_send_sensor_data,
    extract_and_send_stat_data,
)
from app.api.models.influx import get_latest_data, write_line
from app.conf.config import influxdb
from app.helpers.my_logger import log_error, log_info

router = APIRouter()


@router.get("/get_latest")
async def get_latest(chip_id: str = "esp11609738") -> dict:
    print("\n")
    x = get_latest_data(chip_id)
    return x


@router.get("/hello/{name}")
async def say_hello(name: str):
    print("\n")
    log_info(f"GET /hello/{name}")
    return {"message": f"Hello {name}"}


# ToDo: Maybe merge /ping and /restart to /post_stat
@router.get("/ping/{chip_type}/{chip_id}")
async def ping(chip_type: str, chip_id: str):
    print("\n")
    log_info(f"GET /ping/{chip_type}/{chip_id}")
    match chip_type:
        case "esp8266id":
            chip_id = f"esp{chip_id}"
        case "sensorId":
            chip_id = f"gen_{chip_id}"

    tags = {"sensorID": chip_id}
    fields = {"ping": 1}
    write_line(tags, fields, "", influxdb)

    return {"message": f"Received Ping"}


@router.get("/restart/{chip_type}/{chip_id}")
async def restart(chip_type: str, chip_id: str):
    print("\n")
    log_info(f"GET /restart/{chip_type}/{chip_id}")
    match chip_type:
        case "esp8266id":
            chip_id = f"esp{chip_id}"
        case "sensorId":
            chip_id = f"gen_{chip_id}"

    tags = {"sensorID": chip_id}
    fields = {"restart": 1}
    write_line(tags, fields, "", influxdb)

    return {"message": f"Received Restart"}


# ToDo: Test function
@router.post("/post_stat")
async def post_stat(req: Request):
    print("\n")
    log_info(f"POST /post_stat")
    try:
        stat_data_json: dict = await req.json()
    except Exception as err:
        body = await req.body()
        log_error("POST /post_stat", f"Error: {err} \n" f"\tInvalid JSON body: {body}")
        return {"message": "Failed to receive Sensor Data JSON Object!"}
    else:
        log_info("POST /post_stat", f"Received Data: \n" f"{stat_data_json}")

        failed: int = extract_and_send_stat_data(stat_data_json)
        if not failed:
            return {
                "message": "Successfully received and sent Sensor Stat to Influx DB!"
            }
        else:
            match failed:
                case 1:
                    return {"message": "Error: No Chip ID was sent!"}
                case 2:
                    return {"message": "Error: No sensor data was sent!"}
                case 3:
                    return {"message": "Could not write the data to Influx DB!"}
                case _:
                    return {
                        "message": "Unknown error occurred. Could not extract data or send to Influx DB!"
                    }


@router.post("/Send")
async def send_sensor_data(req: Request):
    ##################################################
    # Retrieve Request and JSON data
    ##################################################
    print("\n")
    log_info("POST /Send", "Received Request")
    try:
        sensor_data_json: dict = await req.json()
    except Exception as err:
        body = await req.body()
        log_error("POST /Send", f"Error: {err} \n" f"\tInvalid JSON body: {body}")
        return {"message": "Failed to receive Sensor Data JSON Object!"}
    else:
        log_info("POST /Send", f"Received Data: \n" f"{sensor_data_json}")

        failed: int = extract_and_send_sensor_data(sensor_data_json)
        if not failed:
            return {
                "message": "Successfully received and sent Sensor Data to Influx DB!"
            }
        else:
            match failed:
                case 1:
                    return {"message": "Error: No Chip ID was sent!"}
                case 2:
                    return {"message": "Error: No sensor data was sent!"}
                case 3:
                    return {"message": "Could not write the data to Influx DB!"}
                case _:
                    return {
                        "message": "Unknown error occurred. Could not extract data or send to Influx DB!"
                    }
