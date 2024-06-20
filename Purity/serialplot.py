import logging
import sys
import time
from datetime import datetime
import serial
import pyqtgraph as pg
from pyqtgraph import PlotWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
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
    result = pyqtSignal(float, float, float)

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
                    T1 = int(response_hex[34:36] + response_hex[32:34], 16) / 10  # T1                                                                                     
                    T2 = int(response_hex[38:40] + response_hex[36:38], 16) / 10  # T2                                                                                     
                    logging.info(f"Time: {current_time}, T1: {T1}, T2: {T2}")

                    self.result.emit(current_time,T1, T2)
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


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("QThread + pyqtgraph")
        self.resize(600, 400)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.T1Label = QLabel("T1: --")
        self.T1Label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.T2Label = QLabel("T2: --")
        self.T2Label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.startBtn = QPushButton("Start")
        self.startBtn.clicked.connect(self.startTask)
        self.stopBtn = QPushButton("Stop")
        self.stopBtn.clicked.connect(self.stopTask)
        self.stopBtn.setEnabled(False)

        self.plotWidget = PlotWidget()
        self.plotWidget.setBackground('w')
        self.plotWidget.setYRange(0, 100, padding=0)

        layout = QVBoxLayout()
        layout.addWidget(self.T1Label)
        layout.addWidget(self.T2Label)
        layout.addWidget(self.plotWidget)
        layout.addWidget(self.startBtn)
        layout.addWidget(self.stopBtn)
        self.centralWidget.setLayout(layout)

        self.time = []
        self.dataT1 = []
        self.dataT2 = []
        self.plotData1 = self.plotWidget.plot(self.time, self.dataT1, pen=pg.mkPen(color=(255, 0, 0), width=2))
        self.plotData2 = self.plotWidget.plot(self.time, self.dataT2, pen=pg.mkPen(color=(0, 0, 255), width=2))

    def startTask(self):
        self.worker = Worker()
        self.worker.result.connect(self.updateData)
        self.worker.start()
        self.startBtn.setEnabled(False)
        self.stopBtn.setEnabled(True)

    def stopTask(self):
        self.worker.stop()
        self.startBtn.setEnabled(True)
        self.stopBtn.setEnabled(False)

    @pyqtSlot(float, float, float)
    def updateData(self, current_time, T1, T2):
        self.T1Label.setText(f"T1: {T1:.1f}")
        self.T2Label.setText(f"T2: {T2:.1f}")

        self.time.append(current_time)

        self.dataT1.append(T1)
        self.dataT2.append(T2)

        self.plotData1.setData(self.time, self.dataT1)
        self.plotData2.setData(self.time, self.dataT2)


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
