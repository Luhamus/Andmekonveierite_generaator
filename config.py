INTERACTIVE_MODE=True
#PLATFORM="Telegraf"


#### Nifi specific ####

NIFI_HOST="https://127.0.0.1.nip.io"
NIFI_DEPLOY=True

NIFI_USER="lab08nifiuser"
NIFI_PASS="tartunifi2023"

MEASUREMENT_NAME="EurDol_kurss"

## Database
DB_URL="http://influxdb:8086"
#DB_NAME="nifi_weatherData"
DB_NAME="nifi_valuuta"
DB_USER="admin"
DB_PASS="admin"


#### Over all ####

## Needed if Interactive mode turned off
#API_URL="https://api.open-meteo.com/v1/forecast?latitude=37.9838&longitude=23.7275&current_weather=true"
API_URL="https://v6.exchangerate-api.com/v6/78660310eae8ed2c9ab662f8/latest/USD"
#API_FIELDS={'temperature': '.current_weather.temperature', 'windspeed': '.current_weather.windspeed'}
API_FIELDS={'temp': '.main.temp', 'winds': '.wind.speed'}
API_USERNAME="rasmus.luha"
API_PASSWORD="Placeholder"
PIPELINE_SCHEDULING_PERIOD="10"
PIPELINE_NAME="ExchangeRate_pipeline"
