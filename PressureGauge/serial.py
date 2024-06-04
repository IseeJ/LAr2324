import serial
import time

ser = serial.Serial(
    port='/dev/tty.usbserial-AB0OAX4J',
    baudrate = 19200,
    parity='N',
    stopbits=1,
    bytesize=8,
    timeout=1
)

while True:
    ser.write(bytearray(b'#01RS\r'))
    #ser.write(bytearray(b'isee'))
    #ser.write(bytearray(b'!183')) 
    time.sleep(1)
    y = ser.readline()
    print(y)




#Hornet

import serial
import time
class SerialRead:
    def getConvectronP():
        ser = serial.Serial(
            port='COM5',
            baudrate = 19200,
            parity='N',
            stopbits=1,
            bytesize=8,
            timeout=1
        )
        ser.write(bytearray(b'#01RDCG1\r'))
        value = ser.readline()
        pressure = value[4:-1]
    
        return pressure

    def getIonP():
        ser = serial.Serial(
            port='COM5',
            baudrate = 19200,
            parity='N',
            stopbits=1,
            bytesize=8,
            timeout=1
        )
        ser.write(bytearray(b'#01RD\r'))
        value = ser.readline()
        pressure = value[4:-1]
    
        return pressure
    
    def getUnit():
        ser = serial.Serial(
            port='COM5',
            baudrate = 19200,
            parity='N',
            stopbits=1,
            bytesize=8,
            timeout=1
        )
        ser.write(bytearray(b'#01RU\r'))
        value = ser.readline()
    
        return value[4:-1]






    try:
    except KeyboardInterrupt:
        ser.close()
        print("Closing COM5"


port = "COM5"

with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Timestamp', 'IG Pressure [Torr]','CG Pressure'])
    csvwriter.writerow([set_angle, time_ms, voltage])



try:
    ser = Hornet.openSerial()
    #print....
    
    
except KeyboardInterrupt:
    ser.close()
    print("Closing COM5 port")



filename = "Pressurelog.csv"
with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Timestamp','CGPressure(Torr)','IGPressure(Torr)'])
try:
    while True:
        now = dt.now()
        csvwriter.writerow([now.strftime('%Y%m%d'+'T'+'%H%M%S'),Hornet.getConvectronP(), Hornet.getIonP()])
        time.sleep(1)
        
except KeyboardInterrupt:
    exit()
    print("Exiting")




#final

        
with open(filename, 'a') as csvfile:
    headers = ['Timestamp','CGPressure(Torr)','IGPressure(Torr)']
    writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n',fieldnames=headers)
    if fileEmpty:
        writer.writeheader() 

    try:
        while True:
            now = dt.now()
            csvwriter.writerow([now.strftime('%Y%m%d'+'T'+'%H%M%S'),Hornet.getConvectronP(), Hornet.getIonP()])
            time.sleep(1)
        
    except KeyboardInterrupt:
        exit()
        print("Exiting")


#log to csv
filename = "Pressurelog.csv"
with open(filename, 'a') as csvfile:
    csvwriter = csv.writer(csvfile)
    #csvwriter.writerow(['Timestamp','CGPressure(Torr)','IGPressure(Torr)'])
    try:
        while True:
            now = dt.now()
            csvwriter.writerow([now.strftime('%Y%m%d'+'T'+'%H%M%S'),Hornet.getConvectronP(), Hornet.getIonP()])
            print(now.strftime('%Y%m%d'+'T'+'%H%M%S'),Hornet.getConvectronP(), Hornet.getIonP())
            time.sleep(1)
        
    except KeyboardInterrupt:
        exit()
        print("Exiting, Saving to Pressurelog.csv")

