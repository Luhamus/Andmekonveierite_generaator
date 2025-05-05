INTERACTIVE_MODE=True
PLATFORM="Telegraf"


#### Nifi ####

NIFI_HOST="https://127.0.0.1.nip.io"
NIFI_DEPLOY=True

NIFI_USER="lab08nifiuser"
NIFI_PASS="tartunifi2023"

MEASUREMENT_NAME="testers_measurementersNames"

## Database
DB_URL="http://influxdb:8086"
#DB_NAME="nifi_weatherData"
DB_NAME="telegraf_weatherData"
DB_USER="admin"
DB_PASS="admin"

#### Telegraf ####

#TBA



#### Over all ####

## Needed if Interactive mode turned off
API_URL="https://api.open-meteo.com/v1/forecast?latitude=37.9838&longitude=23.7275&current_weather=true"
API_FIELDS={'temperature': '.current_weather.temperature', 'windspeed': '.current_weather.windspeed'}
API_USERNAME="rasmus.luha"
API_PASSWORD="rasmusPass"
PIPELINE_SCHEDULING_PERIOD="15"
PIPELINE_NAME="TestPiper"
