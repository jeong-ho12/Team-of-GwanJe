import threading
import csv
from queue import Queue
import time
import numpy as np

class DataSaver:
    def __init__(self, datahub):

        self.datahub = datahub
        self.buffer_size = 2
        self.counter = 0
        self.file = None
        self.writer = None
        self.saverows = 0

                
    def save_data(self):
        while self.datahub.isdatasaver_start:
            lineRemain = len(self.datahub.altitude) - self.saverows
            if lineRemain > 0:
                data = np.vstack((self.datahub.hours[self.saverows:self.saverows+lineRemain],
                                  self.datahub.mins[self.saverows:self.saverows+lineRemain],
                                  self.datahub.secs[self.saverows:self.saverows+lineRemain],
                                  self.datahub.tenmilis[self.saverows:self.saverows+lineRemain],
                                  self.datahub.rolls[self.saverows:self.saverows+lineRemain],
                                  self.datahub.pitchs[self.saverows:self.saverows+lineRemain],
                                  self.datahub.yaws[self.saverows:self.saverows+lineRemain],
                                  self.datahub.rollSpeeds[self.saverows:self.saverows+lineRemain],
                                  self.datahub.pitchSpeeds[self.saverows:self.saverows+lineRemain],
                                  self.datahub.yawSpeeds[self.saverows:self.saverows+lineRemain],
                                  self.datahub.Xaccels[self.saverows:self.saverows+lineRemain],
                                  self.datahub.Yaccels[self.saverows:self.saverows+lineRemain],
                                  self.datahub.Zaccels[self.saverows:self.saverows+lineRemain],
                                  self.datahub.latitudes[self.saverows:self.saverows+lineRemain],
                                  self.datahub.longitudes[self.saverows:self.saverows+lineRemain],
                                  self.datahub.altitude[self.saverows:self.saverows+lineRemain]))

                for i in range(lineRemain):
                    self.writer.writerow(data[:,i],)
                self.file.flush()
                self.saverows += lineRemain


                
    def start(self):
        while True:

            if self.datahub.isdatasaver_start:
                if self.file is None or self.file.closed:
                    self.counter = 0
                    self.file = open(self.datahub.file_Name, 'w', newline='')

                    self.writer = csv.writer(self.file)
                    self.writer.writerow(["Hours","Minute","Second","10milis","Roll","Pitch","Yaw","RollSpeed","PitchSpeed","YawSpeed","Xaccel","Yaccel","Zaccel","longitude","latitude","altitude"])
                    self.save_data()
                    self.stop()
                else:
                    pass
            time.sleep(0.1)
            
                
    def stop(self):
        if self.file != None and not self.file.closed:
            self.file.close()