# Virtual Underwater Sensor Network 
The main purpose of the virtual underwater sensor network is to be able inject simulated data into the SmartOcean platform. 
The data can be simulated in various ways:
* From historic data files
* Custom generated data in SmartOcean format

## Setup
Install python packages from requirements.txt:

```
python -m pip install -r requirements.txt
```

The project reuses MQTT client componets from the [MQTT Connector](https://github.com/smartoceanplatform/mqtt_connector) project, and the current setup expects the MQTT Connector to be in the same parent folder as the virtualuwsn project. 


## Configuration
Credentials for the broker is to be placed in a .env file with the following content:

| Env variable        | Explanation                                       | Mandatory | Default     |
|---------------------|---------------------------------------------------|-----------|-------------|
| BROKER_USERNAME     | Username for connecting to the MQTT broker        | Yes       | -           |
| BROKER_PASSWORD     | Password for connecting to the MQTT broker        | Yes       | -           |

The remaining configuration is placed in a .yml file with the following content. 

| Config variable     | Explanation                                                                   | Mandatory | Default     |
|---------------------|-------------------------------------------------------------------------------|-----------|-------------|
| BROKER_URL          | URL of the MQTT broker                                                        | Yes       | -           |
| BROKER_PORT         | Port number of the MQTT broker                                                | Yes       | -           |
| TOPIC               | MQTT topic to publish messages to                                             | Yes       | -           |
| QOS                 | Quality of Service level for message delivery                                 | Yes       | -           |
| NR_OF_MESSAGES      | Number of messages to publish                                                 | Yes       | 5           |
| PUBLISH_SLEEP_TIME  | Interval between each publish                                                 | Yes       | 5           |
| TLS_ENABLED         | Determines if the client is configured with TLS                               | Yes       | False       |
| TESTDATA_PATH       | Path to test data                                                             | No        | ""          |
| RETAIN              | Determines the retain flag for publish packets                                | No        | False       |
| RECONNECT_ATTEMPTS  | Determines the amount of reconnect attempts before shutting down              | No        | -1          |
| RECONNECT_MIN_DELAY | Sets the minimum time period, in seconds, to wait before trying to reconnect  | No        | 1           |
| RECONNECT_MAX_DELAY | Sets the maximum time period, in seconds, to wait before trying to reconnect  | No        | 120         |

Configuration .yml files are placed in the */configs* folder, and the data path to a specific configuration file is provided as input to the main script. The default configuration, if no input is provided, is the configuration at *configs/config-broker-evaluation.yml*. 

The default behaviour of the VUWSN is to generate data in the SmartOcean format. To simulate historic data from files, the TESTDATA_PATH must be set to a specific testdata folder path.

Current testdata includes:
* testdata/aadi/erroneous_data (sample of AADI data with errors)
* testdata/aadi/SFI_Austevoll_NordDestination (AADI data from Austevoll North)
* testdata/aadi/SFI_Austevoll_SorDestination (AADI data from Austevoll Sor)
* testdata/aadi/valid_data (sample of valid AADI data)
* wsense/valid_data (sample of valid WSense data)

## Running the project
### Running locally
MQTT broker credentials are to be placed in an `.env` file, while the remaining configuration is provided in the input configuration file. 

### Running in Docker container
To create a docker image, use the docker build command with the [Dockerfile](Dockerfile) as input. Since the MQTT Connector needs to be copied in to the container, run the command from the parent folder of both projects. 
```
docker build -t <image_name>:<tag> -f Dockerfile .
```

MQTT broker credentials and configuration are provided as environment variables and input argument to the container, e.g. by providing an .env file and configuration file when running the container:
```
docker run --env-file <.env_file>  --name <name> <image_name> --configfile <path_to_configfile>
```

#### Example:
```
docker build -t virtualuwsn:latest -f virtualuwsn/Dockerfile .

docker run --env-file virtualuwsn/.env --name aadivuwsn virtualuwsn --configfile configs/config-aadinode-test.yml
```

### Main script
Running the main.py script will start the simulation based on the configuration:
* If the TESTDATA_PATH is present and valid, the hubnode will be connected to a FileVUWSN that transmits historical data from data files found at the provided path
* If not a TempCondBattVUWSN (consisting of a temperature, a conductivity and a battery sensor) transmits generated data in the SmartOcean format