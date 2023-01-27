from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QLabel, QMessageBox
from PyQt5.QtCore import QObject, QThread, pyqtSlot, QRunnable, QThreadPool
import sys
import threading
import sys, os
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWidgets import QApplication, QMainWindow

class MapViewer_Thread(QThread):
    def __init__(self, mainwindow):
        super().__init__()
        self.mainwindow = mainwindow
        # self.setWindowTitle("Real-time Dynamic Map")

        # Create the QWebEngineView widget
        self.view = QWebEngineView(self.mainwindow)
        self.view.setGeometry(0, 0, 800, 600)

        # Load the HTML file that contains the leaflet map
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        file_path = os.path.join(dir_path, 'map.html')
        self.view.load(QUrl.fromLocalFile(file_path))
        self.view.show()


    def on_load_finished(self):
        # Get the QWebEnginePage object
        try:
            page = self.view.page()
            print("eeeeeee")

            # Inject a JavaScript function to update the marker's location
            script = """
            var map = L.map("map").setView([51.5, -0.09], 13);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
                maxZoom: 18,
            }).addTo(map);
            var marker = L.marker([51.5, -0.09]).addTo(map);
            var lat = 51.5;
            var lng = -0.09;
            function updateMarker() {
                lat = lat + 0.001;
                lng = lng + 0.001;
                marker.setLatLng([lat, lng]);
            }
            """
            print("wwwwwwwwww")
            page.runJavaScript(script)

            # Create a QTimer to call the updateMarker function every second
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_marker)
            self.timer.start(1000)
        except:
            print("error appeared!")
    def update_marker(self):
        # Call the JavaScript function to update the marker's location
        self.view.page().runJavaScript("updateMarker()")

    # Connect the QWebEngineView's loadFinished signal to the on_load_finished slot
    def run(self):
        self.view.loadFinished.connect(self.on_load_finished)
        print("showed")


class MainWindow(QMainWindow):
    def __init__(self, datahub):
        self.app = QApplication(sys.argv)
        super().__init__()
        # self.widgethub = Widgethub()
        self.datahub = datahub
        self.mapviewer = MapViewer_Thread(self)

        #버튼 누르면 연결해야하는 것
        self.show_map_button = QPushButton("Show map",self)
        self.show_map_button.clicked.connect(self.start_mapviewer)
   
    def start_mapviewer(self):

        self.mapviewer.start()


    def start(self):
        self.show()


    def setEventLoop(self):
        sys.exit(self.app.exec_())
