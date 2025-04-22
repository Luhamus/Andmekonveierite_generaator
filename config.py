INTERACTIVE_MODE=True

## Nifi
NIFI_USER="lab08nifiuser"
NIFI_PASS="tartunifi2023"

NIFI_HOST="https://127.0.0.1.nip.io"
NIFI_DEPLOY=False

NIFI_MEASUREMENT_NAME="test_measurementName"


## Database
DB_URL="http://influxdb:8086/write?db=nifi_weatherData"
DB_USER="admin"

## TODO - somehow must be hidden inside the pipeline in the end
DB_PASS="admin"



###############################



## Needed if Interactive mode turned off
API_URL="https://api.open-meteo.com/v1/forecast?latitude=58.38&longitude=26.72&current_weather=true"
API_FIELDS={'temperature': '.current_weather.temperature', 'windspeed': '.current_weather.windspeed'}
API_USERNAME="TODO"
API_PASSWORD="TODO"
PIPELINE_SCHEDULING_PERIOD="5 sec"
PIPELINE_NAME="test_pipeline.json"
