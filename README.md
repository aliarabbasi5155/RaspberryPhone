# Raspberry Phone
A simple Raspberry-Pi-Based phone with 4 operations: making calls,receiving calls,sending messages,receiving messages.This project completely has been made under educational purposes.

## Requirements
- 1 x Raspberry Pi 3 B
- 1 x Sim800c (or other compatible Simxxx module)
- 1 x Character LCD 16x2
- 1 x Microphone

### Optional (For notification light):
- 1 x LED
- 1 x Ressistance

## Circuit Diagram
### Here you can see the complete RP diagram 
![alt text](https://github.com/aliarabbasi5155/RaspberryPhone/blob/master/RaspberryPhone.jpg)

## Working Procedure
Basically it's inital release of RP and it has made under educational purposes as above mentioned.
It needs a physical keyboard to work properly but you can attach a keypad if you want.
If you want to use RP in Full-Feature mode you should run `RaspberryPhone.py` file with  su previlages but if you want to check each feature seperately you can run these files:

`MakeCall.py` --> To call others

`ReceiveCall.py` --> To receive call from others

`SendMessage.py` --> To send messages to others

`ReceiveMessage.py` --> To receive messages from others

