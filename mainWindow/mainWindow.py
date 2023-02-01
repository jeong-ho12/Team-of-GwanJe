from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton,QLineEdit, QLabel, QMessageBox, QInputDialog
from PyQt5.QtCore import QThread, QUrl, QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys, os
from pyqtgraph import PlotWidget, GridItem
from numpy import empty
from numpy import zeros

class GraphViewer_Thread(QThread):
    def __init__(self, mainwindow,datahub):
        super().__init__()
        self.mainwindow = mainwindow
        self.datahub = datahub

        self.view = QWebEngineView(self.mainwindow)
        self.view.load(QUrl())
        self.view.setGeometry(10, 10, 10, 10)
        
        self.pw_angle = PlotWidget(self.mainwindow)
        self.pw_angleSpeed = PlotWidget(self.mainwindow)
        self.pw_accel = PlotWidget(self.mainwindow)
        
        self.pw_angle.addItem(GridItem())
        self.pw_angleSpeed.addItem(GridItem())
        self.pw_accel.addItem(GridItem())

        #set label in each axis
        self.pw_angle.getPlotItem().getAxis('bottom').setLabel('Time(second)')
        self.pw_angle.getPlotItem().getAxis('left').setLabel('Degree')
        self.pw_angleSpeed.getPlotItem().getAxis('bottom').setLabel('Time(second)')
        self.pw_angleSpeed.getPlotItem().getAxis('left').setLabel('Degree/second')
        self.pw_accel.getPlotItem().getAxis('bottom').setLabel('Time(second)')
        self.pw_accel.getPlotItem().getAxis('left').setLabel('g(gravity accel)')

        #set range in each axis
        self.pw_angle.setYRange(-180,180)
        self.pw_angleSpeed.setYRange(-1000,1000)
        self.pw_accel.setYRange(-6,6)

        #legend
        self.pw_angle.getPlotItem().addLegend()
        self.pw_angleSpeed.getPlotItem().addLegend()
        self.pw_accel.getPlotItem().addLegend()
    

        

        self.pw_angle.setGeometry(10, 10, 300, 300)
        self.pw_angleSpeed.setGeometry(10, 320, 300, 300)
        self.pw_accel.setGeometry(10, 630, 300, 300)
        

        self.curve_roll = self.pw_angle.plot(pen='r', name = "roll")
        self.curve_pitch = self.pw_angle.plot(pen='g',name = "pitch")
        self.curve_yaw = self.pw_angle.plot(pen='b', name = "yaw")

        self.curve_rollSpeed = self.pw_angleSpeed.plot(pen='r', name = "roll speed")
        self.curve_pitchSpeed = self.pw_angleSpeed.plot(pen='g', name = "pitch speed")
        self.curve_yawSpeed = self.pw_angleSpeed.plot(pen='b', name = "yaw speed")

        self.curve_xaccel = self.pw_accel.plot(pen='r', name = "x acc")
        self.curve_yaccel = self.pw_accel.plot(pen='g',name = "y acc")
        self.curve_zaccel = self.pw_accel.plot(pen='b',name ="z acc")

        
        self.loadnum = 0

        self.starttime = 0.0
        self.starttime_count = 0
        self.init_sec = 0
        self.time = zeros(150)
        self.roll = zeros(150)
        self.pitch = zeros(150)
        self.yaw = zeros(150)
        self.rollSpeed = zeros(150)
        self.pitchSpeed = zeros(150)
        self.yawSpeed = zeros(150)
        self.xaccel = zeros(150)
        self.yaccel = zeros(150)
        self.zaccel = zeros(150)

    def update_data(self):
        if len(self.datahub.altitude) == 0:
            pass

        else:
            if len(self.datahub.altitude) <= 150 :
                n = len(self.datahub.altitude) 
                self.roll[-n:] = self.datahub.rolls
                self.pitch[-n:] = self.datahub.pitchs
                self.yaw[-n:] = self.datahub.yaws
                self.rollSpeed[-n:] = self.datahub.rollSpeeds
                self.pitchSpeed[-n:] = self.datahub.pitchSpeeds
                self.yawSpeed[-n:] = self.datahub.yawSpeeds
                self.xaccel[-n:] = self.datahub.Xaccels
                self.yaccel[-n:] = self.datahub.Yaccels
                self.zaccel[-n:] = self.datahub.Zaccels
                hours = self.datahub.hours * 3600
                minutes = self.datahub.mins * 60
                miliseconds = self.datahub.tenmilis * 0.01
                seconds = self.datahub.secs
                totaltime = hours + minutes + miliseconds + seconds
                self.starttime = self.datahub.hours[0]*3600 + self.datahub.mins[0]*60 + self.datahub.tenmilis[0]*0.01+ self.datahub.secs[0]
                self.time[-n:] = totaltime - self.starttime
                print(n)
                print("hello")
                print(self.time)
            
            else : 
                self.roll[:] = self.datahub.rolls[-150:]
                self.pitch[:] = self.datahub.pitchs[-150:]
                self.yaw[:] = self.datahub.yaws[-150:]
                self.rollSpeed[:] = self.datahub.rollSpeeds[-150:]
                self.pitchSpeed[:] = self.datahub.pitchSpeeds[-150:]
                self.yawSpeed[:] = self.datahub.yawSpeeds[-150:]
                self.xaccel[:] = self.datahub.Xaccels[-150:]
                self.yaccel[:] = self.datahub.Yaccels[-150:]
                self.zaccel[:] = self.datahub.Zaccels[-150:]
                hours = self.datahub.hours[-150:] * 3600
                minutes = self.datahub.mins[-150:] * 60
                miliseconds = self.datahub.tenmilis[-150:] * 0.01
                seconds = self.datahub.secs[-150:]
                totaltime = hours + minutes + miliseconds + seconds
                self.time[:] = totaltime - self.starttime

            self.curve_roll.setData(x=self.time, y=self.roll)
            self.curve_pitch.setData(x=self.time, y=self.pitch)
            self.curve_yaw.setData(x=self.time, y=self.yaw)

            self.curve_rollSpeed.setData(x=self.time, y=self.rollSpeed)
            self.curve_pitchSpeed.setData(x=self.time, y=self.pitchSpeed)
            self.curve_yawSpeed.setData(x=self.time, y=self.yawSpeed)

            self.curve_xaccel.setData(x=self.time, y=self.xaccel)
            self.curve_yaccel.setData(x=self.time, y=self.yaccel)
            self.curve_zaccel.setData(x=self.time, y=self.zaccel)

    def on_load_finished(self):
        # to move the timer to the same thread as the QObject
        self.mytimer = QTimer(self)
        self.mytimer.timeout.connect(self.update_data)
        self.mytimer.start(100)

    def run(self):
        self.view.loadFinished.connect(self.on_load_finished)


class MapViewer_Thread(QThread):
    def __init__(self, mainwindow,datahub):
        super().__init__()
        self.mainwindow = mainwindow
        self.datahub= datahub
        # self.setWindowTitle("Real-time Dynamic Map")

        # Create the QWebEngineView widget
        self.view = QWebEngineView(self.mainwindow)
        self.view.setGeometry(320,220, 800, 600)
        
        # Load the HTML file that contains the leaflet map
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        file_path = os.path.join(dir_path, 'map.html')
        self.view.load(QUrl.fromLocalFile(file_path))
        self.view.show()


    def on_load_finished(self):
        # Get the QWebEnginePage object
    
        page = self.view.page()
        # Inject a JavaScript function to update the marker's location
        self.script = f"""
        var lat = 36.666;
        var lng = 126.666;
        var map = L.map("map").setView([lat,lng], 15);
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
            maxZoom: 18,
        }}).addTo(map);
        var marker = L.marker([lat,lng]).addTo(map);
        /*
        trigger is a variable which update a map view according to their location
        */
        var trigger_javascript = 0;
        function updateMarker(latnew, lngnew, trigger_python) {{
           
            marker.setLatLng([latnew, lngnew]);
        
            if(trigger_python >= 1 && trigger_javascript == 0) {{
            map.setView([latnew,lngnew], 15);
            trigger_javascript = 1;
            }}
        }}
        """
        #{print(self.datahub.latitudes)}
        page.runJavaScript(self.script)
        # Create a QTimer to call the updateMarker function every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_marker)
        self.timer.start(1000)

    def update_marker(self):
        #wait for receiving datas.....
        if len(self.datahub.latitudes) == 0:
            pass
        # Call the JavaScript function to update the marker's location
        else: 
            self.view.page().runJavaScript(f"updateMarker({self.datahub.latitudes[-1]},{self.datahub.longitudes[-1]},{len(self.datahub.latitudes)})")

    # Connect the QWebEngineView's loadFinished signal to the on_load_finished slot
    def run(self):
        self.view.loadFinished.connect(self.on_load_finished)


class MainWindow(QMainWindow):
    def __init__(self, datahub):
        self.app = QApplication(sys.argv)
        super().__init__()

        self.datahub = datahub
        self.resize(1440,1080)
        self.setStyleSheet("QMainWindow { background-color: rgb(20, 20, 20);}")
        
        """Set Buttons"""
        self.start_button = QPushButton("Press Start",self,)
        self.stop_button = QPushButton("Stop",self,)
        self.rf_port_edit = QLineEdit("COM8",self)
        
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.rf_port_edit.setEnabled(True)
        
        """Set Buttons Connection"""
        self.start_button.clicked.connect(self.start_button_clicked)
        self.stop_button.clicked.connect(self.stop_button_clicked)
        
        """Set Geometry"""
        self.start_button.setGeometry(1170,400,200,150)
        self.stop_button.setGeometry(1170,600,200,150)
        QLabel("Enter your Serial Port:",self).setGeometry(1170,320,200,30)
        self.rf_port_edit.setGeometry(1170,350,200,30)
        
        """Set Viewer Thread"""
        self.mapviewer = MapViewer_Thread(self,datahub)
        self.graphviewr = GraphViewer_Thread(self,datahub)
        self.mapviewer.start()
        self.graphviewr.start()

    # Run when start button is clicked
    def start_button_clicked(self):
        QMessageBox.information(self,"information","Program Start")
        FileName,ok = QInputDialog.getText(self,'Input Dialog', 'Enter your File Name',QLineEdit.Normal,"Your File Name")
        if ok:
            self.datahub.mySerialPort=self.rf_port_edit.text()
            self.datahub.file_Name = FileName+'.csv'
            self.datahub.communication_start()
            
            self.datahub.serial_port_error=-1
            if self.datahub.check_communication_error():
                QMessageBox.warning(self,"warning","SSUJJUN")
                self.datahub.communication_stop()

            else:
                self.datahub.datasaver_start()
                self.start_button.setEnabled(False)
                self.stop_button.setEnabled(True)
                self.rf_port_edit.setEnabled(False)
        self.datahub.serial_port_error=-1
    # Run when stop button is clicked
    def stop_button_clicked(self):
        QMessageBox.information(self,"information","Program Stop")
        self.datahub.communication_stop()
        self.datahub.datasaver_stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.rf_port_edit.setEnabled(False)     
        
    # Main Window start method
    def start(self):
        self.show()
        
    def setEventLoop(self):
        sys.exit(self.app.exec_())
        
    # Run when mainwindow is closed
    def closeEvent(self, event):
        self.stop_button_clicked()
        event.accept()