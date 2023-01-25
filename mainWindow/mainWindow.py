from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QLabel, QMessageBox
import sys

from .widgethub import Widgethub

class MainWindow(QMainWindow):
    def __init__(self, datahub):
        self.app = QApplication(sys.argv)
        super().__init__()

        self.widgethub = Widgethub()
        self.datahub = datahub

        central_widget = QWidget()
        self.setCentralWidget(central_widget)


    def start(self):
        self.show()


    def setEventLoop(self):
        sys.exit(self.app.exec_())
