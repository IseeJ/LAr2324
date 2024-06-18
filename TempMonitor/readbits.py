import serial
import time
import datetime

ser = serial.Serial(
    port='COM6', 
    baudrate=19200,
    timeout=1
)

def send_data_hex(data_hex):
    data_bytes = bytes.fromhex(data_hex)  
    ser.write(data_bytes)  
    print(f"Sent: {data_hex}")

def read_bits():
    while True:
        if ser.in_waiting > 0:
            received_data = ser.read(5)  #read 5 bytes (40 bits)
            received_hex = received_data.hex()  ##to hex
            print(f"Received: {received_hex}")
            
            received_int &= 0x1FFFFFFFFF
            
            bit_17 = (received_int >> 17) & 1
            bit_18 = (received_int >> 18) & 1
            
            combined_string = f"{bit_18:02d}{bit_17:02d}"
            decimal_value = int(combined_string, 16)/10
            print(received_hex)
            print("CH1: ", decimal_value)
            
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            """
            with open("data.dat", "a") as file:
                file.write(f"{timestamp}, {bit_17}, {bit_18}\n")
            
            print(f"Logged: {timestamp}, {bit_17}, {bit_18}")
            break 
            """

try:
    #send_data_hex("48656c6c6f2c2053657269616c21")  
    read_bits() 
    time.sleep(1) 
except Exception as e:
    print(f"Error: {e}")
finally:
    ser.close() 
    print("Serial port closed.")
