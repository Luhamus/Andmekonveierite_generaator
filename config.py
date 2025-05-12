INTERACTIVE_MODE=True
#PLATFORM="Telegraf"


#### Nifi specific ####

NIFI_HOST="https://127.0.0.1.nip.io"
NIFI_DEPLOY=True

NIFI_USER="nifi_user"
NIFI_PASS="nifi_passwod"

MEASUREMENT_NAME="measurement_name"



##j## Database ####
DB_URL="http://influxdb:8086"
DB_NAME="nifi_weatherData"
DB_USER="admin"
DB_PASS="admin"



#### Over all ####

## Needed if Interactive mode turned off
API_URL="https://api.open-meteo.com/v1/forecast?latitude=37.9838&longitude=23.7275&current_weather=true"
API_FIELDS={'temperature': '.current_weather.temperature', 'windspeed': '.current_weather.windspeed'}
API_USERNAME="Placeholder"
API_PASSWORD="Placeholder"
PIPELINE_SCHEDULING_PERIOD="10"
PIPELINE_NAME="pipelineName"
