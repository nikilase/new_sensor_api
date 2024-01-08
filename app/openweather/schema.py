import json
from typing import List, Optional
from pydantic import BaseModel, Field


class WeatherData(BaseModel):
    id: Optional[int] = Field(None, description='Weather condition id', example=803)
    main: Optional[str] = Field(None, description='Group of weather parameters (Rain, Snow etc.)', example='Clouds')
    description: Optional[str] = Field(None, description='Weather condition within the group',
                                       example='Überwiegend bewölkt')
    icon: Optional[str] = Field(None, description='Weather icon id', example='04d')


class FeelsLike(BaseModel):
    morn: Optional[float] = Field(None, description='Morning temperature.', example=8.3)
    day: Optional[float] = Field(None, description='Day temperature.', example=10.4)
    eve: Optional[float] = Field(None, description='Evening temperature.', example=4.5)
    night: Optional[float] = Field(None, description='Night temperature.', example=-0.5)


class Temp(BaseModel):
    morn: Optional[float] = Field(None, description='Morning temperature.', example=8.3)
    day: Optional[float] = Field(None, description='Day temperature.', example=10.4)
    eve: Optional[float] = Field(None, description='Evening temperature.', example=4.5)
    night: Optional[float] = Field(None, description='Night temperature.', example=-0.5)
    min: Optional[float] = Field(None, description='Min daily temperature.', example=-0.5)
    max: Optional[float] = Field(None, description='Max daily temperature.', example=10.4)


class Rain(BaseModel):
    h: Optional[float] = Field(None, description='(where available) Precipitation, mm/h. Please note that only mm/h as '
                                                 'units of measurement are available for this parameter', example=12.5)


class Snow(BaseModel):
    h: Optional[float] = Field(None, description='where available) Precipitation, mm/h. Please note that only mm/h as '
                                                 'units of measurement are available for this parameter', example=20.6)


class Current(BaseModel):
    dt: Optional[int] = Field(None, description='Time of the forecasted data, unix, UTC', example=1704651747)
    sunrise: Optional[int] = Field(None, description='Sunrise time, Unix, UTC. For polar areas in midnight sun and '
                                                     'polar night periods this parameter is not returned in the '
                                                     'response', example=1704693566)
    sunset: Optional[int] = Field(None, description='Sunset time, Unix, UTC. For polar areas in midnight sun and polar '
                                                    'night periods this parameter is not returned in the response',
                                  example=1704727422)
    temp: Optional[float] = Field(None, description='Units – default: kelvin, metric: Celsius, imperial: Fahrenheit.',
                                  example=8.4)
    feels_like: Optional[float] = Field(None, description='This accounts for the human perception of weather. Units – '
                                                          'default: kelvin, metric: Celsius, imperial: Fahrenheit.',
                                        example=5.9)
    pressure: Optional[int] = Field(None, description='Atmospheric pressure on the sea level, hPa', example=1030)
    humidity: Optional[int] = Field(None, description='Humidity, %', example=58)
    dew_point: Optional[float] = Field(None, description='Atmospheric temperature (varying according to pressure and '
                                                         'humidity) below which water droplets begin to condense and '
                                                         'dew can form. Units – default: kelvin, metric: Celsius, '
                                                         'imperial: Fahrenheit.', example=-13.27)
    clouds: Optional[int] = Field(None, description='Cloudiness, %', example=55)
    uvi: Optional[float] = Field(None, description='The maximum value of UV index for the day', example=0.51)
    visibility: Optional[int] = Field(None, description='Average visibility, metres. The maximum value of the '
                                                        'visibility is 10 km', example=10000)
    wind_speed: Optional[float] = Field(None, description='Wind speed. Units – default: metre/sec, metric: metre/sec, '
                                                          'imperial: miles/hour.', example=5.33)
    wind_gust: Optional[float] = Field(None, description='(where available) Wind gust. Units – default: metre/sec, '
                                                         'metric: metre/sec, imperial: miles/hour.', example=14.1)
    wind_deg: Optional[int] = Field(None, description='Wind direction, degrees (meteorological)', example=71)
    rain: Optional[Rain] = Field(None, description='(where available) Precipitation volume, mm. Please note that only '
                                                   'mm as units of measurement are available for this parameter',
                                 example=12.6)
    snow: Optional[Snow] = Field(None, description='(where available) Snow volume, mm. Please note that only mm as '
                                                   'units of measurement are available for this parameter',
                                 example=4.5)
    weather: Optional[List[WeatherData]] = Field(None, description='Weather Condition and icon')


class Minutely(BaseModel):
    dt: Optional[int] = Field(None, description='Time of the forecasted data, unix, UTC', example=1704651747)
    precipitation: Optional[float] = Field(None, description='Precipitation, mm/h. Please note that only mm/h as units '
                                                             'of measurement are available for this parameter',
                                           example=1.5)


class Hourly(BaseModel):
    dt: Optional[int] = Field(None, description='Time of the forecasted data, unix, UTC', example=1704651747)
    temp: Optional[float] = Field(None, description='Units – default: kelvin, metric: Celsius, imperial: Fahrenheit.',
                                  example=8.4)
    feels_like: Optional[float] = Field(None, description='This accounts for the human perception of weather. Units – '
                                                          'default: kelvin, metric: Celsius, imperial: Fahrenheit.',
                                        example=5.9)
    pressure: Optional[int] = Field(None, description='Atmospheric pressure on the sea level, hPa', example=1030)
    humidity: Optional[int] = Field(None, description='Humidity, %', example=58)
    dew_point: Optional[float] = Field(None, description='Atmospheric temperature (varying according to pressure and '
                                                         'humidity) below which water droplets begin to condense and '
                                                         'dew can form. Units – default: kelvin, metric: Celsius, '
                                                         'imperial: Fahrenheit.', example=-13.27)
    uvi: Optional[float] = Field(None, description='The maximum value of UV index for the day', example=0.51)
    clouds: Optional[int] = Field(None, description='Cloudiness, %', example=55)
    visibility: Optional[int] = Field(None, description='Average visibility, metres. The maximum value of the '
                                                        'visibility is 10 km', example=10000)
    wind_speed: Optional[float] = Field(None, description='Wind speed. Units – default: metre/sec, metric: metre/sec, '
                                                          'imperial: miles/hour.', example=5.33)
    wind_gust: Optional[float] = Field(None, description='(where available) Wind gust. Units – default: metre/sec, '
                                                         'metric: metre/sec, imperial: miles/hour.', example=14.1)
    wind_deg: Optional[int] = Field(None, description='Wind direction, degrees (meteorological)', example=71)
    pop: Optional[int] = Field(None, description='Probability of precipitation. The values of the parameter vary '
                                                 'between 0 and 1, where 0 is equal to 0%, 1 is equal to 100%',
                               example=0)
    rain: Optional[Rain] = Field(None, description='(where available) Precipitation volume, mm. Please note that only '
                                                   'mm as units of measurement are available for this parameter',
                                 example=12.6)
    snow: Optional[Snow] = Field(None, description='(where available) Snow volume, mm. Please note that only mm as '
                                                   'units of measurement are available for this parameter',
                                 example=4.5)
    weather: Optional[List[WeatherData]] = Field(None, description='Weather Condition and icon')


class Daily(BaseModel):
    dt: Optional[int] = Field(None, description='Time of the forecasted data, unix, UTC', example=1704651747)
    sunrise: Optional[int] = Field(None, description='Sunrise time, Unix, UTC. For polar areas in midnight sun and '
                                                     'polar night periods this parameter is not returned in the '
                                                     'response', example=1704693566)
    sunset: Optional[int] = Field(None, description='Sunset time, Unix, UTC. For polar areas in midnight sun and polar '
                                                    'night periods this parameter is not returned in the response',
                                  example=1704727422)
    moonrise: Optional[int] = Field(None, description='The time of when the moon rises for this day, Unix, UTC',
                                    example=1704688460)
    moonset: Optional[int] = Field(None, description='The time of when the moon sets for this day, Unix, UTC',
                                   example=1704715580)
    moon_phase: Optional[float] = Field(None, description="Moon phase. 0 and 1 are 'new moon', 0.25 is 'first quarter "
                                                          "moon', 0.5 is 'full moon' and 0.75 is 'last quarter moon'. "
                                                          "The periods in between are called 'waxing crescent', "
                                                          "'waxing gibbous', 'waning gibbous', and 'waning crescent', "
                                                          "respectively. Moon phase calculation algorithm: if the "
                                                          "moon phase values between the start of the day and the end "
                                                          "of the day have a round value (0, 0.25, 0.5, 0.75, 1.0), "
                                                          "then this round value is taken, otherwise the average of "
                                                          "moon phases for the start of the day and the end of the day "
                                                          "is taken", example=0.89)
    summary: Optional[str] = Field(None, description='Human-readable description of the weather conditions for the day',
                                   example='You can expect partly cloudy in the morning, with clearing in the '
                                           'afternoon')
    temp: Optional[Temp] = Field(None, description='Units – default: kelvin, metric: Celsius, imperial: Fahrenheit.')
    feels_like: Optional[FeelsLike] = Field(None, description='This accounts for the human perception of weather. '
                                                              'Units – default: kelvin, metric: Celsius, imperial: '
                                                              'Fahrenheit.')
    pressure: Optional[int] = Field(None, description='Atmospheric pressure on the sea level, hPa', example=1030)
    humidity: Optional[int] = Field(None, description='Humidity, %', example=58)
    dew_point: Optional[float] = Field(None, description='Atmospheric temperature (varying according to pressure and '
                                                         'humidity) below which water droplets begin to condense and '
                                                         'dew can form. Units – default: kelvin, metric: Celsius, '
                                                         'imperial: Fahrenheit.', example=-13.27)
    wind_speed: Optional[float] = Field(None, description='Wind speed. Units – default: metre/sec, metric: metre/sec, '
                                                          'imperial: miles/hour.', example=5.33)
    wind_gust: Optional[float] = Field(None, description='(where available) Wind gust. Units – default: metre/sec, '
                                                         'metric: metre/sec, imperial: miles/hour.', example=14.1)
    wind_deg: Optional[int] = Field(None, description='Wind direction, degrees (meteorological)', example=71)
    clouds: Optional[int] = Field(None, description='Cloudiness, %', example=55)
    uvi: Optional[float] = Field(None, description='The maximum value of UV index for the day', example=0.51)
    pop: Optional[int] = Field(None, description='Probability of precipitation. The values of the parameter vary '
                                                 'between 0 and 1, where 0 is equal to 0%, 1 is equal to 100%',
                               example=0)
    rain: Optional[float] = Field(None, description='(where available) Precipitation volume, mm. Please note that only '
                                                    'mm as units of measurement are available for this parameter',
                                  example=12.6)
    snow: Optional[float] = Field(None, description='(where available) Snow volume, mm. Please note that only mm as '
                                                    'units of measurement are available for this parameter',
                                  example=4.5)
    weather: Optional[List[WeatherData]] = Field(None, description='Weather Condition and icon')


class Alerts(BaseModel):
    sender_name: Optional[str] = Field(None, description='Name of the alert source', example='Deutscher Wetterdienst')
    event: Optional[str] = Field(None, description='Alert event name', example='icy surfaces')
    start: Optional[int] = Field(None, description='Date and time of the start of the alert, Unix, UTC',
                                 example=1704646800)
    end: Optional[int] = Field(None, description='Date and time of the end of the alert, Unix, UTC',
                               example=1704704400)
    description: Optional[str] = Field(None, description='Description of the alert',
                                       example='There is a risk of icy surfaces (Level 1 of 4).')
    tags: Optional[List[str]] = Field(None, description='Type of severe weather', example=['Other dangers'])


class OpenweatherData(BaseModel):
    lat: Optional[float] = Field(None, description=' Latitude of the location, decimal (−90; 90)', example=-16.92)
    lon: Optional[float] = Field(None, description='Longitude of the location, decimal', example=145.77)

    timezone: Optional[str] = Field(None, description='Timezone name for the requested location',
                                    example='Europe/Berlin')
    timezone_offset: Optional[int] = Field(None, description='Shift in seconds from UTC', example=3600)

    current: Optional[Current] = Field(None, description='Current weather data API response')

    minutely: Optional[List[Minutely]] = Field(None, description='Minute forecast weather data API response')

    hourly: Optional[List[Hourly]] = Field(None, description='Hourly forecast weather data API response')

    daily: Optional[List[Daily]] = Field(None, description='Daily forecast weather data API response')

    alerts: Optional[List[Alerts]] = Field(None, description='National weather alerts data from major national weather '
                                                             'warning systems')


def openweather_data_from_json(obj: dict) -> OpenweatherData:
    ow = OpenweatherData()
    ow.lat = obj["lat"]
    ow.lon = obj["lon"]
    ow.timezone = obj["timezone"]
    ow.timezone_offset = obj["timezone_offset"]
    ow.current = obj["current"]
    ow.minutely = obj["minutely"]
    ow.hourly = obj["hourly"]
    ow.daily = obj["daily"]
    ow.alerts = obj["alerts"]
    return ow
