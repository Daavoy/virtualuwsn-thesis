# Virtual Underwater Sensor Network 

The main purpose of the virtual underwater sensor network is to be able inject simulated data into the SmartOcean platform. 
The data can be simulated in various ways:
* From historic data files
* Custom generated data

# Install

```
python -m pip install -r requirements.txt
```

# Configuration

```
BROKER_URL=url
BROKER_PORT=port
TOPIC=topic
QOS=qos
BROKER_USERNAME=username
BROKER_PASSWORD=password
NR_OF_MESSAGES=nr_of_message
PUBLISH_SLEEP_TIME=publish_sleep_time
```

The default configuration of the VUWSN is to generate data in the SmartOcean format. To simulate historic data from files, another environment variable must be provided:
```
TESTDATA_PATH=path_to_data
```

## Running locally
MQTT broker configuration and credentials are to be placed in a `.env` file

## Running in Docker container
MQTT broker configuration and credentials have to be provided as environment variables to the container

# Execution
Running the main.py will start the simulation based on the configuration:
* If the TESTDATA_PATH is present and valid, a DataFileHubNode transmits historical data from data files found at the provided path
* If not a VirtualSensorHubNode transmits generated data in the SmartOcean format