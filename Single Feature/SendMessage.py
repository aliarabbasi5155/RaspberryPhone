import serial
import RPi.GPIO as GPIO      
import os, time
 
GPIO.setmode(GPIO.BOARD)    
 
# Enable Serial Communication
port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)
 
# Transmitting AT Commands to the Modem
# '\r\n' indicates the Enter key
srng='AT'+'\r\n'
port.write(srng.encode())
rcv = port.read(10)
print('Transmitting AT Commands to the Modem')
print (rcv)
time.sleep(1)

srng='ATE0'+'\r\n'
port.write(srng.encode())      # Disable the Echo
rcv = port.read(10)
print('Disable the Echo')
print (rcv)
time.sleep(1)

srng='AT+CMGF=1'+'\r\n'
port.write(srng.encode())  # Select Message format as Text mode 
rcv = port.read(10)
print('Select Message format as Text mode')
print (rcv)
time.sleep(1)
srng='AT+CNMI=2,1,0,0,0'+'\r\n'
port.write(srng.encode())   # New SMS Message Indications
rcv = port.read(10)
print('New SMS Message Indications')
print (rcv)
time.sleep(1)
 
# Sending a message to a particular Number
srng='AT+CMGS="+98918xxxxxxx"'+'\r\n'
port.write(srng.encode())
rcv = port.read(10)
print('Sending a message to a particular Number')
print (rcv)
time.sleep(1)
srng='Hello User'+'\r\n'
port.write(srng.encode())  # Message
rcv = port.read(10)
print('Message')
print (rcv)
srng="\x1A"
port.write(srng.encode()) # Enable to send SMS
for i in range(10):
    rcv = port.read(10)
    print('Enable to send SMS'+str(i))
    print (rcv)
