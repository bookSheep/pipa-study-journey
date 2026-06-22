
"""These commands are to be run on the kali linux vm that the router is connected to via UART
sudo atftpfd --daemon (this starts the tftp server)
"""
import serial
import time


port = "/dev/ttyUSB0"
ser = serial.Serial(port, baudrate=115200, bytesize=8,stopbits=serial.STOPBITS_ONE,timeout=1)



def send_command(cmd):
    ser.write((cmd + " \r\n").encode("utf-8"))
    time.sleep(1)
    response = ser.read_all()
    print(response.decode("ascii", errors="replace"))
    return response

# Shell wakes up by sending an 'Enter' to confirm sitting at a shell prompt
send_command("")
time.sleep(2)

#List of commands to send to get the full busybox binary

send_command("cd /var/tmp")
send_command("mkdir _tools")
send_command("cd _tools")
send_command("tftp -r busybox-mipsel -g 192.168.0.101")
send_command("chmod +x busybox-mipsel")
send_command("ls -l")
