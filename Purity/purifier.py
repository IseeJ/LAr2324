import sys
import time
from datetime import datetime
import serial
from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg
from mainwindow import Ui_MainWindow

class PurifierModel(QtCore.QAbstractListModel):
    def __init__(self, *args, **kwargs):
        super(PurifierModel, self).__init__(*args, **kwargs)

    data = [3,5,1]
        
    def getData(self):
        return self.data

    def appendData(self, val):
        self.data.append(val)

    def reset(self):
        self.data = []

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, serial_port, baud_rate):
        super(MainWindow, self).__init__()

        # Initialize serial connection
        self.ser = serial.Serial(serial_port, baud_rate, timeout=10)
        
        # Setup user interface from Designer
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.model = PurifierModel()

        # Initialize the graphs
        self.initGraph()

        # Connect signals/slots
        self.ui.startStopButton.pressed.connect(self.toggleRun)
        self.ui.clearButton.pressed.connect(self.clearPlot)

        # Setup a timer for updating the plot
        self.timer = QtCore.QTimer()
        self.timer.setInterval(300) # ms
        self.timer.timeout.connect(self.update)
        
        self.time = []
        self.temperature_T1 = []
        self.temperature_T2 = []
        self.start_time = datetime.now()

    def initGraph(self):
        self.ui.graphWidget.setBackground("w")

        # Define color for lines on graph
        pen_T1 = pg.mkPen(color=(255, 0, 0))
        pen_T2 = pg.mkPen(color=(0, 0, 255))
        
        self.line_T1 = self.ui.graphWidget.plot(pen=pen_T1, name="T1")
        self.line_T2 = self.ui.graphWidget.plot(pen=pen_T2, name="T2")

        self.ui.graphWidget.setLabel("left", "Temperature (°C)", color="red", size="18px")
        self.ui.graphWidget.setLabel("bottom", "Time (min)", color="red", size="18px")
        self.ui.graphWidget.addLegend()
        self.ui.graphWidget.showGrid(x=True, y=True)
        self.ui.graphWidget.setYRange(20, 40)

        self.runningFlag = False

    def clearPlot(self):
        self.model.reset()
        self.time.clear()
        self.temperature_T1.clear()
        self.temperature_T2.clear()
        self.plotData()

    def toggleRun(self):
        if self.runningFlag:
            self.stopRun()
        else:
            self.startRun()

    def startRun(self):
        self.runningFlag = True
        self.timer.start()
        
    def stopRun(self):
        self.runningFlag = False
        self.timer.stop()

    def update(self):
        self.readSerialData()
        self.plotData()

    def readSerialData(self):
        hex_data = [0x01, 0x16, 0x7B, 0x28, 0x48, 0x4C, 0x45, 0x48, 0x54, 0x43, 0x34, 0x30, 0x39, 0x35, 0x67, 0x71, 0x29, 0x7D, 0x7E, 0x04]
        byte_data = bytearray(hex_data)
        self.ser.write(byte_data)
        time.sleep(2)
        response = self.ser.read(37)
        response_hex = response.hex()
        bits_response = ' '.join(response_hex[i:i+2] for i in range(0, len(response_hex), 2))
        pairs = bits_response.split()

        # T1
        pair_18 = pairs[17]  # 18th bit
        pair_17 = pairs[16]  # 17th bit
        T1 = pair_18 + pair_17
        T1_d = int(T1, 16) / 10

        # T2
        pair_20 = pairs[19]  # 20th bit
        pair_19 = pairs[18]  # 19th bit
        T2 = pair_20 + pair_19
        T2_d = int(T2, 16) / 10

        current_time = (datetime.now() - self.start_time).seconds / 60
        self.time.append(current_time)
        self.temperature_T1.append(T1_d)
        self.temperature_T2.append(T2_d)

    def plotData(self):
        self.line_T1.setData(self.time, self.temperature_T1)
        self.line_T2.setData(self.time, self.temperature_T2)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    serial_port = '/dev/cu.usbserial-110'
    baud_rate = 38400
    window = MainWindow(serial_port, baud_rate)
    window.show()
    sys.exit(app.exec_())



