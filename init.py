import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QPixmap

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        collecting_data_button = QPushButton("Collecting Data", self)
        collecting_data_button.clicked.connect(self.collecting_data)
        
        visualizing_button = QPushButton("Visualizing", self)
        visualizing_button.clicked.connect(self.visualizing)
        
        end_mission_button = QPushButton("End Mission", self)
        end_mission_button.clicked.connect(self.end_mission)
        
        collecting_data_button.move(30, 30)
        visualizing_button.move(30, 60)
        end_mission_button.move(30, 90)

        #create a label to show an image
        label = QLabel(self)
        pixmap = QPixmap('C:/Users/qkrwj/image.png')
        label.setPixmap(pixmap)
        label.move(150,20)
        
        self.setGeometry(300, 300, 500, 300)
        self.setWindowTitle("Buttons")
        self.show()
        
    def collecting_data(self):
        print("Collecting Data")
        
    def visualizing(self):
        print("Visualizing")
        
    def end_mission(self):
        print("End Mission")
        sys.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
