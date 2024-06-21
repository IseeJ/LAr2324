import sys
import logging
import time
from datetime import datetime
import serial
import numpy as np
import pyqtgraph as pg
from pyqtgraph import PlotWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QModelIndex, QObject
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

logging.basicConfig(format="%(message)s", level=logging.INFO)


class Worker(QThread):
    result = pyqtSignal(float, tuple)

    def __init__(self):
        super().__init__()
        self.ser = serial.Serial('/dev/cu.usbserial-110', 38400, timeout=2)
        self.is_running = True
        logging.info("Serial Start")
        self.start_time = None

    def run(self):
        try:
            hex_data = [0x01, 0x16, 0x7B, 0x28, 0x48, 0x4C, 0x45, 0x48, 0x54, 0x43, 0x34, 0x30, 0x39, 0x35, 0x67, 0x71, 0x29, 0x7D, 0x7E, 0x04]
            byte_data = bytearray(hex_data)
            self.start_time = datetime.now()
            while self.is_running:
                self.ser.write(byte_data)
                time.sleep(2)
                response = self.ser.readline()
                if response:
                    response_hex = response.hex()
                    current_time = (datetime.now() - self.start_time).seconds / 60
                    temperatures = parse_temp(response)
                    logging.info(f"Time: {current_time}, Temperatures: {temperatures}")
                    self.result.emit(current_time, temperatures)
                else:
                    logging.warning("No response")
        except serial.SerialException as e:
            logging.error("Error")
        finally:
            self.ser.close()
            logging.info("Serial stop")

    def stop(self):
        self.is_running = False
        self.quit()
        self.wait()


def hex_dec(T_hex):
    try:
        T_val = int(T_hex, 16)
        T_max = 18000  #1800C max                                                                                                                                                                                                                                                                                                                                                                                                                                                       
        hex_max = 0xFFFF  #FFFF max                                                                                                                                                                                                                                                                                                                                                                                                                                                     
        if T_val > T_max:
            T = -(hex_max - T_val + 1) / 100  #negative value                                                                                                                                                                                                                                                                                                                                                                                                                           
        else:
            T = T_val / 10
        return T
    except ValueError:
        return 'err'


def parse_temp(response):
    response_hex = response.hex()
    temperatures = []

    for i in range(8):
        hex_str = response_hex[34 + i * 4:36 + i * 4] + response_hex[32 + i * 4:34 + i * 4]
        temperatures.append(hex_dec(hex_str))
    return tuple(temperatures)


class PurifierModel(QObject):
    def __init__(self, parent=None):
        super(PurifierModel, self).__init__(parent)
        self.data = []  #for tuples                                                                                                                                                                                                                                                                                                                                                                                                                                                     

    def rowCount(self, parent=QModelIndex()):
        return len(self.data)

    def appendData(self, time, *temps):
        self.data.append((time,) + temps)
        self.dataChanged.emit()

    def clearData(self):
        self.data = []
        self.dataChanged.emit()

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row = index.row()
            return self.data[row]

        return None

    dataChanged = pyqtSignal()


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Temperature")
        self.resize(800, 600)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.labels = []
        self.data = [[] for _ in range(8)]  #list for 8 channels data                                                                                                                                                                                                                                                                                                                                                                                                                   
        self.time = []
        self.model = PurifierModel()

        layout = QVBoxLayout()

        for i in range(8):
            label = QLabel(f"T{i + 1}: --")
            label.setAlignment(Qt.AlignCenter)
            self.labels.append(label)
            layout.addWidget(label)

        self.plotWidget = PlotWidget()
        self.plotWidget.setBackground('w')
        self.plotWidget.setYRange(0, 100, padding=0)
        layout.addWidget(self.plotWidget)

        self.startBtn = QPushButton("Start")
        self.startBtn.clicked.connect(self.startTask)
        layout.addWidget(self.startBtn)

        self.stopBtn = QPushButton("Stop")
        self.stopBtn.clicked.connect(self.stopTask)
        self.stopBtn.setEnabled(False)
        layout.addWidget(self.stopBtn)

        self.centralWidget.setLayout(layout)

        # Initialize plot lines for T1 to T8                                                                                                                                                                                                                                                                                                                                                                                                                                            
        self.plotLines = []
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
                  (255, 0, 255), (0, 255, 255), (128, 0, 0), (0, 128, 0)]

        for i in range(8):
            plot_line = self.plotWidget.plot(self.time, self.data[i], pen=pg.mkPen(color=colors[i % len(colors)], width=2))
            self.plotLines.append(plot_line)

    def startTask(self):
        self.worker = Worker()
        self.worker.result.connect(self.updateData)
        self.worker.start()
        self.startBtn.setEnabled(False)
        self.stopBtn.setEnabled(True)

    def stopTask(self):
        if self.worker:
            self.worker.stop()
            self.worker = None
        self.startBtn.setEnabled(True)
        self.stopBtn.setEnabled(False)

    @pyqtSlot(float, tuple)
    def updateData(self, current_time, temperatures):
        #update temperature labels                                                                                                                                                                                                                                                                                                                                                                                                                                                      
        for i in range(8):
            if temperatures[i] != 'err':
                self.labels[i].setText(f"T{i + 1}: {temperatures[i]:.1f}")
            else:
                self.labels[i].setText(f"T{i + 1}: --")

        #store data to PurifierModel                                                                                                                                                                                                                                                                                                                                                                                                                                                    
        self.model.appendData(current_time, *temperatures)
        self.time.append(current_time)

        #update data arrays for each temperature                                                                                                                                                                                                                                                                                                                                                                                                                                        
        for i in range(8):
            if i < len(temperatures):
                if temperatures[i] == 'err':
                    self.data[i].append(np.nan)  #for missing data                                                                                                                                                                                                                                                                                                                                                                                                                      
                else:
                    self.data[i].append(temperatures[i])

            self.plotLines[i].setData(self.time, self.data[i])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


