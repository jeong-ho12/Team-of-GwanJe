import numpy as np

class Datahub:

    def __init__ (self):
        """
        Communication Status Parameter
        """
        self.iscommunication_start = 0
        self.isdatasaver_start = 0
        self.file_Name = 'FileName.csv'
        self.mySerialPort = 'COM8'
        self.serial_port_error=-1
        """
        Rocket Status Parameter
        """
        self.hours = np.empty(0)
        self.mins = np.empty(0)
        self.secs = np.empty(0)
        self.tenmilis = np.empty(0)
        self.rolls = np.empty(0)
        self.pitchs = np.empty(0)
        self.yaws = np.empty(0)
        self.rollSpeeds = np.empty(0)
        self.pitchSpeeds = np.empty(0)
        self.yawSpeeds = np.empty(0)
        self.Xaccels = np.empty(0)
        self.Yaccels = np.empty(0)
        self.Zaccels = np.empty(0)
        self.latitudes = np.empty(0)
        self.longitudes = np.empty(0)
        self.altitude = np.empty(0)
        
        #map view trigger
        self.trigger_python = 0
            
    def communication_start(self):
        self.iscommunication_start=1
        
    def communication_stop(self):
        self.iscommunication_start=0
    
    def check_communication_error(self):
        while True:
            if self.serial_port_error==0 or self.serial_port_error==1:
                return self.serial_port_error
    
    def datasaver_start(self):
        self.isdatasaver_start=1

    def datasaver_stop(self):
        self.isdatasaver_start=0
        
    def update(self,datas):
        """Update Datas received from rocket"""
        
        self.hours = np.append(self.hours,datas[0])
        self.mins = np.append(self.mins,datas[1])
        self.secs = np.append(self.secs,datas[2])
        self.tenmilis = np.append(self.tenmilis,datas[3])
        self.rolls = np.append(self.rolls,datas[4])
        self.pitchs = np.append(self.pitchs,datas[5])
        self.yaws = np.append(self.yaws, datas[6])
        self.rollSpeeds = np.append(self.rollSpeeds, datas[7])
        self.pitchSpeeds = np.append(self.pitchSpeeds, datas[8])
        self.yawSpeeds = np.append(self.yawSpeeds, datas[9])
        self.Xaccels = np.append(self.Xaccels, datas[10])
        self.Yaccels = np.append(self.Yaccels, datas[11])
        self.Zaccels = np.append(self.Zaccels, datas[12])
        self.latitudes = np.append(self.latitudes, datas[13])
        self.longitudes = np.append(self.longitudes, datas[14])
        self.altitude = np.append(self.altitude, datas[15])
