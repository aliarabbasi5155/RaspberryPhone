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

srng='ATD+98918xxxxxxx;'+'\r\n'
port.write(srng.encode())
rcv = port.read(10)
print (rcv)
if "OK" in str(rcv):
	print('Call stablished')
time.sleep(1)
res=''
while(1):
    rcv = port.read(10)
    strrcv=str(rcv)
    print(strrcv)
    if rcv != "b''":
        res=res+strrcv[2:len(strrcv)-1]
        #print('ali0')
        #print('res inside: '+res)
        #print('ali')
    if ('NO CARRIER' in res ):
        print('NO CARRIER')
        print('Call Ended')
        break
    if ('BUSY' in res ):
        print('BUSY')
        print('Subscriber is Busy!')
        break
    if ('NO ANSWER' in res ):
        print('NO ANSWER')
        print('Subscriber did not answer!')
        break
    if ('NO DIALTONE' in res ):
        print('NO DIALTONE')
        print('NO DIALTONE')
        break



