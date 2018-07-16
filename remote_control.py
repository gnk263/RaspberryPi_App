import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

CLIENT_ID = "test_client_id"
ENDPOINT = "xxxxxxx.iot.ap-northeast-1.amazonaws.com"
PORT = 8883

ROOT_CA = "./cert/root_ca.pem"
PRIVATE_KEY = "./cert/private.pem.key"
CERTIFICATE = "./cert/certificate.pem.crt.txt"

TOPIC = "raspberry_pi/test"

def main():
    # https://s3.amazonaws.com/aws-iot-device-sdk-python-docs/sphinx/html/index.html
    client = AWSIoTMQTTClient(CLIENT_ID)
    client.configureEndpoint(ENDPOINT, PORT)
    client.configureCredentials(ROOT_CA, PRIVATE_KEY, CERTIFICATE)

    client.configureAutoReconnectBackoffTime(1, 32, 20)
    client.configureOfflinePublishQueueing(-1)
    client.configureDrainingFrequency(2)
    client.configureConnectDisconnectTimeout(10)
    client.configureMQTTOperationTimeout(5)

    client.connect()
    client.subscribe(TOPIC, 1, subscribe_callback)

    while True:
        time.sleep(5)

def subscribe_callback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")


if __name__ == "__main__":
    main()
