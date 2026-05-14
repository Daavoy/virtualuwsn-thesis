import argparse
import copy
import logging
import os
import sys
import time

from vuwsn import *
from utils.config_utils import *
from gateway import Gateway
from hubnode import HubNode
from mqtt_connector.mqtt.client import MQTTPublisher
from sfisop.datamodels.tsdatamodel.timeseriesdata import Location


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Provide the log file name")

        parser.add_argument(
            "--configfile",
            default="configs/config-broker-evaluation.yml",
            help="Path to the config file"
        )
        args = parser.parse_args()

        if not os.path.exists(args.configfile):
            raise RuntimeError(f"Error: The configfile '{args.configfile}' does not exist.")

        config = getVUWSNConfig(args.configfile)

        if config.TESTDATA_PATH is None or config.TESTDATA_PATH == "":
            sdc = config.SMARTOCEAN_DATA_CONFIG
            if sdc is not None:
                location = Location(
                    latitude=sdc.LOCATION_LATITUDE,
                    longitude=sdc.LOCATION_LONGITUDE
                )
                vuwsn = SmartOceanVUWSN(
                    description=sdc.DESCRIPTION,
                    format=sdc.FORMAT,
                    origin=sdc.TIMESERIES,
                    timeseries=sdc.TIMESERIES,
                    source=sdc.SOURCE,
                    source_id=sdc.SOURCE_ID,
                    location=location
                )
            else:
                raise RuntimeError("Error: No test data path or SmartOcean data configuration found")
        elif not os.path.exists(config.TESTDATA_PATH):
            raise RuntimeError(f"Error: The data_path '{config.TESTDATA_PATH}' does not exist.")
        else:
            origin = f"Data File {config.TESTDATA_PATH}"
            vuwsn = FileVUWSN(origin, config.TESTDATA_PATH)

        if vuwsn.sinks:
            id_prefix = config.MQTT_CONFIG.CONNECT_CONFIG.CLIENT_ID
            user_prefix = config.MQTT_CONFIG.BROKER_CONFIG.USERNAME
            topic_prefix = (config.MQTT_CONFIG.BROKER_CONFIG.TOPIC or "").rstrip("/")

            if config.NR_OF_MESSAGES >= 0 and config.PUBLISH_INTERVAL >= 0:
                for i in range(1, config.NR_OF_MESSAGES + 1):
                    for gateway in vuwsn.sinks:
                        gateway_config = copy.deepcopy(config.MQTT_CONFIG)

                        gateway_parts = gateway.name.split(".")
                        gateway_leaf = gateway_parts[-1]  # gateway1

                        # Unique client id per gateway
                        if id_prefix and id_prefix != "":
                            gateway_config.CONNECT_CONFIG.CLIENT_ID = f"{id_prefix}.{gateway_leaf}"
                        else:
                            gateway_config.CONNECT_CONFIG.CLIENT_ID = gateway.name

                        # Username fallback only if not provided
                        if not user_prefix or user_prefix == "":
                            gateway_config.BROKER_CONFIG.USERNAME = gateway.name

                        # Gateway-level topic prefix, hub suffix added in Gateway.run()
                        gateway_config.BROKER_CONFIG.TOPIC = "/".join(
                            part for part in [topic_prefix, gateway_leaf] if part
                        )

                        mqtt_publisher = MQTTPublisher("Publisher", gateway_config, gateway.logger)

                        gateway.log(
                            f"Starting publishing {config.NR_OF_MESSAGES} messages "
                            f"with {config.PUBLISH_INTERVAL} second intervals"
                        )
                        gateway.run(mqtt_publisher, i)
                        mqtt_publisher.stop()

                    time.sleep(config.PUBLISH_INTERVAL)
            else:
                raise RuntimeError(
                    f"Invalid NR_OF_MESSAGES or PUBLISH_INTERVAL: "
                    f"{config.NR_OF_MESSAGES}, {config.PUBLISH_INTERVAL}"
                )
        else:
            raise RuntimeError("Error: Gateway was not configured correctly")

    except Exception as e:
        import traceback
        traceback.print_exc()
        logging.error(str(e))
        sys.exit(1)