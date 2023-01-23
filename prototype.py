import sys, os
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWidgets import QApplication, QMainWindow

class MapViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Real-time Dynamic Map")

        # Create the QWebEngineView widget
        self.view = QWebEngineView(self)
        self.view.setGeometry(0, 0, 800, 600)

        # Load the HTML file that contains the leaflet map
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        file_path = os.path.join(dir_path, 'map.html')
        self.view.load(QUrl.fromLocalFile(file_path))
        self.view.show()

        # Connect the QWebEngineView's loadFinished signal to the on_load_finished slot
        self.view.loadFinished.connect(self.on_load_finished)

    def on_load_finished(self):
        # Get the QWebEnginePage object
        page = self.view.page()

        # Inject a JavaScript function to update the marker's location
        script = """

        var map = L.map('map').setView([51.5, -0.09], 13);
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
        page.runJavaScript(script)
        page.runJavaScript(script)

        # Create a QTimer to call the updateMarker function every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_marker)
        self.timer.start(1000)

    def update_marker(self):
        # Call the JavaScript function to update the marker's location
        self.view.page().runJavaScript("updateMarker()")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    map_viewer = MapViewer()
    map_viewer.show()
    sys.exit(app.exec_())
