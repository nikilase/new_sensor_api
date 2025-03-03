from decimal import Decimal

server = {"host": "0.0.0.0", "port": 1234, "reload": False}

allowed_hosts = ["*"]

influxdb = {
    # The address of the InfluxDB
    "host": "0.0.0.0",
    # The port of the InfluxDB
    "port": 8080,
    # The database name
    "db": "database",
    # The measurement
    "msrmt": "measurement",
    # The retention policy
    "ret": "autogen",
    # The username
    "user": "admin",
    # The password of the user
    "pwd": "password",
    # The precision, standard is s
    "prec": "s",
    # The consistency, standard is one
    "cons": "one",
    # Do we use SSL for the database and if so do we verify the cert?
    "ssl": False,
    "verify_ssl": False,
}

openweathermap = {
    "api_key": "<secret_key>",
    "base_url": "https://api.openweathermap.org/data/3.0/onecall",
    "only_allowed_coords": True,
    "allowed_coords": [{"lat": Decimal(50.9462), "long": Decimal(8.1235)}],
}

sensors = [
    {
        "sensor": "esp12345",
        "elevation": 319.0,
        "lat": 51.18486,
        "long": 10.08179,
        "country": "GER",
        "state": "HE",
    }
]
