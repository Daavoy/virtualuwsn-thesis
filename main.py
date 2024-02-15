import sys
import os
import logging

sys.path.append(os.path.abspath("../"))
from mqtt_connector.mqtt_client import MQTTPublisher

from gateway import Gateway
from datamodels.timeseriesdata import Location
from hubnode import HubNode
from vuwsn import *
from utils.config_utils import *

if __name__ == "__main__":
    try:
        # Get VUWSN config   
        config = getVUWSNConfig()

        # VUWSN setup
        gateway = None

        if config.TESTDATA_PATH is None or config.TESTDATA_PATH == "":
            sdc = config.SMARTOCEAN_DATA_CONFIG
            if sdc is not None:
                location = Location(latitude=sdc.LOCATION_LATITUDE, longitude=sdc.LOCATION_LONGITUDE)
                vuwsn = TempCondBattVUWSN(description=sdc.DESCRIPTION,format=sdc.FORMAT, origin=sdc.TIMESERIES, timeseries=sdc.TIMESERIES, 
                                          source=sdc.SOURCE, source_id=sdc.SOURCE_ID, location=location)
                node = HubNode(sdc.DESCRIPTION, sdc.TIMESERIES, vuwsn)
                gateway = Gateway("Virtual SmartOcean Gateway", [node])
            else:
                print("Error: No test data path or SmartOcean data configuration found")
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
                mqtt_publisher = MQTTPublisher("Publisher", config.BROKER_CONFIG, config.CONNECT_CONFIG, config.REATTEMPT_CONFIG, 
                                               gateway.logger, config.RETAIN)
                gateway.run(config.NR_OF_MESSAGES, config.PUBLISH_SLEEP_TIME, mqtt_publisher)
            else:
                print(f"Invalid NR_OF_MESSAGES or PUBLISH_SLEEP_TIME: {config.NR_OF_MESSAGES}, {config.PUBLISH_SLEEP_TIME}")
        else:
            # log error
            print("Error: Gateway was not configured correctly")

    except Exception as e:
        logging.error({e})
        sys.exit(1)

    
