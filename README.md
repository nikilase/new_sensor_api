# new_sensor_api

This is a small API for receiving sensor data from https://sensor.community/ (formerly https://luftdaten.info/) sensor nodes and saving it in an Influx (version 1) Time Series Database.<br>
Also includes a little html based website for showing the current data of one sensor.

# Startup
To start the app, just run: <br>
`python3.11 server.py`

Be aware that you should start the program in the root directory of the project.

Only tested with python 3.11 but _should_ also work with python 3.10 or above.<br>
Needs python 3.10 at minimum due to usage of `match case` functionality.

# Python Virtual Environment
### Create a Virtual Environment
To create a Virtual Environment execute <br>
`python3.11 -m venv {venv_directory}` <br>
in the root directory of the project.

Then activate it by using <br>
`source {venv_directory}/bin/activate`

Install requirements in activated Virtual Environment by using <br>
`pip install -r requirements.txt`

Deactivate Virtual Environment with command <br>
`deactivate`

### Run in Virtual Environment

In the root directory of the program activate the Virtual Environment <br>
`source {venv_directory}/bin/activate`

Then just execute like above using <br>
`python3.11 server.py`