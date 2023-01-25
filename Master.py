
import threading
import sys

from datasaver.datasaver import DataSaver
from receiver.receiver   import Receiver
from datahub import Datahub
from mainWindow.mainWindow import MainWindow

class Thread_Receiver(threading.Thread):
    def __init__(self):
        super().__init__()
    
    def run(self):
        receiver = Receiver()
        receiver.start()

class Thread_DataSaver(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        datasaver = DataSaver()
        datasaver.start()

class Master:
  
    def __init__(self,myport):
        
        self.datahub = Datahub()
        self.mainWindow = MainWindow(self.datahub)
        self.datasaver = Thread_DataSaver(self.datahub)
        self.receiver = Thread_Receiver(myport,self.datahub)
        
        
    def run(self, isDatasaver, isReceiver):

        self.receiver.start()
        self.datasaver.start()
        self.mainWindow.start()        

        
        self.mainWindow.setEventLoop()


if __name__ == "__main__":
    master = Master(myport='COM8')

    master.run(isDatasaver=1,
               isReceiver=1)