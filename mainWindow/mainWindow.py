from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QLabel, QMessageBox, QInputDialog
from PyQt5.QtCore import QObject, QThread, pyqtSlot, QRunnable, QThreadPool, QUrl, QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
import sys, os
import pyqtgraph as pg
import time


class MainWindow(QMainWindow):
    def __init__(self, datahub):
        self.s = time.time()
        self.app = QApplication(sys.argv)
        super().__init__()

        self.datahub = datahub
        self.resize(1440,1080)
        
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
        


        """initalize 1.map and 2.graph and timer"""

        """1.initialize map"""
        self.view = QWebEngineView(self)
        self.view.setGeometry(320,220, 800, 600)

        # Load the HTML file that contains the leaflet map
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        file_path = os.path.join(dir_path, 'map.html')
        self.view.load(QUrl.fromLocalFile(file_path))
        self.view.show()

        """2.initialize graph"""
        # self.pw_angle = pg.PlotWidget(self)
        # self.pw_angleSpeed = pg.PlotWidget(self)
        # self.pw_accel = pg.PlotWidget(self)
        # self.pw_angle.setGeometry(10, 10, 300, 300)
        # self.pw_angleSpeed.setGeometry(10, 320, 300, 300)
        # self.pw_accel.setGeometry(10, 630, 300, 300)
        

        # self.curve_roll = self.pw_angle.plot(pen='r')
        # self.curve_pitch = self.pw_angle.plot(pen='g')
        # self.curve_yaw = self.pw_angle.plot(pen='b')

        # self.curve_rollSpeed = self.pw_angleSpeed.plot(pen='r')
        # self.curve_pitchSpeed = self.pw_angleSpeed.plot(pen='g')
        # self.curve_yawSpeed = self.pw_angleSpeed.plot(pen='b')

        # self.curve_xaccel = self.pw_accel.plot(pen='r')
        # self.curve_yaccel = self.pw_accel.plot(pen='g')
        # self.curve_zaccel = self.pw_accel.plot(pen='b')

        self.loadnum = 0

        self.init_sec = 0
        self.time = []
        self.roll = []
        self.pitch = []
        self.yaw = []
        self.rollSpeed = []
        self.pitchSpeed = []
        self.yawSpeed = []
        self.xaccel = []
        self.yaccel = []
        self.zaccel = []



        """update map and graph"""
    def on_load_finished(self):

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
        page.runJavaScript(self.script)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_map_graph)
        



    def update_map_graph(self):
        """map update"""
        #wait for receiving datas.....
        if len(self.datahub.latitudes) == 0:
            pass
        # Call the JavaScript function to update the marker's location
        else: 
            self.view.page().runJavaScript(f"updateMarker({self.datahub.latitudes[-1]},{self.datahub.longitudes[-1]},{len(self.datahub.latitudes)})")

            """graph update"""
            # lineRemain =len(self.datahub.hours) - self.loadnum
            # if lineRemain > 0:
            #     for i in range(lineRemain):
            #         min = self.datahub.mins[self.loadnum+i]
            #         sec = self.datahub.secs[self.loadnum+i]
            #         tenmilis = self.datahub.tenmilis[self.loadnum+i]
            #         total_sec = min*60+sec+tenmilis*0.01
            #         if len(self.time)==0:
            #             self.init_sec = total_sec
            #         self.time.append(total_sec-self.init_sec)
    
            #         self.roll.append(self.datahub.rolls[self.loadnum+i])
            #         self.pitch.append(self.datahub.pitchs[self.loadnum+i])
            #         self.yaw.append(self.datahub.yaws[self.loadnum+i])
    
            #         self.rollSpeed.append(self.datahub.rollSpeeds[self.loadnum+i])
            #         self.pitchSpeed.append(self.datahub.pitchSpeeds[self.loadnum+i])
            #         self.yawSpeed.append(self.datahub.yawSpeeds[self.loadnum+i])
    
            #         self.xaccel.append(self.datahub.Xaccels[self.loadnum+i])
            #         self.yaccel.append(self.datahub.Yaccels[self.loadnum+i])
            #         self.zaccel.append(self.datahub.Zaccels[self.loadnum+i])
    
            #     self.loadnum += lineRemain
            # self.curve_roll.setData(x=self.time, y=self.roll)
            # self.curve_pitch.setData(x=self.time, y=self.pitch)
            # self.curve_yaw.setData(x=self.time, y=self.yaw)
    
            # self.curve_rollSpeed.setData(x=self.time, y=self.rollSpeed)
            # self.curve_pitchSpeed.setData(x=self.time, y=self.pitchSpeed)
            # self.curve_yawSpeed.setData(x=self.time, y=self.yawSpeed)
    
            # self.curve_xaccel.setData(x=self.time, y=self.xaccel)
            # self.curve_yaccel.setData(x=self.time, y=self.yaccel)
            # self.curve_zaccel.setData(x=self.time, y=self.zaccel)
    
            # self.pw_angle.setXRange(self.time[-1]-10,self.time[-1])
            # self.pw_angleSpeed.setXRange(self.time[-1]-10,self.time[-1])
            # self.pw_accel.setXRange(self.time[-1]-10,self.time[-1])


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
                self.timer.start(200)

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
        self.view.loadFinished.connect(self.on_load_finished)
        self.show()
        
    def setEventLoop(self):
        sys.exit(self.app.exec_())
        
    # Run when mainwindow is closed
    def closeEvent(self, event):
        self.stop_button_clicked()
        event.accept()