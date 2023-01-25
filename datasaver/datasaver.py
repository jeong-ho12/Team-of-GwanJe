import threading
import csv
from queue import Queue
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QLabel, QMessageBox


class DataSaver(QMainWindow):
    def __init__(self, datahub):
        super().__init__()
        self.datahub = datahub
        self.file_name = 'fileName'
        self.buffer_size = 2
        self.counter = 0
        self.file = None
        self.writer = None
        self.saverows = 0
        self.stop_event = threading.Event()
        self.data_queue = Queue()
        self.thread = threading.Thread(target=self.saver, name='DataSaver', daemon=True)
        self.thread.start()

    def saver(self):
        while not self.stop_event.is_set():
            while not self.data_queue.empty():
                data = self.data_queue.get()
                self.writer.writerow(data)
                self.counter += 1
                if self.counter >= self.buffer_size:
                    self.counter = 0
                    self.file.flush()
                
    def save_data(self):
        lineRemain = len(self.datahub.timespace) - self.saverows
        if lineRemain > 0:
            for i in range(lineRemain-1):
                self.data_queue.put([self.datahub.timespace[self.saverows+i]])
            self.saverows += lineRemain
            print("Wait for data")


    def start(self):
        if self.file is None or self.file.closed:
            self.counter = 0
            self.file = open(self.file_name, 'w', newline='')
            QMessageBox.warning(self, "Warning", "File is Opened.")
            self.writer = csv.writer(self.file)
            self.save_data()
        else:
            QMessageBox.warning(self, "Warning", "Previous file is still open, please close it before opening a new one.")

        if not self.thread.is_alive():
            self.stop_event.clear()
        
            


    def stop(self):
        self.stop_event.set()

        if not self.data_queue.empty():
            while not self.data_queue.empty():
                data = self.data_queue.get()
                self.writer.writerow(data)
        if self.file != None and not self.file.closed:
            self.file.close()
            QMessageBox.warning(self, "Warning", "File Closed.")