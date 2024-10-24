import argparse
import logging
from vuwsn import *
from utils.config_utils import *
from gateway import Gateway
from hubnode import HubNode
from mqtt_connector.mqtt.client import MQTTPublisher
from sfisop.datamodels.tsdatamodel.timeseriesdata import Location


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Provide the log file name")

        # Get VUWSN config
        parser.add_argument("--configfile", default="configs/config-broker-evaluation.yml",
                            help="Path to the config file")
        args = parser.parse_args()

        if not os.path.exists(args.configfile):
            raise RuntimeError(f"Error: The configfile '{args.configfile}' does not exist.")
        # Get VUWSN config   
        config = getVUWSNConfig(args.configfile)

        # VUWSN setup
        gateway = None

        if config.TESTDATA_PATH is None or config.TESTDATA_PATH == "":
            sdc = config.SMARTOCEAN_DATA_CONFIG
            if sdc is not None:
                location = Location(latitude=sdc.LOCATION_LATITUDE, longitude=sdc.LOCATION_LONGITUDE)
                vuwsn = SmartOceanVUWSN(description=sdc.DESCRIPTION,format=sdc.FORMAT, origin=sdc.TIMESERIES,
                                        timeseries=sdc.TIMESERIES, source=sdc.SOURCE, source_id=sdc.SOURCE_ID,
                                        location=location)
            else:
                print("Error: No test data path or SmartOcean data configuration found")
        elif not os.path.exists(config.TESTDATA_PATH):
            print(f"Error: The data_path '{config.TESTDATA_PATH}' does not exist.")
        else:
            origin = f"Data File {config.TESTDATA_PATH}"
            vuwsn = FileVUWSN("Data File VUWSN", config.TESTDATA_PATH)

        if not vuwsn.sinks:
            for gateway in vuwsn.sinks:
                if config.NR_OF_MESSAGES >= 0 and config.PUBLISH_INTERVAL >= 0:
                    # MQTT setup
                    mqtt_publisher = MQTTPublisher("Publisher", config.MQTT_CONFIG, gateway.logger)

                    gateway.log(f"Starting publishing {config.NR_OF_MESSAGES} messages with {config.PUBLISH_INTERVAL} second intervals")
                    for i in range(1, config.NR_OF_MESSAGES + 1):
                        gateway.run(mqtt_publisher)

                    time.sleep(config.PUBLISH_INTERVAL)
                else:
                    print(f"Invalid NR_OF_MESSAGES or PUBLISH_INTERVAL: {config.NR_OF_MESSAGES}, {config.PUBLISH_INTERVAL}")
        else:
            # log error
            print("Error: Gateway was not configured correctly")

    except Exception as e:
        logging.error({e})
        sys.exit(1)

    
