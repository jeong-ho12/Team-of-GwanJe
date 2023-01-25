
import threading
import sys

from datasaver.datasaver import DataSaver
from receiver.receiver   import Receiver
from datahub import Datahub
from mainWindow.mainWindow import MainWindow

class Master():
  
    def __init__(self):
        
        self.datahub = Datahub()
        self.datasaver = DataSaver(self.datahub)
        self.receiver = Receiver(self.datahub)
        self.mainWindow = MainWindow(self.datahub)
        
        
        
    def run(self, isDatasaver, isReceiver):

        self.receiver.start()
        self.mainWindow.start()







        self.mainWindow.setEventLoop()

    def update(self):


if __name__ == "__main__":
    master = Master()
    master.run(isDatasaver=1,
               isReceiver=1)