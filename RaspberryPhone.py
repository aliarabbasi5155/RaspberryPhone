from RPLCD.gpio import CharLCD
import time
import threading
import subprocess as sp
import serial
import RPi.GPIO as GPIO      
import os, time
import re

GPIO.setwarnings(False)

port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)

def find(str, ch):
    for i, ltr in enumerate(str):
        if ltr == ch:
            yield i
            
def Receive():
    lcd.clear();
	# Transmitting AT Commands to the Modem
    # '\r\n' indicates the Enter key
    srng='AT'+'\r\n'
    port.write(srng.encode())
    rcv = port.read(10)
    print('Transmitting AT Commands to the Modem')
    print (rcv)
    time.sleep(1)
    lcd.clear()
    lcd.write_string('Waiting for ring')
    while(1):
        rcv = port.read(10)
        if "RING" in str(rcv):
            print('Ringing...')
            for i in range (10):
                GPIO.output(7,0)
                lcd.clear()
                time.sleep(0.1)
                GPIO.output(7,1)
                lcd.write_string('Ringing...')
                time.sleep(0.1) 
            lcd.clear()
            lcd.write_string('Ringing:1)Answer2)Decline')
            inp = input('1)Answer2)Decline: ')
            if inp == '2':
                srng='AT+HVOIC '+'\r\n'
                port.write(srng.encode())
                rcv = port.read(10)
                print(rcv)
                print('Call Disconnected')
                lcd.clear()
                lcd.write_string('Call Cancelsed!')
                time.sleep(2)
                Main()
                
            if inp == '1':
                srng='ATA'+'\r\n'
                port.write(srng.encode())
                rcv = port.read(10)
                if "OK" in str(rcv):
                    print('Call stablished')
                    lcd.clear()
                    lcd.write_string('Call Connected')
                print (rcv)
                time.sleep(1)
                res=''
                while(1):
                    rcv = port.read(10)
                    print (rcv)
                    time.sleep(1)
                    strrcv = str(rcv)
                    if rcv != "b''":
                        res=res+strrcv[2:len(strrcv)-1]
                    if ('NO CARRIER' in res ):
                        print('NO CARRIER')
                        print('Call Ended')
                        lcd.clear()
                        lcd.write_string('Call Ended!')
                        time.sleep(2)
                        Main()

    Main()
    
def Call():
    lcd.write_string('Enter Phone Number')
    PhoneNumber = input('Enter Phone Number: ')
    lcd.clear()
    lcd.write_string('Calling +'+PhoneNumber)
    srng='AT'+'\r\n'
    port.write(srng.encode())
    rcv = port.read(10)
    print('Transmitting AT Commands to the Modem')
    print (rcv)
    time.sleep(1)

    srng='ATD'+PhoneNumber+';'+'\r\n'
    port.write(srng.encode())
    rcv = port.read(30)
    print (rcv)
    if "OK" in str(rcv):
        lcd.clear()
        lcd.write_string('Call With +'+PhoneNumber)
        print('Call stablished')
    time.sleep(1)
    res=''
    while(1):
        rcv = port.read(10)
        strrcv=str(rcv)
        print('Receiving Data: '+strrcv)
        if rcv != "b''":
            res=res+strrcv[2:len(strrcv)-1]
        if ('NO CARRIER' in res ):
            print('NO CARRIER')
            print('Call Ended')
            lcd.clear()
            lcd.write_string('Call Ended!')
            time.sleep(2)
            Main()
        if ('BUSY' in res ):
            print('BUSY')
            print('Subscriber is Busy!')
            lcd.clear()
            lcd.write_string('Subscriber is Busy!')
            time.sleep(2)
            Main()
        if ('NO ANSWER' in res ):
            print('NO ANSWER')
            print('Subscriber did not answer!')
            lcd.clear()
            lcd.write_string('Subscriber did not answer!')
            time.sleep(2)
            Main()
        if ('NO DIALTONE' in res ):
            print('NO DIALTONE')
            print('NO DIALTONE')
            lcd.clear()
            lcd.write_string('NO DIALTONE')
            time.sleep(2)
            Main()

def SendMessage():
    lcd.write_string('Enter Phone Number')
    PhoneNumber = input('Enter Phone Number: ')
    lcd.clear()
    lcd.write_string('Write Your Text')
    Text = input('Text:')
    lcd.clear()
    lcd.write_string(str(Text))
    time.sleep(4)
    lcd.clear()
    lcd.write_string('Y to continue/N to cancel')
    inp = input('y to continue/n to cancel: ')

    if inp == 'y':
        lcd.clear()
        lcd.write_string('Sending Message!')
	    # Transmitting AT Commands to the Modem
        # '\r\n' indicates the Enter key
        srng='AT'+'\r\n'
        port.write(srng.encode())
        rcv = port.read(10)
        print('Transmitting AT Commands to the Modem')
        print (rcv)
        time.sleep(0.1)
        
        srng='ATE0'+'\r\n'
        port.write(srng.encode())      # Disable the Echo
        rcv = port.read(10)
        print('Disable the Echo')
        print (rcv)
        time.sleep(0.1)
        
        srng='AT+CMGF=1'+'\r\n'
        port.write(srng.encode())  # Select Message format as Text mode 
        rcv = port.read(10)
        print('Select Message format as Text mode')
        print (rcv)
        time.sleep(0.1)
        
        srng='AT+CNMI=2,1,0,0,0'+'\r\n'
        port.write(srng.encode())   # New SMS Message Indications
        rcv = port.read(10)
        print('New SMS Message Indications')
        print (rcv)
        time.sleep(0.1)
        
        # Sending a message to a particular Number
        srng='AT+CMGS="'+PhoneNumber+ '"'+'\r\n'
        port.write(srng.encode())
        rcv = port.read(10)
        print('Sending a message to a particular Number')
        
        print (rcv)
        time.sleep(0.1)
        srng=Text+'\r\n'
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
        lcd.clear()
        lcd.write_string('Message Sent!')
        time.sleep(3)
           
        
    if inp == 'n':
        lcd.clear()
        lcd.write_string('Canceled!')
        time.sleep(3)
    Main()
    
def Inbox():
    # Transmitting AT Commands to the Modem
    # '\r\n' indicates the Enter key
    lcd.clear()
    lcd.write_string('Wait...')
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
    
    lcd.clear()
    lcd.write_string('y for next message n to back')
    time.sleep(2)
    counter=1
    while(1):
        lcd.clear()
        lcd.write_string('Wait...')
        srng='AT+CMGR='+str(counter)+'\r\n'
        rd=port.write(srng.encode())
        msg=''
        SmsContent=''
        for j in range(10):
            rcv = port.read(20)
            
            strrcv=str(rcv)
            if j == 1:
                SmsSender='+'+str(re.search(r'\d+', strrcv).group())
                #print(SmsSender)
            if j == 2:
                print(strrcv)
                SmsTime=strrcv[2:len(strrcv)-4]
                #print(SmsTime)
            if j > 2:
                SmsContent=SmsContent+strrcv[2:len(strrcv)-1]
            msg=msg+str(rcv)
            #print(msg)
        SmsContent=SmsContent[SmsContent.index('n')+1:len(SmsContent)-14]
        print('Sender: '+SmsSender)
        print('Time: '+SmsTime)
        print('Content: '+SmsContent)
        lcd.clear()
        lcd.write_string('From: '+SmsSender)
        time.sleep(2)
        lcd.clear()
        lcd.write_string('Time: '+SmsTime)
        time.sleep(2)
        lcd.clear()
        lcd.write_string('Text: '+SmsContent)
        srng='AT+CNMI=2,1,0,0,0'+'\r\n'
        port.write(srng.encode())           # New SMS Message Indications
        rcv = port.read(10)
        print('New SMS Message Indications')
        print (rcv)
        time.sleep(0.1)
        
        inp = input('y for next n for back to menu: ')
        if inp == 'y':
            counter=counter+1
        if inp == 'n':
            Main()
        
        	
def Main():
    lcd.clear()
    lcd.write_string('1)Call2)Send Msg3)Inbox4)Rcv Call')
    print('1)Call2)Send Msg3)Inbox4)Rcv Call')
    inp = input('Select one: ')
    lcd.clear();
    if inp == '1':
        Call()
    if inp == '2':
        SendMessage()
    if inp == '3':
        Inbox()
    if inp == '4':
        Receive()
	
	

     
lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[40, 38, 36, 32, 33, 31, 29, 23],numbering_mode=GPIO.BOARD)
text=""
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)
for i in range (10):
   GPIO.output(7,0)
   time.sleep(0.1)
   GPIO.output(7,1)
   time.sleep(0.1) 
print('Preparing Device, Pleas Wait')
lcd.write_string("Hi, I'm OneMinus 5t")
time.sleep(2)
lcd.clear();
lcd.write_string("Setting up")
time.sleep(0.5)
lcd.clear();
lcd.write_string("Setting up.")
time.sleep(0.5)
lcd.clear();
lcd.write_string("Setting up..")
time.sleep(0.5)
lcd.clear();
lcd.write_string("Setting up...")
time.sleep(0.5)
lcd.clear();
##lcd.write_string(sp.getoutput('hostname -I'))
##time.sleep(3)

Main()







