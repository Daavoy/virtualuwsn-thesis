import paho.mqtt.client as paho
from paho.mqtt.client import MQTT_ERR_SUCCESS
from utils.log_utils import getTimedRotatingFileHandler

class MQTTClient:

    def __init__(self, broker_url, broker_port, topic, qos, username, password, logfile):
        self.BROKER_URL = broker_url
        self.BROKER_PORT = broker_port
        self.TOPIC = topic
        self.QOS = qos
        self.USERNAME = username
        self.PASSWORD = password

        # Setup publisher logging
        self.logger = getTimedRotatingFileHandler("MQTT Client Rotating Log", logfile)

        self.log(self.__str__())

    def __str__(self) -> str:
        return ''.join((f'MQTT Client Configuration: \n',
                        f'BROKER: {self.BROKER_URL}:{self.BROKER_PORT} \n',
                        f'TOPIC: {self.TOPIC}:{self.QOS}'))

    def log(self, msg: str):
        self.logger.info(msg)

    def on_publish(self, client, userdata, mid):
        self.log(f'Publisher: [on_publish {mid}]')

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.log("Publisher: [Connected]")
        else:
            self.log(f"Publisher: [Failed to connect with code {rc}]")

    def on_disconnect(self, client, userdata, rc):
        self.log("Publisher: [Disconnected]")

    def publish(self, data: str):
        client = paho.Client()
        client.on_publish = self.on_publish
        client.on_connect = self.on_connect
        client.on_disconnect = self.on_disconnect
        client.tls_set(tls_version=paho.ssl.PROTOCOL_TLS)
        client.username_pw_set(self.USERNAME, self.PASSWORD)

        self.log("Publisher: [Connecting]")
        client.connect(host=self.BROKER_URL, port=self.BROKER_PORT)
        client.loop_start()

        # publish
        result = client.publish(self.TOPIC, data, self.QOS, True) 
        published = False

        # disconnect if PUBLISH was successfully sent
        if result.rc is MQTT_ERR_SUCCESS or result.is_published():
            result.wait_for_publish(60)
            mid = result.mid
            client.disconnect()
            published = True
            self.log(f"Publisher: [Published data] \n {data}")

        # otherwise - error handling
        else:
            self.log("Publisher: Error publishing data to broker")  # revert start time

        client.loop_stop(force=False)
        return published