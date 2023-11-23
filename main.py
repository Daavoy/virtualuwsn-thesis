import sys
from decouple import config
import os

from mqttclient import MQTTPublisher
from gateway import Gateway
from datamodels.timeseriesdata import Location
from virtualhubnode import VirtualSensorHubNode
from hubnode import DataFileHubNode

if __name__ == "__main__":
    # Get environment variables
    try:
        BROKER_URL = config('BROKER_URL')
        TOPIC = config('TOPIC')
        USERNAME = config('BROKER_USERNAME')
        PASSWORD = config('BROKER_PASSWORD')

        try:
            NR_OF_MESSAGES = config('NR_OF_MESSAGES', cast=int)
            PUBLISH_SLEEP_TIME = config('PUBLISH_SLEEP_TIME', cast=int)
            BROKER_PORT = config('BROKER_PORT', cast=int)
            QOS = config('QOS', cast=int)
        except ValueError as e:
            print(f"Value error when casting environment variable to int: {e}")
            sys.exit(1) 
    except Exception as e:
        print(f"Error when reading environment variables: {e}")
        sys.exit(1)

    # MQTT setup
    mqtt_publisher = MQTTPublisher(BROKER_URL, BROKER_PORT, TOPIC, QOS, USERNAME, PASSWORD, "logs/publisher.log")

    # VUWSN setup
    gateway = None

    TESTDATA_PATH = config("TESTDATA_PATH", default="") # Path to test data files, if omitted the simulator will generate custom test data in SmartOcean format

    if TESTDATA_PATH is None or TESTDATA_PATH == "":
        location = Location(latitude=60.3692257067, longitude=5.3505234505, elevation=0)
        node = VirtualSensorHubNode("Virtual Sensor Node", location)
        gateway = Gateway("Virtual Gateway", node)
    elif not os.path.exists(TESTDATA_PATH):
        print(f"Error: The data_path '{TESTDATA_PATH}' does not exist.")
    else:
        origin = f"Data File Node {TESTDATA_PATH}"
        node = DataFileHubNode("Simulated data from data files", origin, origin, TESTDATA_PATH)
        gateway = Gateway(f"Data File Gateway {TESTDATA_PATH}", node)
    
    if gateway is not None:
        if NR_OF_MESSAGES >= 0 and PUBLISH_SLEEP_TIME >= 0:
                gateway.run(NR_OF_MESSAGES, PUBLISH_SLEEP_TIME, mqtt_publisher.publish)
        else:
            print(f"Invalid NR_OF_MESSAGES or PUBLISH_SLEEP_TIME: {NR_OF_MESSAGES}, {PUBLISH_SLEEP_TIME}")
    else:
        # log error
        print("Error: Gateway was not configured correclty")
