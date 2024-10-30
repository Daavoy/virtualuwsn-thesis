import argparse
import logging
import os
import ssl
import time
from pathlib import Path

import paho.mqtt.client as mqtt

from paho.mqtt.enums import MQTTProtocolVersion

from utils.config_utils import getVUWSNConfig
from logging.handlers import TimedRotatingFileHandler

global sub


class Subscriber:

    def __init__(self, id,logfile, addr, port, topic, qos, keep_alive,clean=False,tls=False,topics=0):
        self.id = id
        self.topic = topic
        self.addr = addr
        self.port = port
        self.keep_alive = keep_alive
        self.tls = tls
        self.clean_sesh = clean
        self.logfile = logfile
        self.qos = qos
        self.ntopics=topics

        # setup logging
        formatter = logging.Formatter(fmt='%(asctime)s[%(levelname)s],%(message)s', datefmt="%Y-%m-%dT%H:%M:%S%z")
        self.logger = logging.getLogger("Exec-Log")
        self.logger.setLevel(logging.INFO)

        # Create log path in case it not exists
        path = Path(logfile)
        directory = path.parent.absolute()
        directory.mkdir(parents=True, exist_ok=True)

        handler = TimedRotatingFileHandler(logfile, when="m", interval=60, backupCount=100)

        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.info(f"Subscriber: [Initialized] \n{self}")

    def __str__(self):
        return ''.join((f'MQTT Client Configuration: \n',
                        f'CLIENT_ID: {self.id} \n',
                        f'BROKER_URL: {self.addr}:{self.port} \n',
                        f'TOPIC: {self.topic}:{self.qos} \n',
                        f'CONNECT CONFIG: tls={self.tls}, clean_start={self.clean_sesh}, keepalive={self.keep_alive},'))

    def log(self,mid,send,recv,topic,payload_size,topic_size,index):
        msg = ','.join((mid,str(send),str(recv),topic,str(payload_size),str(topic_size)),index)
        self.logger.info(msg)


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    sub.logger.info(f"Connected with result code {reason_code}")

    if sub.ntopics == 0:
        client.subscribe(sub.topic, qos=sub.qos)
    elif sub.ntopics > 0:
        topics2subscribe = [(get_topic_name(sub.topic,idx), sub.qos) for idx in range(sub.ntopics)]
        client.subscribe(topics2subscribe)


def get_topic_name(prefix: str, i: int):
    return '/'.join((prefix, f'node{str(i + 1)}'))


def on_disconnect(client, userdata, disconnect_flags, reason_code, properties):
    print(f"Disconnected from Broker")
    sub.logger.info("Disconnected from Broker")


def on_message(client, userdata, msg):
    # print(f"Received message: {msg.topic} -> {msg.payload.decode('utf-8')}")
    sub.logger.info(f"Received message on topic: {msg.topic}")
    if not msg.properties.isEmpty():
        if msg.properties.UserProperty[0][0] == 'unique_message_id':
            mid = msg.properties.UserProperty[0][1]  # msg.useuserdata['unique_message_id']
            if msg.properties.UserProperty[1][0] == 'publisher_send_time':
                send_time = float(msg.properties.UserProperty[1][1])  # userdata['publisher_send_time']
                recv_time = time.time() * 1000;  # convert to ms
                if msg.properties.UserProperty[2][0] == 'order':  # userdata['order']
                    order = msg.properties.UserProperty[2][1]
                    sub.log(mid, send_time, recv_time, msg.topic, len(msg.payload), len(msg.topic), order)


def on_subscribe(client, userdata, mid, reason_code_list, properties):
    print(f"Subscribed to MID: {mid} with codes: {reason_code_list}")
    sub.logger.info(f"Subscribed to MID: {mid} with codes: {reason_code_list}")


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description="Provide the log file name")
        parser.add_argument("--logfile", required=True, help="Path to the log file")
        parser.add_argument("--ntopics",type=int, default=0, help="Number of topics to subscribe sequentially")

        # Get VUWSN config
        parser.add_argument("--configfile", required=True, default="configs/config-broker-evaluation.yml",
                            help="Path to the config file")
        args = parser.parse_args()

        if not os.path.exists(args.configfile):
            raise RuntimeError (f"Error: The configfile '{args.configfile}' does not exist.")
        config = getVUWSNConfig(args.configfile)

        lfile = args.logfile
        sub = Subscriber(id=config.MQTT_CONFIG.CONNECT_CONFIG.CLIENT_ID,
                         logfile=lfile, addr=config.MQTT_CONFIG.BROKER_CONFIG.BROKER_URL,
                         port=config.MQTT_CONFIG.BROKER_CONFIG.BROKER_PORT,
                         topic=config.MQTT_CONFIG.BROKER_CONFIG.TOPIC,
                         qos=config.MQTT_CONFIG.BROKER_CONFIG.QOS,
                         keep_alive=config.MQTT_CONFIG.CONNECT_CONFIG.KEEPALIVE,
                         clean=config.MQTT_CONFIG.CONNECT_CONFIG.CLEAN_START,
                         tls=config.MQTT_CONFIG.CONNECT_CONFIG.USE_TLS,
                         topics=args.ntopics)

        # connect and subscribe
        client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, protocol=MQTTProtocolVersion.MQTTv5,
                             client_id=sub.id,reconnect_on_failure=True)
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_disconnect = on_disconnect
        client.on_subscribe = on_subscribe

        if sub.tls:
            if not config.MQTT_CONFIG.CONNECT_CONFIG.CA_CERT:
                client.tls_set()
            else:
                client.tls_set(ca_certs=config.MQTT_CONFIG.CONNECT_CONFIG.CA_CERT)
        username=config.MQTT_CONFIG.BROKER_CONFIG.USERNAME
        pwd=config.MQTT_CONFIG.BROKER_CONFIG.PASSWORD

        client.username_pw_set(username=username, password=pwd)
        client.connect(host=sub.addr, port=sub.port, keepalive=sub.keep_alive,clean_start=sub.clean_sesh)


        client.loop_forever(retry_first_connection=True)

    except KeyboardInterrupt:
        if sub is None:
            print("Exited with KeyboardInterrupt")
        else:
            sub.logger.error("Exited with KeyboardInterrupt")
    except Exception as e:
        if sub is None:
            print(f"Error: {e}")
        else:
            sub.logger.error(f"Error: {e}")
    finally:
        # client.loop_stop()
        client.disconnect()

