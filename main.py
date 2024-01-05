import sys
from decouple import config
import os
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mqtt_connector.mqtt_client import MQTTPublisher

from gateway import Gateway
from datamodels.timeseriesdata import Location
from hubnode import HubNode
from vuwsn import *
from utils.config_utils import *

if __name__ == "__main__":
    # Get VUWSN config
    try:
        config = getVUWSNConfig()
        # VUWSN setup
        gateway = None

        if config.TESTDATA_PATH is None or config.TESTDATA_PATH == "":
            location = Location(latitude=60.3692257067, longitude=5.3505234505, elevation=0)
            vuwsn = TempCondBattVUWSN("VUWSN", location)
            node = HubNode("VUWSN for SmartOcean data", "VUWSN", vuwsn)
            gateway = Gateway("Virtual SmartOcean Gateway", [node])
        elif not os.path.exists(config.TESTDATA_PATH):
            print(f"Error: The data_path '{config.TESTDATA_PATH}' does not exist.")
        else:
            origin = f"Data File {config.TESTDATA_PATH}"
            vuwsn = FileVUWSN("Data File VUWSN", config.TESTDATA_PATH)
            node = HubNode("VUWSN for historic data", origin, vuwsn)
            gateway = Gateway(f"Virtual Data File Gateway {config.TESTDATA_PATH}", [node])
        
        if gateway is not None:
            if config.NR_OF_MESSAGES >= 0 and config.PUBLISH_SLEEP_TIME >= 0:
                # MQTT setup
                
                mqtt_publisher = MQTTPublisher("Publisher", config.BROKER, config.BROKER_PORT, config.TOPIC, config.QOS, config.USERNAME, 
                                               config.PASSWORD, config.RECONNECT_CONFIG, gateway.logger, config.RETAIN, use_tls=config.TLS_ENABLED)
                gateway.run(config.NR_OF_MESSAGES, config.PUBLISH_SLEEP_TIME, mqtt_publisher.publish)
            else:
                print(f"Invalid NR_OF_MESSAGES or PUBLISH_SLEEP_TIME: {config.NR_OF_MESSAGES}, {config.PUBLISH_SLEEP_TIME}")
        else:
            # log error
            print("Error: Gateway was not configured correctly")

    except Exception as e:
        logging.error({e})
        sys.exit(1)

    
