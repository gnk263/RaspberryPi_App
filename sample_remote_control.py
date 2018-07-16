import configparser
import time
import json
import RPi.GPIO as GPIO
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

#Use PIN 7 (GPIO 4)
GPIO_AIRCON_PIN = 7

def main():
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

def init_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(GPIO_AIRCON_PIN, GPIO.OUT)

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
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)

    params = parse_payload(message.payload.decode(encoding="utf-8"))
    print(json.dumps(params, indent=4))

    print("--------------\n\n")

def parse_payload(payload):
    params = {}
    key_value_list = payload.split("&")
    for item in key_value_list:
        (key, value) = item.split("=")
        params[key] = value
    return params

if __name__ == "__main__":
    main()
