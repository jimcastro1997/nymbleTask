"""
Python Side code for UART Communication Task

This program is created for Nymble Firmware Engineer Role Task

Program Developed by Jim Castro Soman
"""

#Import Libirary
import serial
import time

def start_com():
    try:
        com_port = 'COM9'
        baud_rate = 2400
        message = "Hello World - Jim #"

        ser = serial.Serial(com_port, baud_rate)
        time.sleep(2)

        print("Starting...")

        # Sending data to MCU
        data_size_in_bits = len(message.encode()) * 8  # Total bits

        for char in message:
            ser.write(char.encode()) # Send Data
        print("Data Sent - Done")

        time.sleep(2)

        # Receiving data
        print("Data Receiving...")

        received_data = ""
        data_size_received = 0
        start_time = time.time()

        while True:
            if ser.in_waiting > 0: # Waiting for Data
                char = ser.read().decode()
                received_data += char
                data_size_received += len(char.encode()) * 8
                # Check End of Message
                if char == "#":
                    print("Data Received - Done")
                    print(received_data)
                    break

    finally:
        try:
            ser.close()
        except:
            pass

start_com()