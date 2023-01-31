import struct
import serial
import numpy as np
import threading
#from datahub import Datahub

class Receiver(threading.Thread):
    def __init__(self, datahub):
        super().__init__()
        self.count = 0
        self.datahub = datahub
        self.first_time = True
        self.ser = None

    def _decode_data(self, time_bytes, data_bytes):
        time = struct.unpack('>4f', time_bytes)
        decodetime = tuple(np.around(np.array(time, dtype=float),1))
        decode_data = struct.unpack('>13f', data_bytes)
        if abs(sum(decode_data[:-1])-decode_data[-1])<1:
            angular_data = np.around(decode_data[:12],4)
            tude_data = np.around(decode_data[9:12],4)
            processed_data = np.concatenate((angular_data, tude_data),axis=0)
            alldata = np.concatenate((decodetime, processed_data),axis=0)
            return alldata

    def setSerialport(self,myport):
            self.ser = serial.Serial(port=myport,
                                    baudrate = 9600,
                                    parity=serial.PARITY_NONE,
                                    stopbits=serial.STOPBITS_TWO,
                                    bytesize=serial.EIGHTBITS,
                                    timeout=0.2)

    def run(self):
        while True:
            if self.datahub.iscommunication_start:

                        if self.first_time:
                            self.setSerialport(self.datahub.mySerialPort)
                            self.first_time=False

                        self.datahub.serial_port_error=0
                        header1 = self.ser.read(1)

                        if header1 == b'A':
                            header2 = self.ser.read(1)
                            
                            if header2 == b'B':
                                time_bytes = self.ser.read(16)
                                data_bytes = self.ser.read(52)
                                data = self._decode_data(time_bytes, data_bytes)
                                if data is not None:
                                    self.datahub.update(data)
         

if __name__=="__main__":
    receiver = Receiver()
    receiver.run()