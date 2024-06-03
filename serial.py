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
    
