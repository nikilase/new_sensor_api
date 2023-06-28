from influxdb import InfluxDBClient
from influxdb.resultset import ResultSet

from conf.config import influxdb as inf


def write_line(tags: dict, fields: dict, measurement: str = inf["msrmt"]):
	database: str = inf["db"]
	if measurement == "water":
		database = "NodeRed"
	print(f"{measurement} {database}")
	try:
		client = InfluxDBClient(host=inf["host"], port=inf["port"], username=inf["user"], password=inf["pwd"],
							database= database, ssl=inf["ssl"], verify_ssl=inf["verify_ssl"])
		json_body = [
			{
				"measurement": measurement,
				"fields": fields
			}
		]
		client.write_points(json_body, tags=tags, time_precision=inf["prec"], retention_policy=inf["ret"],
							consistency=inf["cons"])
		client.close()
		return True
	except Exception as e:
		print(e)
		return False

def get_latest_data(chip_id: str = "esp11609738"):
	try:
		client = InfluxDBClient(host=inf["host"], port=inf["port"], username=inf["user"], password=inf["pwd"],
							database= inf["db"], ssl=inf["ssl"], verify_ssl=inf["verify_ssl"])


		query = f"SELECT * FROM \"{inf['msrmt']}\" WHERE (\"sensorID\"='{chip_id}') ORDER BY time DESC LIMIT 1"
		result: ResultSet = client.query(query)
		client.close()

		result_dict = {}
		for point in result.get_points():
			result_dict.update(point)
		return result_dict

	except Exception as e:
		print(e)
		return False

