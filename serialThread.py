import serial
from threading import Thread
import time, re

class SerialCommunication(Thread):
    def __init__(self, serialPort, baudrate, mqttClient):
        Thread.__init__(self)
        self._stopev = False

        if serialport is not None:
            self._serialport = serialport

        if baudrate is None:
            self._baudrate = 115200
        else:
            self._baudrate = baudrate

        self.client = mqttClient
        self._serial = serial.Serial(self._serialport, self._baudrate)

    @property
    def serialport(self):
        return self._serialport

    @property
    def baudrate(self):
        return self._baudrate

    def readline(self):
        return self._serial.readline()

    def read(self):
        return self._serial.read()

    def readLength(self, length):
        return self._serial.read(length)

    def open(self):
        return self._serial.open()

    def close(self):
        return self._serial.close()
    
    def isOpen(self):
        return self._serial.isOpen()

    def stop(self):
        self._stopev = True

    def write(self, data):
        self._serial.write(str.encode(data, 'utf-8'))

    def inWaiting(self):
        self._serial.inWaiting()

    def flushInput(self):
        self._serial.flushInput()

    def flushOutput(self):
        self._serial.flushOutput()

    def doRead(self,term):
        matcher = re.compile(term)
        tic = time.time()
        buff = self._serial.read(1)
        while ((time.time() - tic) < self._readtimeout) and (not matcher.search(buff)):
            buff += self._serial.read(1)
        return buff[:len(buff)-1]

    def run(self):
        try:
            self.open()
        except Exception:
            pass 
        
        self._serial.flushInput()
        self._serial.flushOutput()
        
        _data = {'temperature': 0, 'humidity': 0, 'winspeed': 0}

        while not self._stopev:
            _res = str(self.doRead(b'!'), 'utf-8')
            print(_res)
            
            if _res is not None:
                # TODO
                # Parse data from Microbit
                _data['temperature'] = random.randint(0, 100)
                _data['humidity'] = random.randint(0, 100)
                _data['winspeed'] = random.randint(0, 100)

                # Send data to Thingsboard
                self.client.publish('v1/devices/me/telemetry', json.dumps(_data), 1)
        
        self.close()