import paho.mqtt.client as paho
from paho.mqtt.properties import Properties, PacketTypes
from paho.mqtt.client import MQTT_ERR_SUCCESS
from utils.log_utils import getFileHandler
import time

class MQTTPublisher:

    def __init__(self, broker_url, broker_port, topic, qos, username, password):
        self.BROKER_URL = broker_url
        self.BROKER_PORT = broker_port
        self.TOPIC = topic
        self.QOS = qos
        self.USERNAME = username
        self.PASSWORD = password

        # Setup publisher logging
        self.logger = getFileHandler("logs/publisher")

        self.publisher = paho.Client(protocol=paho.MQTTv5)
        self.initPublisher()

        self.log(self.__str__())

    def __str__(self) -> str:
        return ''.join((f'MQTT Publisher Configuration: \n',
                        f'BROKER: {self.BROKER_URL}:{self.BROKER_PORT} \n',
                        f'TOPIC: {self.TOPIC}:{self.QOS}'))

    def log(self, msg: str):
        self.logger.info(msg)

    def initPublisher(self):
        self.publisher.on_publish = self.on_publish
        self.publisher.on_connect = self.on_connect
        self.publisher.on_disconnect = self.on_disconnect
        self.publisher.tls_set(tls_version=paho.ssl.PROTOCOL_TLS)
        self.publisher.username_pw_set(self.USERNAME, self.PASSWORD)

    def on_publish(self, client, userdata, mid):
        self.log(f'Publisher: [on_publish {mid}]')

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            self.log("Publisher: [Connected]")
        else:
            self.log(f"Publisher: [Failed to connect with code: {rc}]")

    def on_disconnect(self, client, userdata, rc, properties=None):
        self.log("Publisher: [Disconnected]")

    def publish(self, data: str, id:int):
        published = False
        self.log("Publisher: [Connecting]")
        self.publisher.connect(host=self.BROKER_URL, port=self.BROKER_PORT)
        if self.publisher.is_connected():
            self.publisher.loop_start()

            # user properties
            publish_properties = Properties(PacketTypes.PUBLISH) 
            publish_properties.UserProperty = ("unique_message_id", str(id)) 
            publish_properties.UserProperty = ("publisher_send_time", str((time.time()*1000)))

            # publish
            result = self.publisher.publish(self.TOPIC, data, self.QOS, False, publish_properties)

            # disconnect if PUBLISH was successfully sent
            if result.rc is MQTT_ERR_SUCCESS or result.is_published():
                result.wait_for_publish(60)
                mid = result.mid
                self.publisher.disconnect()
                published = True
                self.log(f"Publisher: [Published data] \n {data}")

            # otherwise - error handling
            else:
                self.log("Publisher: Error publishing data to broker") 
        else:
            # TODO: try to reconnect?
            self.log("Publisher: Could not publish do to error connecting to broker")

        self.publisher.loop_stop(force=False)
        return published