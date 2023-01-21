import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QLabel, QMessageBox
from datasaver import DataSaver

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.event_loop_running = False
        self.data_saver = DataSaver("data.csv", 10)
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.add_button = QPushButton("Add Data")
        self.stop_button.setEnabled(False)
        self.add_button.setEnabled(False)

        self.roll_edit = QLineEdit()
        self.pitch_edit = QLineEdit()
        self.yaw_edit = QLineEdit()
        self.file_name_edit = QLineEdit()
        
        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)
        self.add_button.clicked.connect(self.add_data)

        layout = QVBoxLayout()
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.add_button)
        layout.addWidget(self.roll_edit)
        layout.addWidget(self.pitch_edit)
        layout.addWidget(self.yaw_edit)
        layout.addWidget(QLabel("Enter the file name:"))
        layout.addWidget(self.file_name_edit)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def start(self):
        filename = self.file_name_edit.text()
        if filename and not os.path.isfile(filename):
            self.data_saver.file_name = filename
            self.data_saver.start()
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.add_button.setEnabled(True)
        else:
            if not filename:
                QMessageBox.warning(self, "Warning", "Please Enter a file name.")
            else:
                QMessageBox.warning(self, "Warning", "File already exist, please enter different name")


    def stop(self):
        self.data_saver.stop()
        self.stop_button.setEnabled(False)
        self.start_button.setEnabled(True)
        self.add_button.setEnabled(False)
        self.event_loop_running = False

    def add_data(self):
        roll = self.roll_edit.text()
        pitch = self.pitch_edit.text()
        yaw = self.yaw_edit.text()

        if roll == "":
            roll = "empty"
        elif not roll.isnumeric():
            roll = "Non Numeric Values"
        else:
            roll = float(roll)
        if pitch == "":
            pitch = "empty"
        elif not pitch.isnumeric():
            pitch = "Non Numeric Values"
        else:
            pitch = float(pitch)
        if yaw == "":
            yaw = "empty"
        elif not yaw.isnumeric():
            yaw = "Non Numeric Values"
        else:
            yaw = float(yaw)
            
        self.data_saver.save_data(roll, pitch, yaw)

    def closeEvent(self, event):
        self.data_saver.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()

    sys.exit(app.exec_())
