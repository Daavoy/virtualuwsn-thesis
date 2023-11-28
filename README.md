# Virtual Underwater Sensor Network 

The main purpose of the virtual underwater sensor network is to be able inject simulated data into the SmartOcean platform. 
The data can be simulated in various ways:
* From historic data files
* Custom generated data in SmartOcean format

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
Current testdata includes:
* testdata/aadi/erroneous_data (AADI data with errors)
* testdata/aadi/SFI_Austevoll_NordDestination (AADI data from Austevoll North)
* testdata/aadi/SFI_Austevoll_SorDestination (AADI data from Austevoll Sor)
* testdata/aadi/valid_data
* wsense/valid_data

## Running locally
MQTT broker configuration and credentials are to be placed in a `.env` file

## Running in Docker container
MQTT broker configuration and credentials have to be provided as environment variables to the container, e.g. by providing an .env file when running the container:
```
docker run --env-file .env  --name <name> <image_name>
```

# Execution
Running the main.py will start the simulation based on the configuration:
* If the TESTDATA_PATH is present and valid, the hubnode will be connected to a FileVUWSN that transmits historical data from data files found at the provided path
* If not a TempCondBattVUWSN (consisting of temperature, conductivity and battery sensor) transmits generated data in the SmartOcean format