import time
import serial
def openSerial():
    ser = serial.Serial(
        port='COM5',
        baudrate = 19200,
        parity='N',
        stopbits=1,
        bytesize=8,
        timeout=1
    )
    return ser

        
def getConvectronP():
    ser = openSerial()
    ser.write(bytearray(b'#01RDCG1\r'))
    value = ser.readline()
    pressure = value[4:-1]
    ser.close()
    return float(pressure)

def getIonP():
    ser=openSerial()
    ser.write(bytearray(b'#01RD\r'))
    value = ser.readline()
    pressure = value[4:-1]

    ser.close()
    return float(pressure)
    
def getUnit():
    ser=openSerial()
    ser.write(bytearray(b'#01RU\r'))
    value = ser.readline()
    ser.close()
    return value[4:-1]