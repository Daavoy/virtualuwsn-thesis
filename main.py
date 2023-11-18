import sys
from decouple import config

from mqttclient import MQTTClient
from gateway import Gateway
from datamodels.timeseriesdata import Location
from virtualhubnode import VirtualSensorHubNode


if __name__ == "__main__":
    # Get environment variables
    env_vars = ['BROKER_URL', 'BROKER_PORT', 'TOPIC', 'QOS', 'BROKER_USERNAME', 'BROKER_PASSWORD', 'NR_OF_MESSAGES', 'PUBLISH_SLEEP_TIME'] 
    missing_vars = [var for var in env_vars if config(var) is None]

    if missing_vars:
        print(f"Missing required environment variables: {', '.join(missing_vars)}")
        sys.exit(1)

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

    # MQTT setup
    mqtt_publisher = MQTTClient(BROKER_URL, BROKER_PORT, TOPIC, QOS, USERNAME, PASSWORD, "publisher.log")

    # VUWSN setup
    location = Location(latitude=60.3692257067, longitude=5.3505234505, elevation=0)
    node = VirtualSensorHubNode("Virtual Sensor Node", location)
    gateway = Gateway("Virtual Gateway", node)

    if NR_OF_MESSAGES >= 0 and PUBLISH_SLEEP_TIME >= 0:
            gateway.run(NR_OF_MESSAGES, PUBLISH_SLEEP_TIME, mqtt_publisher.publish)
    else:
        print(f"Invalid NR_OF_MESSAGES or PUBLISH_SLEEP_TIME: {NR_OF_MESSAGES}, {PUBLISH_SLEEP_TIME}")







