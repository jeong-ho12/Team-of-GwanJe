from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QLabel, QMessageBox
import sys

from .widgethub import Widgethub

class MainWindow(QMainWindow):
    def __init__(self, datahub):
        self.app = QApplication(sys.argv)
        super().__init__()

        self.datahub = datahub
        self.widgethub = Widgethub()

        self.resize(800,600)

        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.stop_button.setEnabled(False)

        self.label = QLabel()
        self.label.setText("Hello")

        layout = QVBoxLayout()
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.label)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)


    def start(self):
        self.show()


    def setEventLoop(self):
        sys.exit(self.app.exec_())
