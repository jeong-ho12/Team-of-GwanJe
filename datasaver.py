import threading
import csv
from queue import Queue

class DataSaver:
    def __init__(self, file_name:str, buffer_size:int):
        self.file_name = file_name
        self.buffer_size = buffer_size
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
                # if self.counter >= self.buffer_size:
                #     self.counter = 0
                #     self.file.flush()
                

    def save_data(self, roll:float, pitch:float, yaw:float):
        self.data_queue.put([roll, pitch, yaw])

    def start(self):
        if self.file is None or self.file.closed:
            self.counter = 0
            self.file = open(self.file_name, 'w', newline='')
            self.writer = csv.writer(self.file)
        else:
            print("Previous file is still open, please close it before opening a new one.")

        if not self.thread.is_alive():
            self.stop_event.clear()
            

    def stop(self):
        self.stop_event.set()

        if not self.data_queue.empty():
            while not self.data_queue.empty():
                data = self.data_queue.get()
                self.writer.writerow(data)
        self.file.close()