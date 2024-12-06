"""
This is a UI developed for UART Communication, which will send message to MCU
& Display the received message from MCU

This program is created for Nymble Firmware Engineer Role Task

Program Developed by Jim Castro Soman
"""

#Import Libirary
import tkinter as tk
from tkinter import messagebox
import serial
import time
import threading

# Function for Bits Per Second Calculation
def calc_speed(start_time, bits_transferred):
    time_elapsed = time.time() - start_time  # time from start to current
    if time_elapsed > 0:
        return bits_transferred / time_elapsed  # sending Bits per sec
    return 0

# Main Function for Sending & Receiving Data
def start_com():
    try:
        com_port = com_port_entry.get()
        baud_rate = int(baud_rate_entry.get()) # Convert to Int
        message = message_text.get("1.0", tk.END).strip() # Get Message

        # Replace special characters with ASCII equivalents
        message_ascii = message.replace("“", "\"").replace("”", "\"").replace("’", "'").replace("‘", "'") + '#'

        ser = serial.Serial(com_port, baud_rate) # UART Communication Init
        time.sleep(2) # Pause for 2 sec [Not necessary] Just for UI

        notification_label.config(text="START", fg="blue")
        window.update()

        # Sending data to atmega328
        data_size_in_bits = len(message_ascii.encode()) * 8  # Total bits
        start_time = time.time()

        for char in message_ascii:
            ser.write(char.encode()) # Send Data
            send_speed = calc_speed(start_time, data_size_in_bits) # Calculating Bits/Sec
            send_speed_label.config(text=f"Sending Speed: {send_speed:.2f} bits/second")
            window.update()

        notification_label.config(text="DATA SENT - OK", fg="green")
        window.update()

        # Receiving data
        notification_label.config(text="Receiving Data", fg="blue")
        window.update()

        received_data = ""
        data_size_received = 0
        start_time = time.time()

        while True:
            if ser.in_waiting > 0: # Waiting for Data
                char = ser.read().decode()
                received_data += char
                data_size_received += len(char.encode()) * 8
                receive_speed = calc_speed(start_time, data_size_received)
                receive_speed_label.config(text=f"Receiving Speed: {receive_speed:.2f} bits/second")
                window.update()

                # Check End of Message
                if char == "#":
                    break

        notification_label.config(text="DATA RECEIVED - OK", fg="green")

        # Strip the '#' character
        received_message_text.config(state="normal")
        received_message_text.delete("1.0", tk.END)
        received_message_text.insert(tk.END, received_data.rstrip("#"))  # Remove the '#' from the end
        received_message_text.config(state="disabled")
        window.update()

    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        try:
            ser.close()
        except:
            pass


# GUI
window = tk.Tk()
window.title("UART Communication GUI")
window.geometry("500x500")

# COM Port Entry
com_port_label = tk.Label(window, text="COM Port:")
com_port_label.pack()
com_port_entry = tk.Entry(window)
com_port_entry.pack()

# Baud Rate Entry
baud_rate_label = tk.Label(window, text="Baud Rate:")
baud_rate_label.pack()
baud_rate_entry = tk.Entry(window)
baud_rate_entry.pack()

# Message to be Sent to Atmega328
message_label = tk.Label(window, text="Message:")
message_label.pack()
message_text = tk.Text(window, height=5, width=50, wrap="word")
message_text.pack()

# Notification
notification_label = tk.Label(window, text="", font=("Helvetica", 14))
notification_label.pack()

# Sending Speed Notification
send_speed_label = tk.Label(window, text="Sending Speed: 0 bits/second", font=("Helvetica", 12))
send_speed_label.pack()

# Receiving Speed Notification
receive_speed_label = tk.Label(window, text="Receiving Speed: 0 bits/second", font=("Helvetica", 12))
receive_speed_label.pack()

# Received Message Text
received_message_label = tk.Label(window, text="Received Message:", font=("Helvetica", 12))
received_message_label.pack()
received_message_text = tk.Text(window, height=5, width=50, wrap="word", state="disabled")
received_message_text.pack()

# Start Button
start_button = tk.Button(window, text="Start", command=start_com)
start_button.pack()

window.mainloop()
