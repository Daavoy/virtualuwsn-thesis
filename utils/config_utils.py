import argparse
import os
from decouple import config
import yaml
import sys

from mqtt_connector.mqtt.configs import BrokerConfig, ConnectConfig, ReattemptConfig, MQTTClientConfig

class VUWSNConfigurationException(Exception):
    pass

class SmartOceanDataConfig:
    def __init__(self, description: str, timeseries: str, source: str, source_id: str, latitude: float, longitude: float,
                 format: str):
        self.DESCRIPTION = description
        self.TIMESERIES = timeseries
        self.SOURCE = source
        self.SOURCE_ID = source_id
        self.LOCATION_LATITUDE = latitude
        self.LOCATION_LONGITUDE = longitude
        self.FORMAT = format

class VUWSNConfig:
        def __init__(self, mqtt_config:MQTTClientConfig, nr_of_messages:int, publish_interval:int, data_path:str=None,
                     so_data_config:SmartOceanDataConfig=None):
            self.MQTT_CONFIG = mqtt_config
            self.TESTDATA_PATH = data_path
            self.NR_OF_MESSAGES = nr_of_messages
            self.PUBLISH_INTERVAL = publish_interval
            self.SMARTOCEAN_DATA_CONFIG = so_data_config


def getVUWSNConfig()->VUWSNConfig:
    """
        Get the VUWSN configuration from the environment and config file.
        If no config file is specified, the default config file, located at 'configs/config-broker-evaluation.yml',  is used.

        Returns:
            VUWSNConfig: A VUWSNConfig object containing the configuration.

        Raises:
            VUWSNConfigurationException: If an error occurs when loading the configuration.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--configfile", default="configs/config-broker-evaluation.yml", help="Path to the config file")
    args = parser.parse_args()

    if not os.path.exists(args.configfile):
        raise VUWSNConfigurationException(f"Error: The configfile '{args.configfile}' does not exist.")
    
    # load credentials
    try:  
        USERNAME = config('BROKER_USERNAME')
        PASSWORD = config('BROKER_PASSWORD')
    except Exception as e:
        raise VUWSNConfigurationException(f"Error when reading credentials from environment: {e}")
    
    # load configuration from config file
    try:
        with open(args.configfile) as f:
            conf = yaml.load(f, Loader=yaml.FullLoader)
            BROKER_PORT = conf['BROKER_PORT']
            BROKER = conf['BROKER_URL']
            TOPIC = conf['TOPIC']
            QOS = conf['QOS']
            CLEAN_START = conf.get('CLEAN_START', False)
            KEEPALIVE = conf.get('KEEPALIVE', 120)
            SESSION_EXPIRY_INTERVAL = conf.get('SESSION_EXPIRY_INTERVAL', 3600)
            TLS_ENABLED = conf.get('TLS_ENABLED', False)
            RETAIN = conf.get('RETAIN', False)
            REATTEMPTS = conf.get('REATTEMPTS', 5)
            REATTEMPT_MIN_DELAY = conf.get('REATTEMPT_MIN_DELAY', 2)
            REATTEMPT_MAX_DELAY = conf.get('REATTEMPT_MAX_DELAY', 3600)
            NR_OF_MESSAGES = conf.get('NR_OF_MESSAGES')
            PUBLISH_INTERVAL = conf.get('PUBLISH_INTERVAL', 5)
            TESTDATA_PATH = conf.get("TESTDATA_PATH", "").strip() # Path to test data files, if omitted the simulator will generate custom test data in SmartOcean format

            so_data_config = None
            if TESTDATA_PATH is None or TESTDATA_PATH == "":
                # Load SmartOcean data configuration
                DESCRIPTION = conf.get('DESCRIPTION', "SmartOcean VUWSN Sensor Hub Timeseries")
                TIMESERIES = conf.get('TIMESERIES', "SmartOceanVUWSN:0001")
                SOURCE = conf.get('SOURCE', 'SmartOcean VUWSN Sensor Hub')
                SOURCE_ID = conf.get('SOURCE_ID', '0001')
                LATITUDE = conf.get('LOCATION_LATITUDE', 60.0)
                LONGITUDE = conf.get('LOCATION_LONGITUDE', 5.5)
                FORMAT = conf.get('FORMAT', "SMARTOCEAN_V1")
                so_data_config = SmartOceanDataConfig(DESCRIPTION, TIMESERIES, SOURCE, SOURCE_ID, LATITUDE, LONGITUDE, FORMAT)

    except Exception as e:
        raise VUWSNConfigurationException(f"Error when reading from config file: {e}")

    connect_config = ConnectConfig(use_tls=TLS_ENABLED, clean_start=CLEAN_START, keepalive=KEEPALIVE, 
                                   session_expiry_interval=SESSION_EXPIRY_INTERVAL)
    reattempt_config = ReattemptConfig(REATTEMPTS, REATTEMPT_MIN_DELAY, REATTEMPT_MAX_DELAY)
    broker_config = BrokerConfig(USERNAME, PASSWORD, BROKER_PORT, BROKER, TOPIC, QOS)

    mqtt_config = MQTTClientConfig(broker_config, connect_config, reattempt_config, RETAIN)
    
    return VUWSNConfig(mqtt_config, NR_OF_MESSAGES, PUBLISH_INTERVAL, TESTDATA_PATH, so_data_config)
    

