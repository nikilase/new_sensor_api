import math
from conf.config import sensors

def get_height(chip_id: str):
	heights = [sensor["elevation"] for sensor in sensors if sensor["sensor"]==chip_id]
	if heights:
		return heights[0]
	else:
		return None

def normalize_pressure(pressure: float, height: float, temperature: float):
	p = 1 - ((0.0065 * height) / (temperature + 0.0065 * height + 273.15))
	p = pressure * math.pow(p, -5.257)
	return round(p*100) / 100