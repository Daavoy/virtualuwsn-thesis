# Virtual Underwater Sensor Network 
The main purpose of the virtual underwater sensor network is to be able inject simulated data into the SmartOcean platform. 
The data can be simulated in various ways:
* From historic data files
* Custom generated data in SmartOcean format

## Setup
### Getting the source code

Clone the git repository

```
git clone https://github.com/smartoceanplatform/virtualuwsn.git
```

The repository uses git submodules to include the [smartocean data model](https://github.com/smartoceanplatform/datamodels). The data model submodule can be fetched using:

```
git submodule update --init --recursive
```

If there is a need to later update the data models based on the submodule repository use:

```
 git submodule update --remote
```

### Python packages
Install python packages from requirements.txt:

```
python -m pip install -r requirements.txt
```

The project reuses MQTT client components from the [MQTT Connector](https://github.com/smartoceanplatform/mqtt_connector) project, and the current setup expects the MQTT Connector to be in the same parent folder as the virtualuwsn project. 


## Configuration
Broker credentials are to be placed in a .env file with the following content:

| Env variable        | Explanation                                       | Mandatory |
|---------------------|---------------------------------------------------|-----------|
| BROKER_USERNAME     | Username for connecting to the MQTT broker        | Yes       |
| BROKER_PASSWORD     | Password for connecting to the MQTT broker        | Yes       |

The remaining configuration is placed in a .yml file with the following content: 

| Config variable     | Explanation                                                                          | Mandatory | Default     |
|---------------------|--------------------------------------------------------------------------------------|-----------|-------------|
| BROKER_URL          | URL of the MQTT broker                                                               | Yes       | -           |
| BROKER_PORT         | Port number of the MQTT broker                                                       | Yes       | -           |
| TOPIC               | MQTT topic to publish messages to                                                    | Yes       | -           |
| QOS                 | Quality of Service level for message delivery                                        | Yes       | -           |
| NR_OF_MESSAGES      | Number of messages to publish                                                        | Yes       | -           |
| CLEAN_START         | Determines if the client starts with a clean session.                                | Yes       | False       |
| KEEPALIVE           | Maximum period in seconds between communications with the broker. If no other messages are being exchanged, this controls the rate at which the client will send ping messages to the broker.                                 | Yes       | 120         |
| SESSION_EXPIRY_INTERVAL  | Session expiry interval for MQTT session in seconds                             | Yes       | 3600       |
| PUBLISH_SLEEP_TIME  | Interval between each publish                                                        | Yes       | 5           |
| TLS_ENABLED         | Determines if the client is configured with TLS                                      | Yes       | False       |
| RETAIN              | Determines the retain flag for publish packets                                       | Yes       | False       |
| REATTEMPTS  | Determines the amount of connect attempts before shutting down. < 0 means no limit | Yes       | 5         |
| REATTEMPT_MIN_DELAY | Sets the minimum time period, in seconds, to wait before trying to reattempt connect         | Yes       | 2           |
| REATTEMPT_MAX_DELAY | Sets the maximum time period, in seconds, to wait before trying to reattempt connect        | Yes       | 3600         |
| TESTDATA_PATH       | Path to test data                                                                    | No        | ""          |


Configuration .yml files are placed in the [configs](configs) folder, and the data path to a specific configuration file is provided as input to the main script. If no input is provided, the default configuration at [configs/config-broker-evaluation.yml](configs/config-broker-evaluation.yml) is used. 

The default behaviour of the VUWSN is to generate data in the SmartOcean format. To simulate historic data from files, the TESTDATA_PATH must be set to a specific testdata folder path.

Current testdata includes:
* testdata/aadi/erroneous_data (sample of AADI data with errors)
* testdata/aadi/SFI_Austevoll_NordDestination (AADI data from Austevoll North)
* testdata/aadi/SFI_Austevoll_SorDestination (AADI data from Austevoll Sor)
* testdata/aadi/valid_data (sample of valid AADI data)
* wsense/valid_data (sample of valid WSense data)

## Running the project
### Main script
Running the main.py script starts the simulation based on the configuration:
* If the TESTDATA_PATH is present and valid, the hubnode will be connected to a FileVUWSN that transmits historical data from data files found at the provided path. An exception is thrown if no files are found at the TESTDATA_PATH.
* If not a TempCondBattVUWSN (consisting of a temperature, a conductivity and a battery sensor) transmits generated data in the SmartOcean V0 format

### Running locally
MQTT broker credentials are to be placed in a `.env` file, while the remaining configuration is provided in the input .yml configuration file. Running the main.py script starts the simulation. 
```
python main.py --configfile <path_to_configfile>
```
### Running in Docker container
To create a docker image, use the docker build command with the [Dockerfile](Dockerfile) as input. Since the MQTT Connector needs to be copied to the container, run the command from the parent folder of both projects. 
```
docker build -t <image_name>:<tag> -f Dockerfile .
```

MQTT broker credentials and configuration are provided as environment variables and input arguments to the container, e.g. by providing a .env file and configuration file when running the container:
```
docker run --env-file <.env_file>  --name <name> <image_name> --configfile <path_to_configfile>
```

#### Examples:
```
docker build -t virtualuwsn:latest -f virtualuwsn/Dockerfile .
```
```
docker run --env-file virtualuwsn/.env --name aadivuwsn virtualuwsn --configfile configs/config-aadinode-test.yml
```

