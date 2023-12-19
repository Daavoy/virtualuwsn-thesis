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

| Env Variable        | Explanation                                       | Mandatory | Default     |
|---------------------|---------------------------------------------------|-----------|-------------|
| BROKER_URL          | URL of the MQTT broker                            | Yes       | -           |
| BROKER_PORT         | Port number of the MQTT broker                    | Yes       | -           |
| TOPIC               | MQTT topic to publish messages to                 | Yes       | -           |
| QOS                 | Quality of Service level for message delivery     | Yes       | -           |
| BROKER_USERNAME     | Username for connecting to the MQTT broker        | Yes       | -           |
| BROKER_PASSWORD     | Password for connecting to the MQTT broker        | Yes       | -           |
| NR_OF_MESSAGES      | Number of messages published for each experiment  | Yes       | -           |
| PUBLISH_SLEEP_TIME  | Interval between each publish                     | Yes       | -           |
| TLS_ENABLED         | Determines if the client is configured with TLS   | Yes       | True        |
| TESTDATA_PATH       | Path to test data                                 | No        | -           |

The default configuration of the VUWSN is to generate data in the SmartOcean format. To simulate historic data from files, the TESTDATA_PATH environment variable must be provided:

Current testdata includes:
* testdata/aadi/erroneous_data (sample of AADI data with errors)
* testdata/aadi/SFI_Austevoll_NordDestination (AADI data from Austevoll North)
* testdata/aadi/SFI_Austevoll_SorDestination (AADI data from Austevoll Sor)
* testdata/aadi/valid_data (sample of valid AADI data)
* wsense/valid_data (sample of valid WSense data)

## Running locally
MQTT broker credentials and experiment configuration are to be placed in an `.env` file

## Running in Docker container
To create a docker image, use the docker build command with the Dockerfile as input. 
```
docker build -t <image_name>:<tag> -f Dockerfile .
```

MQTT broker credentials and experiment configuration have to be provided as environment variables to the container, e.g. by providing an .env file when running the container:
```
docker run --env-file .env  --name <name> <image_name>
```

Example:
```
docker build -t virtualuwsn:latest -f Dockerfile .

docker run --env-file .env --name SO-vuwsn virtualuwsn
```

# Execution
Running the main.py will start the simulation based on the configuration:
* If the TESTDATA_PATH is present and valid, the hubnode will be connected to a FileVUWSN that transmits historical data from data files found at the provided path
* If not a TempCondBattVUWSN (consisting of a temperature, a conductivity and a battery sensor) transmits generated data in the SmartOcean format