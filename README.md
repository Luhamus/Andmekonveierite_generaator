# Pipeline generator
This is a pipeline generator that currently supports the following platforms: `Nifi`, `Telegraf`(TODO).

## Usage
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- Setup sutff in `config.py` (database and nifi auth etc)
- Then run `main.py`
WIP


## Configuration info
Configuration variables are defined in `config.py`, where sample Variables are already given.
WIP

### Variables

#### Nifi

| Variable Name       | Description                                     | Example Value              | 
|---------------------|-------------------------------------------------|----------------------------|-
| `NIFI_HOST`         | Base URL of the Apache NiFi instance            | `https://127.0.0.1.nip.io` | 
| `NIFI_USER`         | Username for authenticating in Nifi             | `nifi_username`            | 
| `NIFI_PASS`         | Username for authenticating in Nifi             | `nifi_password`            | 
| `NIFI_DEPLOY`       | Automatically delpoy pipeline to Nifi           | `True`                     | 
| `INTERACTIVE_MODE`  | If False you can parse through api call data    | `True`                     | 

In interactive mode you can manually give the API url, credentials and data fields for the pipeline from API response 
If you opt out the interactive mode you have to define needed variables in the config.py file before using the tool.

The following variables have to be defined if interactive mode is tured to `False`

| Variable Name                 | Description                               | Example Value                                                                               |
|-------------------------------|-------------------------------------------|---------------------------------------------------------------------------------------------|
| API_URL                       | API url that returens JSON data           | https://api.open-meteo.com/v1/forecast?latitude=58.38&longitude=26.72&current_weather=true" |
| API_FIELDS                    | Data fields for pipeline, with json paths | {'temperature': '.current_weather.temperature', 'windspeed': '.current_weather.windspeed'}  |
| API_USERNAME                  | Api username, if required                 | Placeholder"                                                                                |
| API_PASSWORD                  | Api username, if required                 | Placehoder"                                                                                 |
| PIPELINE_SCHEDULING_PERIOD    | How often the pipeline should run         | 5 sec                                                                                       |
| PIPELINE_NAME                 | Name of the pipeline                      | test_pipeline.json                                                                          |


#### Database
Database variales have to be filled out before using the tool as currently there is only influxDB support.

| Variable Name       | Description                              | Example Value                                    | 
|---------------------|------------------------------------------|--------------------------------------------------|
| `DB_URL`            | Url to the influxDB for the pipeline     | `http://influxdb:8086/write?db=nifi_weatherData` | 
| `DB_USER`           | Database usernmae                        | `admin`                                          | 
| `DB_PASS`           | Database passwod                         | `admin`                                          | 



## Current Repo structure
```
|-- common
|   `-- core.py
|-- config.py
|-- main.py
|-- modules
|   |-- nifi
|   |   |-- core.py
|   |   `-- templates
|   |       |-- ...
|   `-- telegraf
|       `-- core.py
|-- pipelines
|   `-- <Generated pipelines>
|-- README.md
`-- requirements.txt
```


### Samples

Currently testing with 2 following apis (sample urls):
  - https://api.open-meteo.com/v1/forecast?latitude=58.38&longitude=26.72&current_weather=true
  - https://delta.iot.cs.ut.ee/measurement/measurements?source=780&?dateFrom=2024-10-15T00:00:00Z&dateTo=2024-10-16T00:00:01Z&pageSize=200&type=KogEN

