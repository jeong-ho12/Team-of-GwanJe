import struct
import serial
import numpy as np
import threading

class Receiver(threading.Thread):
    def __init__(self,datahub):
        super().__init__()

        self.ser = serial.Serial(port='COM4',
                    baudrate = 9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_TWO,
                    bytesize=serial.EIGHTBITS,
                    timeout=2)
        self.datahub = datahub

    def run(self):
        while True:
            data = self.ser.read(60)
            if data[:4] == b'?/': #header
                if data[4:8] == b'adsf':
                    decodeData = struct.unpack('>13f', data[8:])

                    if abs(sum(decodeData[:-1])-decodeData[-1])<1:
                        alldata = np.around(decodeData[:-1],4)
                        alldata = alldata[1:]
                        self.datahub.update(alldata)

                        print(alldata)

    def start():
        pass
    
if __name__=="__main__":
    reciver = Receiver()
    reciver.run()