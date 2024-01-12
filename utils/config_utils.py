import argparse
import os
from decouple import config
import yaml

class VUWSNConfigurationException(Exception):
    pass

class ReconnectConfig:
        def __init__(self, attempts:int=-1, min_delay:int=1, max_delay:int=120):
            self.ATTEMPTS = attempts
            self.MIN_DELAY = min_delay
            self.MAX_DELAY = max_delay

class BrokerConfig:
        def __init__(self, username, password, broker_port, broker_url, topic, qos):
            self.USERNAME = username
            self.PASSWORD = password
            self.BROKER_PORT = broker_port
            self.BROKER = broker_url
            self.TOPIC = topic
            self.QOS = qos

class VUWSNConfig:
        def __init__(self, broker_config:BrokerConfig, reconnect_config:ReconnectConfig, qos:int, retain_flag:bool, 
                     nr_of_messages:int,publish_sleep_time:int, use_tls:bool, data_path:str=None):
            self.USERNAME = broker_config.USERNAME
            self.PASSWORD = broker_config.PASSWORD
            self.BROKER = broker_config.BROKER
            self.BROKER_PORT = broker_config.BROKER_PORT
            self.TOPIC = broker_config.TOPIC
            self.QOS = qos
            self.RETAIN = retain_flag
            self.RECONNECT_CONFIG = reconnect_config
            self.TESTDATA_PATH = data_path
            self.NR_OF_MESSAGES = nr_of_messages
            self.PUBLISH_SLEEP_TIME = publish_sleep_time
            self.TLS_ENABLED = use_tls


def getVUWSNConfig()->VUWSNConfig:
    """
        Get the VUWSN configuration from the environment and config file.

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
            RETAIN = conf.get('RETAIN', False)
            RECONNECT_ATTEMPTS = conf.get('RECONNECT_ATTEMPTS', -1)
            RECONNECT_MIN_DELAY = conf.get('RECONNECT_MIN_DELAY', 1)
            RECONNECT_MAX_DELAY = conf.get('RECONNECT_MAX_DELAY', 120)
            NR_OF_MESSAGES = conf.get('NR_OF_MESSAGES')
            PUBLISH_SLEEP_TIME = conf.get('PUBLISH_SLEEP_TIME', 5)
            TLS_ENABLED = conf.get('TLS_ENABLED', False)
            TESTDATA_PATH = conf.get("TESTDATA_PATH", "").strip() # Path to test data files, if omitted the simulator will generate custom test data in SmartOcean format
    except Exception as e:
        raise VUWSNConfigurationException(f"Error when reading from config file: {e}")

    reconnect_config = ReconnectConfig(RECONNECT_ATTEMPTS, RECONNECT_MIN_DELAY, RECONNECT_MAX_DELAY)
    broker_config = BrokerConfig(USERNAME, PASSWORD, BROKER_PORT, BROKER, TOPIC, QOS)
    
    return VUWSNConfig(broker_config, reconnect_config, QOS, RETAIN, NR_OF_MESSAGES, PUBLISH_SLEEP_TIME, TLS_ENABLED, TESTDATA_PATH)
    

