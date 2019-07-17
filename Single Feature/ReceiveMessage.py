import serial
import RPi.GPIO as GPIO      
import os, time
import re
# Find a suitable character in a text or string and get its position
def find(str, ch):
    for i, ltr in enumerate(str):
        if ltr == ch:
            yield i
 
GPIO.setmode(GPIO.BOARD)  
 
# Enable Serial Communication
port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)
 
# Transmitting AT Commands to the Modem
# '\r\n' indicates the Enter key
srng='AT'+'\r\n'
port.write(srng.encode())
srng="\x0D\x0A"
port.write(srng.encode())
rcv = port.read(10)
print('Transmitting AT Commands to the Modem')
print (rcv)
time.sleep(1)

srng='ATE0'+'\r\n'
port.write(srng.encode())              # Disable the Echo
rcv = port.read(10)
print('Disable the Echo')
print (rcv)
time.sleep(1)

srng='AT+CMGF=1'+'\r\n'
port.write(srng.encode())           # Select Message format as Text mode 
rcv = port.read(10)
print('Select Message format as Text mode')
print (rcv)
time.sleep(1)

srng='AT+CNMI=2,1,0,0,0'+'\r\n'
port.write(srng.encode())           # New SMS Message Indications
rcv = port.read(10)
print('New SMS Message Indications')
print (rcv)
time.sleep(1)

ck=1
while ck==1:
    rcv = port.read(10)
    #print (rcv)
    fd=rcv
    if len(rcv)>3:                   # check if any data received 
        print('Loading New Message')
        ck=12
        for i in range(5):            
            rcv = port.read(10)
            #print (rcv)
            fd=fd+rcv                 # Extract the complete data 
 
# Extract the message number shown in between the characters "," and '\r'
        #print(str(fd))
        p=list(find(str(fd), ","))
        q=list(find(str(fd), '\r'))
        MsgNo=re.search(r'\d+', str(fd)).group() 
        print(str(fd))
# Read the message corresponds to the message number
        srng='AT+CMGR='+str(MsgNo)+'\r\n'
        rd=port.write(srng.encode())
        msg=''
        SmsContent=''
        for j in range(10):
            rcv = port.read(20)
            strrcv=str(rcv)
            if j == 1:
                SmsSender=str('+'+str(re.search(r'\d+', strrcv).group()))
                #print(SmsSender)
            if j == 2:
                SmsTime=strrcv[4:len(strrcv)-2]
                #print(SmsTime)
            if j > 2:
                SmsContent=SmsContent+strrcv[2:len(strrcv)-1]
                #print(SmsContent)
            #print(str(j))
            #print(str(rcv))
            msg=msg+str(rcv)
        SmsContent=SmsContent[SmsContent.index('n')+1:len(SmsContent)-14]
        #print(SmsContent)
        #print (msg)
    time.sleep(0.1)
print('New Message Recieved')
print('Sender: '+SmsSender)
print('Time: '+SmsTime)
print('Content: '+SmsContent)
