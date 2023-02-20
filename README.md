# new_sensor_api

This is a small API for receiving sensor data from https://sensor.community/ (formerly https://luftdaten.info/) sensor nodes and saving it in an Influx (version 1) Time Series Database.
Also includes a little html based website for showing the current data of one sensor.

To start the app, just run `python3.11 server.py`. Only tested with python 3.11 but _should_ also work with python 3.10 or above.
Needs python 3.10 at minimum due to usage of `match case` functionality. 