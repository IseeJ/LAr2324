import sys
import time
import random
from datetime import datetime
import serial
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import pyqtgraph as pg

class PurifierModel(QtCore.QAbstractListModel):
    def __init__(self, *args, **kwargs):
        super(PurifierModel, self).__init__(*args, **kwargs)
        self.data_T1 = []
        self.data_T2 = []

    def getData(self):
        return self.data_T1, self.data_T2

    def appendData(self, val_T1, val_T2):
        self.data_T1.append(val_T1)
        self.data_T2.append(val_T2)

    def reset(self):
        self.data_T1 = []
        self.data_T2 = []

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, serial_port, baud_rate):
        super(MainWindow, self).__init__()

        # setup user interface from Designer
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.model = PurifierModel()

        # initialize the graphs
        self.initGraph()

        # Serial port setup
        self.ser = serial.Serial(serial_port, baud_rate, timeout=10)
        
        # connect signals/slots
        self.ui.startStopButton.pressed.connect(self.toggleRun)
        self.ui.clearButton.pressed.connect(self.clearPlot)

        # setup a timer (for updating the plot).
        self.timer = QtCore.QTimer()
        self.timer.setInterval(300)  # ms
        self.timer.timeout.connect(self.update)
        
        self.runningFlag = False
        self.start_time = datetime.now()

    def initGraph(self):
        self.ui.graphWidget.setBackground("w")

        # define color for line on graph
        pen_T1 = pg.mkPen(color=(255, 0, 0))
        pen_T2 = pg.mkPen(color=(0, 0, 255))
        
        self.line_T1 = self.ui.graphWidget.getPlotItem().plot(pen=pen_T1, name="T1")
        self.line_T2 = self.ui.graphWidget.getPlotItem().plot(pen=pen_T2, name="T2")

        self.ui.graphWidget.setLabel("left", "Temperature (°C)")
        self.ui.graphWidget.setLabel("bottom", "Time (min)")

    def clearPlot(self):
        self.model.reset()
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

    def addPoint(self):
        hex_data = [0x01, 0x16, 0x7B, 0x28, 0x48, 0x4C, 0x45, 0x48, 0x54, 0x43, 0x34, 0x30, 0x39, 0x35, 0x67, 0x71, 0x29, 0x7D, 0x7E, 0x04]
        byte_data = bytearray(hex_data)
        self.ser.write(byte_data)
        time.sleep(2)
        response = self.ser.read(37)
        response_hex = response.hex()
        bits_response = ' '.join(response_hex[i:i + 2] for i in range(0, len(response_hex), 2))
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
        self.model.appendData((current_time, T1_d), (current_time, T2_d))

    def update(self):
        self.addPoint()
        self.plotData()

    def plotData(self):
        time_T1, temp_T1 = zip(*self.model.data_T1) if self.model.data_T1 else ([], [])
        time_T2, temp_T2 = zip(*self.model.data_T2) if self.model.data_T2 else ([], [])
        self.line.setData(time_T1, temp_T1)
        self.line.setData(time_T2, temp_T2)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    serial_port = '/dev/cu.usbserial-110'
    baud_rate = 38400
    main = MainWindow(serial_port, baud_rate)
    main.show()
    sys.exit(app.exec_())



