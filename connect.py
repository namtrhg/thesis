import time
import random
import requests
import sys
import json
import paho.mqtt.client as mqtt
import serial
from serialThread import SerialCommunication

# thingsboard cloud server
THINGS_BOARD_HOST = "thingsboard-iot.tk"
THINGS_BOARD_ACCESS_TOKEN = "QgrZZHgdaVX03zwbLQNb"
THINGS_BOARD_PORT = 1883
THINGS_BOARD_INTERVAL_KEEP_ALIVE = 60  # second

INTERVAL = 10
collect_data = {'temperature': 0, 'temperature2': 0}

# Send a command to the micro:bit and show the response


def myfunc(action):
   out = action + "\n"
   out2 = out.encode('utf_8')
   ser.write(out2)
   return ser.readline().decode('utf-8')

def myfunc2(action):
   out = action + "\n"
   out2 = out.encode('utf_8')
   ser2.write(out2)
   return ser.readline().decode('utf-8')


# configure the serial connections (this will differ on your setup)
ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=115200
)

ser2 = serial.Serial(
    port='/dev/ttyACM1',
    baudrate=115200
)


def getDataSerial():
    # TODO: get data
    collect_data['temperature'] = myfunc("T")
    collect_data['temperature2'] = myfunc2("T")


def on_connect(client, userdata, rc, *extra_params):
    print('Connected with result code ' + str(rc))
    client.subscribe('v1/devices/me/rpc/request/+')
    pass


def on_message(client, userdata, msg):
    global serialControl
    # print('Topic: ' + msg.topic + '\nMessage: ' + str(msg.payload))
    try:
        temp_data = json.loads(msg.payload)
        if temp_data['method'] == 'setValueLED':
            client.publish('v1/devices/me/attributes',
                           json.dumps({'valueLED': temp_data['params']}))
            print("Button pressed is: " + str(temp_data['params']))

            # TODO: Add function controll LED ON/OFF
            if temp_data['params'] == True:
                myfunc("1")
            else:
                myfunc("0")
        elif temp_data['method'] == 'setValueLED2':
            client.publish('v1/devices/me/attributes', json.dumps({'valueLED2': temp_data['params']}))
            print("Button pressed is: " + str(temp_data['params']))

            # TODO: Add function controll LED ON/OFF
            if temp_data['params'] == True:
                myfunc("1")
            else:
                myfunc("0")
            # serialControl.write(data)
    except:
        pass


if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(THINGS_BOARD_ACCESS_TOKEN)
    client.connect(THINGS_BOARD_HOST, THINGS_BOARD_PORT, THINGS_BOARD_INTERVAL_KEEP_ALIVE)
    client.loop_start()

    # try:
    #     serialControl = SerialCommunication(serialPort="", baudrate=115200, mqttClient=client)
    #     serialControl.start()
    # except:
    #     print("Cannot open serial port " + serialPort)

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
    # serialControl.stop()
