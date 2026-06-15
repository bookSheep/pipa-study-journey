"""
Learning Python from a foundation in Powershell isn't too bad with the plethora or resources available.
If something didn't work I'd ask claude why, but then figure out on my own from the old school way of learning, which
in my opinion is lookin a someone else's code in stackOverflow, general google, and then the book 
"Automate The Boring Stuff with Python by Al Sweigart (3rd edition) ;)

The embedded Linux on this TP-Link router is locked down, can't do much without core utilities.
Here I need to interrupt the Linux boot process to get into the Das U-Boot bootloader shell.
From there I can start doing some better enumeration.

So, this is a python script to reboot the router that is connected to my Kali Linux vm via UART,
Spams "tpl", which is needed to get into the U-Boot shell, and then reads back out the serial output
to tell me whether I'm in a U-Boot shell or not. I might need to clean that up a bit more because the 
U-Boot banner gets printed on every router reboot so I need to differentiate between a banner message and being 
in a U-boot shell.
"""

import serial
import time

port = "/dev/ttyUSB0"

#Open serial connection
ser = serial.Serial(port, baudrate=115200, bytesize=8,stopbits=serial.STOPBITS_ONE,timeout=1)

# clear out serial buffer
ser.reset_output_buffer()
ser.reset_input_buffer()


# send the reboot command
ser.write(b"reboot \r\n")

# pause for 1/2 second

time.sleep(0.5)

# for loop to spam the tpl command

for i in range (0, 1000):
    ser.write(b"tpl \r\n")

# read back the output afterward to see if it landed into the U boot cli
ser_string = ser.read_until(b"U-Boot")
print(ser_string.decode("Ascii"))