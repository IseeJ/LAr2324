import csv
import time
from datetime import datetime as dt

filename = "Pressure_log.csv"
with open(filename, 'a') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Date', 'Timestamp', 'Pressure(Torr)'])

    try:
        Hornet.IG_off()
        time.sleep(10)
        print(Hornet.IG_stat())

        while True:
            pressure = Hornet.getConvectronP()
            now = dt.now()
            csvwriter.writerow([now.strftime('%Y%m%d'), now.strftime('%H%M%S'), pressure])
            print([now.strftime('%Y%m%dT%H%M%S'), pressure])
            
            if pressure < 5e-2:
                print("Turning on IG")
                Hornet.IG_on()
                time.sleep(10)
                print(Hornet.IG_stat())
                print(Hornet.getIonEcurrent())
                csvwriter.writerow(['Date', 'Timestamp', 'IGPressure(Torr)'])
                
                while Hornet.getConvectronP() < 5e-2:
                    ion_pressure = Hornet.getIonP()
                    now = dt.now()
                    csvwriter.writerow([now.strftime('%Y%m%d'), now.strftime('%H%M%S'), ion_pressure])
                    print(now.strftime('%Y%m%dT%H%M%S'), ion_pressure)
                    time.sleep(10)

                Hornet.IG_off()
                time.sleep(10)
                print(Hornet.IG_stat())
                break

            time.sleep(10)

    except KeyboardInterrupt:
        print("Exiting, Saving to Pressure_log.csv")
        exit()
