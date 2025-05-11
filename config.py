INTERACTIVE_MODE=False
PLATFORM="Telegraf"


#### Nifi specific ####

NIFI_HOST="https://127.0.0.1.nip.io"
NIFI_DEPLOY=True

NIFI_USER="lab08nifiuser"
NIFI_PASS="tartunifi2023"

MEASUREMENT_NAME="Tartu_ilmaandmed"

## Database
DB_URL="http://influxdb:8086"
#DB_NAME="nifi_weatherData"
DB_NAME="telegraf_weatherData"
DB_USER="admin"
DB_PASS="admin"


#### Over all ####

## Needed if Interactive mode turned off
#API_URL="https://api.open-meteo.com/v1/forecast?latitude=37.9838&longitude=23.7275&current_weather=true"
API_URL="https://api.openweathermap.org/data/2.5/weather?q=Tartu&units=metric&lang=en&appid=01786b7e8b623a1d2112d672ecae1d0d"
#API_FIELDS={'temperature': '.current_weather.temperature', 'windspeed': '.current_weather.windspeed'}
API_FIELDS={'temp': '.main.temp', 'winds': '.wind.speed'}
API_USERNAME="rasmus.luha"
API_PASSWORD="Placeholder"
PIPELINE_SCHEDULING_PERIOD="10"
PIPELINE_NAME="OpenWeather_pipeline"
