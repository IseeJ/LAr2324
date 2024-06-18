#scatter plot with text

import sys
import csv
import time
import numpy as np

from PyQt5 import QtWidgets, QtCore

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from IPython.display import clear_output

import matplotlib.image as mpimg

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        
        self.csv_file = 'Tempread/realtimedata_test2.csv'
        self.latest_entry = None #set self.latest_entry= None to avoid error in firsr run (if-statement check latest data aginst previous)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_image)
        self.timer.start(1000)  

    def latest_data(self, csv_file):
        with open(csv_file, 'r') as file:
            data = csv.reader(file)
            for row in data:
                latest_entry = row
            return latest_entry
    
    def update_image(self):
        self.axes.cla()
        #old code
        new_entry = self.latest_data(self.csv_file)
        if new_entry and new_entry != self.latest_entry: 
            self.latest_entry = new_entry
            timestamp = str(new_entry[1])
            CH1 = float(new_entry[2])
            CH2 = float(new_entry[3])
            CH3 = float(new_entry[4])
            CH4 = float(new_entry[5])
            CH5 = float(new_entry[6])
            CH6 = float(new_entry[7])
            CH7 = float(new_entry[8])

            #self.axes.scatter([1, 2, 3, 4, 5, 6, 7], [CH1, CH2, CH3, CH4, CH5, CH6, CH7]) #test
            
            #plot image 
            img = mpimg.imread('Tempread/Diagram.png')  
            self.axes.imshow(img)
            
            #scatter plot on top of img 
            self.axes.text(430, 420, f"CH1: {CH1} °C", fontsize=8, color='black', fontweight='bold')
            self.axes.scatter(390, 350, color='black', edgecolors='white')

            self.axes.text(450, 780, f"CH2: {CH2} °C", fontsize=8, color='white', fontweight='bold')
            self.axes.scatter(500, 820, color='white', edgecolors='black')

            self.axes.text(470, 1170, f"CH3: {CH3} °C", fontsize=8, color='red', fontweight='bold')
            self.axes.scatter(470, 1100, color='red', edgecolors='white')

            self.axes.text(300, 1470, f"CH4: {CH4} °C", fontsize=8, color='lime', fontweight='bold')
            self.axes.scatter(300, 1400, color='lime', edgecolors='white')

            self.axes.text(1750, 730, f"CH5: {CH5} °C", fontsize=8, color='magenta', fontweight='bold')
            self.axes.scatter(1750, 660, color='magenta', edgecolors='white')

            self.axes.text(1500, 1270, f"CH6: {CH6} °C", fontsize=8, color='cyan', fontweight='bold')
            self.axes.scatter(1500, 1200, color='cyan', edgecolors='white')

            self.axes.text(1140, 1470, f"CH7: {CH7} °C", fontsize=8, color='blue', fontweight='bold')
            self.axes.scatter(1140, 1400, color='blue', edgecolors='white')
            
            
            self.axes.set_title(timestamp)
            self.axes.axis('off')
            self.draw()
            


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.setCentralWidget(self.canvas)

        self.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
