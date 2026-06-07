#Serial connection

import serial
import time


#device port
port = "/dev/ttyUSB0"


with open ("serial_test_log.txt", "w") as f:
    f.write("Checking Processes")

with serial.Serial(port, baudrate=115200, bytesize=8,stopbits=serial.STOPBITS_ONE,timeout =1) as ser:
    print(ser.name)



    while(True): 
        #wait 10 seconds
        time.sleep(10)
        # write the ps command to the serial port
        ser.write(b"ps \r\n")

        # read until it sees ps
        ser_string = ser.read_until(b"ps")
        # print the result
        print(ser_string.decode("Ascii")) 

        # write the result to the log file
        with open("serial_test_log.txt", "a") as log_file:
            log_file.write(ser_string.decode("Ascii"))


