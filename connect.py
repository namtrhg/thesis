import time
import random
import requests
import sys
import json
import paho.mqtt.client as mqtt

#thingsboard cloud server
THINGS_BOARD_HOST = "thingsboard-iot.tk"
THINGS_BOARD_ACCESS_TOKEN = "QgrZZHgdaVX03zwbLQNb"
THINGS_BOARD_PORT = 1883
THINGS_BOARD_INTERVAL_KEEP_ALIVE = 60 #second

INTERVAL = 10
collect_data = {'temperature': 0, 'humidity': 0, 'winspeed': 0}

def getDataSerial():
    # TODO: get data
    collect_data['temperature'] = random.randint(0, 100)
    collect_data['humidity'] = random.randint(0, 100)
    collect_data['winspeed'] = random.randint(0, 100)

def on_connect(client, userdata, rc, *extra_params):
    print('Connected with result code ' + str(rc))
    client.subscribe('v1/devices/me/rpc/request/+')
    pass



def on_message(client, userdata, msg):
    # print('Topic: ' + msg.topic + '\nMessage: ' + str(msg.payload))
    try:
        temp_data = json.loads(msg.payload)
        if temp_data['method'] == 'setValueLED':
            client.publish('v1/devices/me/attributes', json.dumps({'valueLED': temp_data['params']}))
            print("Button pressed is: " + str(temp_data['params']))
    except:
        pass


if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(THINGS_BOARD_ACCESS_TOKEN)
    client.connect(THINGS_BOARD_HOST, THINGS_BOARD_PORT, THINGS_BOARD_INTERVAL_KEEP_ALIVE)
    client.loop_start()

    try:
        while True:
            getDataSerial()
            print("Sending data")
            client.publish('v1/devices/me/telemetry', json.dumps(collect_data), 1)
            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        pass

    client.loop_stop()
    client.disconnect()
