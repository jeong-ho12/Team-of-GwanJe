import struct
import serial
import numpy as np
import threading
import time
#from datahub import Datahub

class Receiver(threading.Thread):
    def __init__(self, datahub):
        super().__init__()
        self.count = 0
        self.datahub = datahub
        self.first_time = True
        self.ser = None

        self.n = 0


    def setSerialport(self,myport):
            self.ser = serial.Serial(port=myport,
                                    baudrate = 115200,
                                    parity=serial.PARITY_NONE,
                                    stopbits=serial.STOPBITS_TWO,
                                    bytesize=serial.EIGHTBITS,
                                    timeout=0.1)

    def _decode_data(self, data_bytes):
        decode_data = struct.unpack('>17f', data_bytes)

        if np.sum(decode_data[4:-1])-decode_data[-1]<1:
            all_data = np.around(decode_data,4)
            if len(all_data)>=1:
                self.datahub.update(all_data)

    def run(self):
        while True:
            # try:
                if self.datahub.iscommunication_start:
                        if self.first_time:
                            self.setSerialport(self.datahub.mySerialPort)
                            self.first_time=False

                        self.datahub.serial_port_error=0
                        header1 = self.ser.read(1)

                        if header1 == b'A':
                            header2 = self.ser.read(1)
                            
                            if header2 == b'B':
                                bytes_data = self.ser.read(68)
                                self._decode_data(bytes_data)
                else:
                    time.sleep(0.1)
            # except:
            #     self.datahub.serial_port_error=1


if __name__=="__main__":
    receiver = Receiver()
    receiver.run()