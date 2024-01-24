import argparse
import os
from decouple import config
import yaml
import sys

sys.path.append(os.path.abspath("../"))
from mqtt_connector.mqtt_client import BrokerConfig, ConnectConfig, ReattemptConfig

class VUWSNConfigurationException(Exception):
    pass

class VUWSNConfig:
        def __init__(self, broker_config:BrokerConfig, connect_config:ConnectConfig, reattempt_config:ReattemptConfig, retain_flag:bool, 
                     nr_of_messages:int, publish_sleep_time:int, data_path:str=None):
            self.BROKER_CONFIG = broker_config
            self.CONNECT_CONFIG = connect_config
            self.REATTEMPT_CONFIG = reattempt_config
            self.RETAIN = retain_flag
            self.TESTDATA_PATH = data_path
            self.NR_OF_MESSAGES = nr_of_messages
            self.PUBLISH_SLEEP_TIME = publish_sleep_time


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
            PUBLISH_SLEEP_TIME = conf.get('PUBLISH_SLEEP_TIME', 5)
            TESTDATA_PATH = conf.get("TESTDATA_PATH", "").strip() # Path to test data files, if omitted the simulator will generate custom test data in SmartOcean format
    except Exception as e:
        raise VUWSNConfigurationException(f"Error when reading from config file: {e}")

    connect_config = ConnectConfig(use_tls=TLS_ENABLED, clean_start=CLEAN_START, keepalive=KEEPALIVE, 
                                   session_expiry_interval=SESSION_EXPIRY_INTERVAL)
    reattempt_config = ReattemptConfig(REATTEMPTS, REATTEMPT_MIN_DELAY, REATTEMPT_MAX_DELAY)
    broker_config = BrokerConfig(USERNAME, PASSWORD, BROKER_PORT, BROKER, TOPIC, QOS)
    
    return VUWSNConfig(broker_config, connect_config, reattempt_config, RETAIN, NR_OF_MESSAGES, PUBLISH_SLEEP_TIME, TESTDATA_PATH)
    

