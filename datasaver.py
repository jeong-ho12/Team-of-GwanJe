import csv

class DataSaver:
    def __init__(self, file_name:str, buffer_size:int):
        self.file_name = file_name
        self.buffer = []
        self.buffer_size = buffer_size
        self.counter = 0
        self.file = None
        self.writer = None

    def save_data(self, roll:float, pitch:float, yaw:float):
        self.buffer.append([roll, pitch, yaw])
        self.counter += 1
        if self.counter >= self.buffer_size:
            self.writer.writerows(self.buffer)
            self.buffer = []
            self.counter = 0

    def stop(self):
        if self.file is not None:
            if len(self.buffer) > 0:
                self.writer.writerows(self.buffer)
                self.buffer = []
            self.file.close()

    def start(self):
        if self.file is None or self.file.closed:
            self.buffer = []
            self.counter = 0
            self.file = open(self.file_name, 'w', newline='')
            self.writer = csv.writer(self.file)
        else:
            print("Previous file is still open, please close it before opening a new one.")