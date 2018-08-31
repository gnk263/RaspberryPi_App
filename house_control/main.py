import os
import configparser
import time
import json
import RPi.GPIO as GPIO
import logging
import parser
from logging import getLogger, Formatter, FileHandler
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

#Use PIN 7 (GPIO 4)
GPIO_AIRCON_PIN = 7

#programme finish trigger file
FINISH_FILE = "finish.txt"

#logger setting
handler_format = Formatter("[%(asctime)s][%(name)s][%(levelname)s] %(message)s")

file_handler = FileHandler("house_control.log", "a")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(handler_format)

logger = getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)


def main():
    logger.info("Start house controller")

    init_gpio()

    (root_ca, private_key, certificate,
        client_id, endpoint, port, topic) = parse_config_file()

    # https://s3.amazonaws.com/aws-iot-device-sdk-python-docs/sphinx/html/index.html
    client = AWSIoTMQTTClient(client_id)
    client.configureEndpoint(endpoint, port)
    client.configureCredentials(root_ca, private_key, certificate)

    client.configureAutoReconnectBackoffTime(1, 32, 20)
    client.configureOfflinePublishQueueing(-1)
    client.configureDrainingFrequency(2)
    client.configureConnectDisconnectTimeout(10)
    client.configureMQTTOperationTimeout(5)

    client.connect()
    client.subscribe(topic, 1, subscribe_callback)

    while True:
        time.sleep(5)

        if is_finish():
            os.remove(FINISH_FILE)
            GPIO.cleanup()
            logger.info("Finish house controller")
            break

def init_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(GPIO_AIRCON_PIN, GPIO.OUT, initial=GPIO.HIGH)

def parse_config_file():
    config = configparser.ConfigParser()
    config.read("config.ini")

    return (
        config["AWS_IOT_CONNECT"]["ROOT_CA"],
        config["AWS_IOT_CONNECT"]["PRIVATE_KEY"],
        config["AWS_IOT_CONNECT"]["CERTIFICATE"],
        config["AWS_IOT_CORE"]["CLIENT_ID"],
        config["AWS_IOT_CORE"]["ENDPOINT"],
        int(config["AWS_IOT_CORE"]["PORT"]),
        config["AWS_IOT_CORE"]["TOPIC"]
    )

def subscribe_callback(client, userdata, message):
    logger.info("Received a new message: ")
    logger.info(message.payload)
    logger.info("from topic: ")
    logger.info(message.topic)

    params = parser.parse_payload(message.payload.decode(encoding="utf-8"))
    logger.info(json.dumps(params, indent=4))

    remote_control(params)

def remote_control(params):
    if params["text"] == "aircon":
        logger.info("Execute GPIO_AIRCON_PIN")
        execute(GPIO_AIRCON_PIN)

def execute(pin_no):
    GPIO.output(pin_no, True)
    time.sleep(0.5)
    GPIO.output(pin_no, False)
    time.sleep(0.5)

def is_finish():
    if os.path.isfile(FINISH_FILE):
        return True
    return False

if __name__ == "__main__":
    main()
