import logging
import random
import sys
import time
import serial

from PyQt5.QtCore import QRunnable, Qt, QThreadPool
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

logging.basicConfig(format="%(message)s", level=logging.INFO)


# Qthread code from https://realpython.com/python-pyqt-qthread/
# 1. Subclass Worker, QRunnable                                                           
class Worker(QRunnable):
    def __init__(self, n):
        super().__init__()
        self.n = n
        self.ser = serial.Serial('/dev/cu.usbserial-110', 38400, timeout=2)
        logging.info(f"Serial start")

    def run(self):
        # Your long-running task goes here ...                                    
        """                                                                       
        for i in range(5):                                                        
            logging.info(f"Working in thread {self.n}, step {i + 1}/5")           
            time.sleep(random.randint(700, 2500) / 1000)                          
        """

        try:
            hex_data = [0x01, 0x16, 0x7B, 0x28, 0x48, 0x4C, 0x45, 0x48, 0x54, 0x4\
3, 0x34, 0x30, 0x39, 0x35, 0x67, 0x71, 0x29, 0x7D, 0x7E, 0x04]
            byte_data = bytearray(hex_data)
            #self.ser = serial.Serial('/dev/cu.usbserial-110', 38400, timeout=2)  
            self.ser.write(byte_data)
            time.sleep(2)
            response = self.ser.readline()
            if response:
                response_hex = response.hex()
                T1 = int(response_hex[34:36] + response_hex[32:34], 16) / 10  # T\
1                                                                                 
                logging.info(f"T1: {T1}")
            else:
                logging.warning("None")
        except serial.SerialException as e:
            logging.error("Error")
        finally:
            self.ser.close()
            logging.info("Serial stop")

class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("QThreadPool + QRunnable")
        self.resize(250, 150)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        # Create and connect widgets                                              
        self.label = QLabel("Hello, World!")
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        countBtn = QPushButton("Click me!")
        countBtn.clicked.connect(self.runTasks)
        # Set the layout                                                          
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(countBtn)
        self.centralWidget.setLayout(layout)

    def runTasks(self):
        threadCount = QThreadPool.globalInstance().maxThreadCount()
        self.label.setText(f"Running {threadCount} Threads")
        pool = QThreadPool.globalInstance()

        '''                                                                       
        for i in range(threadCount):                                              
            # 2. Instantiate the subclass of QRunnable                            
            runnable = Runnable(i)                                                
            # 3. Call start()                                                     
            pool.start(runnable)                                                  
        '''
        runnable = Worker(1)
        pool.start(runnable)


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())


