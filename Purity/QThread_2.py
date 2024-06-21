import logging
import sys
import time
import serial

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

# Define a WorkerSignals class to handle signals
class WorkerSignals(QObject):
    result = pyqtSignal(float)

# 1. Subclass Worker, QThread                                                           
class Worker(QThread):
    result = pyqtSignal(float)

    def __init__(self):
        super().__init__()
        self.ser = serial.Serial('/dev/cu.usbserial-110', 38400, timeout=2)
        self.is_running = True
        logging.info(f"Serial start")

    def run(self):
        try:
            hex_data = [0x01, 0x16, 0x7B, 0x28, 0x48, 0x4C, 0x45, 0x48, 0x54, 0x43, 0x34, 0x30, 0x39, 0x35, 0x67, 0x71, 0x29, 0x7D, 0x7E, 0x04]
            byte_data = bytearray(hex_data)
            while self.is_running:
                self.ser.write(byte_data)
                time.sleep(2)
                response = self.ser.readline()
                if response:
                    response_hex = response.hex()
                    T1 = int(response_hex[34:36] + response_hex[32:34], 16) / 10  # T1                                                                                
                    logging.info(f"T1: {T1}")
                    self.result.emit(T1)  # Emit the result signal with T1 value
                else:
                    logging.warning("None")
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
        self.setWindowTitle("QThread + QThread")
        self.resize(250, 150)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        # Create and connect widgets                                              
        self.label = QLabel("Hello, World!")
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.T1Label = QLabel("T1: --")
        self.T1Label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.startBtn = QPushButton("Start")
        self.startBtn.clicked.connect(self.startTask)
        self.stopBtn = QPushButton("Stop")
        self.stopBtn.clicked.connect(self.stopTask)
        self.stopBtn.setEnabled(False)
        # Set the layout                                                          
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.T1Label)
        layout.addWidget(self.startBtn)
        layout.addWidget(self.stopBtn)
        self.centralWidget.setLayout(layout)

    def startTask(self):
        self.worker = Worker()
        self.worker.result.connect(self.updateT1)
        self.worker.start()
        self.startBtn.setEnabled(False)
        self.stopBtn.setEnabled(True)

    def stopTask(self):
        self.worker.stop()
        self.startBtn.setEnabled(True)
        self.stopBtn.setEnabled(False)

    @pyqtSlot(float)
    def updateT1(self, T1):
        self.T1Label.setText(f"T1: {T1:.1f}")

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
