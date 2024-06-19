import sys
import json
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt

#from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

from mainwindow import Ui_MainWindow

import random

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
    def __init__(self):
        super(MainWindow, self).__init__()

        # setup user interface from Designer
        # see: https://www.riverbankcomputing.com/static/Docs/PyQt5/designer.html
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.model = PurifierModel()

        # initialize the graphs
        self.initGraph()

        # connect signals/slots
        self.ui.startStopButton.pressed.connect(self.toggleRun)
        self.ui.clearButton.pressed.connect(self.clearPlot)

        # setup a timer (for updating the plot).
        # eventually, the timer would be replaced by the arrival of serial data
        # which would trigger a plot update
        self.timer = QtCore.QTimer()
        self.timer.setInterval(300) # ms
        self.timer.timeout.connect(self.update)
        
    def initGraph(self):
        self.ui.graphWidget.setBackground("w")

        # define color for line on graph
        pen = pg.mkPen(color=(255, 0, 0))
        
        self.line = self.ui.graphWidget.getPlotItem().plot(pen=pen)
        self.plotData()

        self.ui.graphWidget.setLabel("left", "y-values [arb.]")
        self.ui.graphWidget.setLabel("bottom", "Time [arb.]")

        self.runningFlag = False

    def clearPlot(self):
        self.model.reset()
        self.plotData()
        
    def toggleRun(self):
        if self.runningFlag:
            self.stopRun()
        else:
            self.startRun()

    def startRun(self):
        print('hi')
        self.runningFlag = True
        #call addPoint() on a timer
        self.timer.start()
        
    def stopRun(self):
        print('bye')
        self.runningFlag = False
        # kill the addPoint() timer
        self.timer.stop()

    def addPoint(self):
        self.model.appendData(random.randint(0,10))

    def update(self):
        self.addPoint()
        self.plotData()

    def plotData(self):
        self.line.setData(range(len(self.model.data)), self.model.data)
        
        
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()


