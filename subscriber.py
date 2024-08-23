import argparse
import logging
import time

import paho.mqtt.client as mqtt

from utils.config_utils import getVUWSNConfig
from logging.handlers import TimedRotatingFileHandler


class Subscriber:

    def __init__(self, logfile, addr, port, topic, keep_alive,clean=False,tls=False):
        self.topic = topic
        self.addr = addr
        self.port = port
        self.keep_alive = keep_alive
        self.tls = tls
        self.clean_sesh = clean
        self.logfile = logfile

        # setup logging
        formatter = logging.Formatter(fmt='%(asctime)s[%(levelname)s],%(message)s', datefmt="%Y-%m-%dT%H:%M:%S%z")
        self.logger = logging.getLogger("latency-Log")
        self.logger.setLevel(logging.INFO)

        handler = TimedRotatingFileHandler(logfile, when="m", interval=30, backupCount=5)

        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log(self,mid,send,recv,topic):
        msg = ','.join((mid,send,recv,topic))
        self.logger.info(msg)

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        print(f"Received message: {msg.topic} -> {msg.payload.decode('utf-8')}")
        mid = userdata['unique_message_id']
        send_time = userdata['publisher_send_time']
        recv_time = time.time() * 1000;  # convert to ms
        self.log(mid,send_time,recv_time,msg.topic)


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description="Provide the log file name")
        parser.add_argument("--logfile", required=True, help="Path to the log file")
        args = parser.parse_args()
        lfile = args.logfile

        # Get VUWSN config
        config = getVUWSNConfig()

        sub = Subscriber(lfile, config.MQTT_CONFIG.BROKER_CONFIG.BROKER_URL,config.MQTT_CONFIG.BROKER_CONFIG.TOPIC,
                         config.MQTT_CONFIG.BROKER_CONFIG.QOS,config.MQTT_CONFIG.CONNECT_CONFIG.KEEPALIVE,
                         config.MQTT_CONFIG.CONNECT_CONFIG.CLEAN_START)

        # connect and subscribe
        client = mqtt.Client()
        client.on_connect = sub.on_connect
        client.on_message = sub.on_message

        client.connect(sub.addr, sub.port, sub.keep_alive)

        client.loop_start()
        while True:
            pass
    except KeyboardInterrupt:
        print("Exited with KeyboardInterrupt")
    finally:
        client.loop_stop()
        client.disconnect()

