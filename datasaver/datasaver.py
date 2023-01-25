import threading
import csv
from queue import Queue
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QLabel, QMessageBox


class DataSaver(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_name = 'fileName'
        self.buffer_size = 2
        self.counter = 0
        self.file = None
        self.writer = None
        self.stop_event = threading.Event()
        self.data_queue = Queue()
        self.thread = threading.Thread(target=self.run, name='DataSaver', daemon=True)
        self.thread.start()

    def run(self):
        while not self.stop_event.is_set():
            while not self.data_queue.empty():
                data = self.data_queue.get()
                self.writer.writerow(data)
                self.counter += 1
                if self.counter >= self.buffer_size:
                    self.counter = 0
                    self.file.flush()
                
    def save_data(self, roll:float, pitch:float, yaw:float):
        self.data_queue.put([roll, pitch, yaw])

    def start(self):
        if self.file is None or self.file.closed:
            self.counter = 0
            self.file = open(self.file_name, 'w', newline='')
            self.writer = csv.writer(self.file)
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