import sys
import json
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt


import sys
import time
from datetime import datetime
import serial


#from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

from mainwindow import Ui_MainWindow

import random


"""
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
"""
        
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, serial_port, baud_rate):
        super().__init__()
        self.ser = serial.Serial(serial_port, baud_rate, timeout=10)
        self.plot_graph = pg.PlotWidget()
        self.setCentralWidget(self.plot_graph)
        self.plot_graph.setBackground("w")
        pen_T1 = pg.mkPen(color=(255, 0, 0))
        pen_T2 = pg.mkPen(color=(0, 0, 255))
        self.plot_graph.setTitle("Temperature vs Time", color="b", size="20pt")
        styles = {"color": "red", "font-size": "18px"}
        self.plot_graph.setLabel("left", "Temperature (°C)", **styles)
        self.plot_graph.setLabel("bottom", "Time (min)", **styles)
        self.plot_graph.addLegend()
        self.plot_graph.showGrid(x=True, y=True)
        self.plot_graph.setYRange(20, 40)
        self.time = []
        self.temperature_T1 = []
        self.temperature_T2 = []
        self.start_time = datetime.now()
        self.line_T1 = self.plot_graph.plot(
            self.time,
            self.temperature_T1,
            name="T1",
            pen=pen_T1,
            symbol="o",
            symbolSize=15,
            symbolBrush="r",
        )
        self.line_T2 = self.plot_graph.plot(
            self.time,
            self.temperature_T2,
            name="T2",
            pen=pen_T2,
            symbol="o",
            symbolSize=15,
            symbolBrush="b",
        )
        self.timer = QtCore.QTimer()
        self.timer.setInterval(300)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_plot(self):
        hex_data = [0x01, 0x16, 0x7B, 0x28, 0x48, 0x4C, 0x45, 0x48, 0x54, 0x43, 0x34, 0x30, 0x39, 0x35, 0x67, 0x71, 0x29, 0x7D, 0x7E, 0x04]
        byte_data = bytearray(hex_data)
        self.ser.write(byte_data)
        time.sleep(2)
        response = self.ser.read(37)
        response_hex = response.hex()
        bits_response = ' '.join(response_hex[i:i+2] for i in range(0, len(response_hex), 2))
        pairs = bits_response.split()
        print(response_hex)
        #T1
        pair_18 = pairs[17]  # 18th bit
        pair_17 = pairs[16]  # 17th bit
        T1 = pair_18 + pair_17
        T1_d = int(T1, 16) / 10

        #T2
        pair_20 = pairs[19]  # 20th bit
        pair_19 = pairs[18]  # 19th bit
        T2 = pair_20 + pair_19
        T2_d = int(T2, 16) / 10

        print("T1:", T1, T1_d, "T2:", T2, T2_d)
        current_time = (datetime.now() - self.start_time).seconds/60
        self.time.append(current_time)
        self.temperature_T1.append(T1_d)
        self.temperature_T2.append(T2_d)

        self.line_T1.setData(self.time, self.temperature_T1)
        self.line_T2.setData(self.time, self.temperature_T2)
        
        
app = QtWidgets.QApplication(sys.argv)
serial_port = '/dev/cu.usbserial-110'
baud_rate = 38400
MainWindow(serial_port, baud_rate)
window.show()
app.exec_()


