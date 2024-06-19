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

class MainWindow(QMainWindow):
    def __init__(self, serial_port, baud_rate, num_channels=8):
        super(MainWindow, self).__init__()
        self.ser = serial.Serial(serial_port, baud_rate, timeout=10)
        self.num_channels = num_channels

        # setup user interface from Designer
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.model = PurifierModel()

        # initialize the graphs
        self.initGraph()

        # connect signals/slots
        self.ui.startStopButton.pressed.connect(self.toggleRun)
        self.ui.clearButton.pressed.connect(self.clearPlot)

        # setup a timer (for updating the plot)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)  # ms
        self.timer.timeout.connect(self.update)

        self.time = []
        self.temperatures = [[] for _ in range(self.num_channels)]
        self.start_time = datetime.now()

        # Initialize labels for each channel dynamically
        self.initLabels()

    def initGraph(self):
        self.ui.graphWidget.setBackground("w")

        # define colors for lines on graph
        pen_colors = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0),
                      (255, 0, 255), (0, 255, 255), (128, 0, 0), (0, 128, 0)]

        self.lines = []
        for i in range(self.num_channels):
            pen = pg.mkPen(color=pen_colors[i % len(pen_colors)])
            line = self.ui.graphWidget.plot(pen=pen, name=f"T{i+1}")
            self.lines.append(line)

        self.ui.graphWidget.setLabel("left", "Temperature (°C)", color="red", size="18px")
        self.ui.graphWidget.setLabel("bottom", "Time (min)", color="red", size="18px")
        self.ui.graphWidget.addLegend()
        self.ui.graphWidget.showGrid(x=True, y=True)
        self.ui.graphWidget.setYRange(20, 40)

        self.runningFlag = False

    def initLabels(self):
        self.labels = []
        for i in range(self.num_channels):
            label = QtWidgets.QLabel(self.centralwidget)
            label.setObjectName(f"label_T{i+1}")
            self.ui.verticalLayout.addWidget(label)
            self.labels.append(label)

    def clearPlot(self):
        self.model.reset()
        self.time.clear()
        for channel_data in self.temperatures:
            channel_data.clear()
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
        self.updateLabels()

    def readSerialData(self):
        # Simulated serial data reading for demonstration
        for i in range(self.num_channels):
            # Simulate temperature data
            temperature = random.uniform(20, 40)
            self.temperatures[i].append(temperature)

        current_time = (datetime.now() - self.start_time).seconds / 60
        self.time.append(current_time)

    def plotData(self):
        for i in range(self.num_channels):
            self.lines[i].setData(self.time, self.temperatures[i], name=f"T{i+1}")

    def updateLabels(self):
        for i in range(self.num_channels):
            if self.temperatures[i]:
                self.labels[i].setText(f"T{i+1}: {self.temperatures[i][-1]:.1f} °C")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    serial_port = '/dev/cu.usbserial-110'
    baud_rate = 38400
    num_channels = 8
    window = MainWindow(serial_port, baud_rate, num_channels)
    window.show()
    sys.exit(app.exec_())
