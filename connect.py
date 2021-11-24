import time
import random
import requests
import sys
import json
import paho.mqtt.client as mqtt

#weather api
API_KEYS = "57ccdbff495327ee0af0a61933a6b5ae"
HO_CHI_MINH_ID = "1566083"
URL = "http://api.openweathermap.org/data/2.5/weather?"

#thingsboard cloud server
THINGS_BOARD_HOST = "thingsboard-iot.tk"
THINGS_BOARD_DEVICE_ID_1 = "50417170-2088-11ec-ad64-fdd28235c473"
THINGS_BOARD_ACCESS_TOKEN_1 = "QgrZZHgdaVX03zwblQNb"
THINGS_BOARD_PORT = 1883
THINGS_BOARD_INTERVAL_KEEP_ALIVE = 60 #second

INTERVAL = 60
collect_data = {'temperature': 0, 'humidity': 0, 'winspeed': 0}
collect_data_1 = {'temperature': 0, 'humidity': 0, 'winspeed': 0, 'deviceNo': 1}
collect_data_2 = {'temperature': 0, 'humidity': 0, 'winspeed': 0, 'deviceNo': 2}
collect_data_3 = {'temperature': 0, 'humidity': 0, 'winspeed': 0, 'deviceNo': 3}

FULL_URL = URL + "id=" + HO_CHI_MINH_ID + "&appid=" + API_KEYS

def randValue(scale = 0):
    temp = random.random()
    if temp >= 0.5:
        temp = temp - 0.5
    return temp*scale

def getWeatherValue():
    response = requests.get(FULL_URL)
    data = response.json()
    collect_data['temperature'] = round(data["main"]["temp"] - 273, 0)
    collect_data['humidity'] = round(data["main"]["humidity"], 0)
    collect_data['winspeed'] = round(data["wind"]["speed"], 0)

    collect_data_1['temperature'] = collect_data['temperature'] + randValue()
    collect_data_1['humidity'] = collect_data['humidity'] + randValue()
    collect_data_1['winspeed'] = collect_data['winspeed'] + randValue()
    collect_data_2['temperature'] = collect_data['temperature'] + randValue(5)
    collect_data_2['humidity'] = collect_data['humidity'] - randValue(3)
    collect_data_2['winspeed'] = collect_data['winspeed'] + randValue(1)
    collect_data_3['temperature'] = collect_data['temperature'] - randValue(5)
    collect_data_3['humidity'] = collect_data['humidity'] - randValue(6)
    collect_data_3['winspeed'] = collect_data['winspeed'] - randValue(1)

def on_connect(client, userdata, rc, *extra_params):
    # print('Connected with result code ' + str(rc))
    pass


def on_message(client, userdata, msg):
    print("Receive message: ", msg.payload)


if __name__ == '__main__':
    client1 = mqtt.Client()
    client2 = mqtt.Client()
    client3 = mqtt.Client()
    client1.on_connect = on_connect
    client2.on_connect = on_connect
    client3.on_connect = on_connect
    client1.on_message = on_message
    client2.on_message = on_message
    client3.on_message = on_message
    client1.username_pw_set(THINGS_BOARD_ACCESS_TOKEN_1)
    client2.username_pw_set(THINGS_BOARD_ACCESS_TOKEN_2)
    client3.username_pw_set(THINGS_BOARD_ACCESS_TOKEN_3)
    client1.connect(THINGS_BOARD_HOST, THINGS_BOARD_PORT, THINGS_BOARD_INTERVAL_KEEP_ALIVE)
    client2.connect(THINGS_BOARD_HOST, THINGS_BOARD_PORT, THINGS_BOARD_INTERVAL_KEEP_ALIVE)
    client3.connect(THINGS_BOARD_HOST, THINGS_BOARD_PORT, THINGS_BOARD_INTERVAL_KEEP_ALIVE)
    client1.loop_start()
    client2.loop_start()
    client3.loop_start()

    try:
        while True:
            getWeatherValue()
            print("Sending data")
            client1.publish('v1/devices/me/telemetry', json.dumps(collect_data_1), 1)
            client2.publish('v1/devices/me/telemetry', json.dumps(collect_data_2), 1)
            client3.publish('v1/devices/me/telemetry', json.dumps(collect_data_3), 1)
            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        pass

    client1.loop_stop()
    client2.loop_stop()
    client3.loop_stop()
    client1.disconnect()
    client3.disconnect()
    client3.disconnect()
