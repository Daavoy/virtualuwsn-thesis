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

MQTT broker configuration and credentials for the broker is to be placed in a `.env` file with the content:

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

# Execution
The main.py script can be execute with or without data_path arg:
* Without data_path arg a VirtualSensorHubNode transmits generated data in the SmartOcean format
* With a valid data_path arg a DataFileHubNode transmits historical data from data files found at the provided path