# Pipeline generator
This is a pipeline generator that currently supports the following platforms: `Nifi`, `Telegraf`(TODO).

## Usage
WIP
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- Setup sutff in `config.py` (database and nifi auth etc)
- Then run `main.py`


## Configuration info
- Can configure under config.py
- sample VAR-s are given
WIP


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

