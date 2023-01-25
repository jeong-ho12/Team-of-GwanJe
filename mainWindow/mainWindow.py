from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QLabel, QMessageBox
import sys



# from .graphVisualizer import GraphVisualizer
# from .mapVisualizer import MapVisualizer
from .widgethub import Widgethub

class MainWindow(QMainWindow):
    def __init__(self, datahub):
        self.app = QApplication(sys.argv)
        super().__init__()

        self.widgethub = Widgethub()
        self.datahub = datahub

        # self.graphVisualizer = GraphVisualizer(self.widgethub,datahub)
    
        central_widget = QWidget()
        # central_widget.setLayout(self.widgethub.graph)
        self.setCentralWidget(central_widget)

    def start(self):
        # self.graphVisualizer.start()
        self.show()

    def setEventLoop(self):
        sys.exit(self.app.exec_())
