#2 cols, CG, IG
import Hornet
import time
from datetime import datetime as dt
import csv

now = dt.now()
filename = str(now.strftime('%Y%m%d%H%M'))+".csv"

with open(filename, 'a') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Date', 'Timestamp','CGPressure(Torr)', 'IGPressure(Torr)'])

    while True:
        CGpressure = Hornet.getConvectronP()
        IGpressure = Hornet.getIonP()
        now = dt.now()
        if str(Hornet.IG_stat())[11:-4] == "ON":
            csvwriter.writerow([now.strftime('%Y%m%d'), now.strftime('%H%M%S'), CGpressure, IGpressure])
            print(now.strftime('%Y%m%dT%H%M%S'), CGpressure, IGpressure)
        else:
            csvwriter.writerow([now.strftime('%Y%m%d'), now.strftime('%H%M%S'), CGpressure, "NaN"])
            print(now.strftime('%Y%m%dT%H%M%S'), CGpressure, 'NaN')
