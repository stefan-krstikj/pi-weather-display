"""
16x2 I2C Display
Version 1.0.1
DELOARTS Research Inc.
Philip Delorenzo
02.05.2016
"""
import smbus
from time import sleep

# Basic display data (change them for your display)
deviceAddress  = 0x3f   # I2C device address
                        # Use i2cdetect -y 1 to find your lcd
deviceWidth = 16 # Maximum characters per line
# Device constants
CHR = 1 # Mode - Sending data
CMD = 0 # Mode - Sending command
# Device deviceAddressesses (refer to the data sheet)
line1 = 0x80
line2 = 0xC0
line3 = 0x94
line4 = 0xD4
backlightOn = 0x08
backlightOff = 0x00
# Time "delays" for the I2C bus
ePulse = 0.0005
eDelay = 0.0005
# Enable the I2C bus
i2c = smbus.SMBus(1) # Rev 2 Pi uses 1

def init():
    sendByte(0x33, CMD)
    sendByte(0x32, CMD)
    sendByte(0x06, CMD)
    sendByte(0x0C, CMD)
    sendByte(0x2B, CMD)
    sleep(eDelay)
    clear()
    setBacklightOn()

def sendByte(bits, mode):
    # bits = data
    # mode = 1 for data
    #        0 for command
    bitsHigh = mode | (bits & 0xF0) | backlightOn
    bitsLow = mode | ((bits << 4) & 0xF0) | backlightOn

    i2c.write_byte(deviceAddress, bitsHigh)
    sleep(eDelay)
    i2c.write_byte(deviceAddress, (bitsHigh | 0b00000100)) # 0b00000100: enable
    sleep(ePulse)
    i2c.write_byte(deviceAddress, (bitsHigh & ~0b00000100))
    sleep(eDelay)
    i2c.write_byte(deviceAddress, bitsLow)
    sleep(eDelay)
    i2c.write_byte(deviceAddress, (bitsLow | 0b00000100))
    sleep(ePulse)
    i2c.write_byte(deviceAddress, (bitsLow & ~0b00000100))
    sleep(eDelay)

def setBacklightOn():
    i2c.write_byte(deviceAddress, backlightOn)
    sleep(eDelay)

def setBacklightOff():
    i2c.write_byte(deviceAddress, backlightOff)
    sleep(eDelay)

def clear():
    sendByte(0x01, CMD)

def printString(message, line):
    message = message.ljust(deviceWidth, " ")
    sendByte(line, CMD)
    for i in range(deviceWidth):
        sendByte(ord(message[i]), CHR)
        
# print a message in a scrolling effect, if longer than num_cols
# num_cols is the number of characters per string
def printScrollingString(message, line):
    num_cols = 16 # number of lines on the screen
    if(len(message) > num_cols):
        while True:
            printString(message[:num_cols], line)
            sleep(1.5)
            for i in range(len(message) - num_cols + 1):
                text_to_print = message[i:i+num_cols]
                printString(text_to_print, line)
                sleep(0.5)
            sleep(1.5)
    else:
        printString(message, line)
    

if __name__ == "__main__":
    init()
    printString("    DELOARTS    ", line1)
    printString(" 16x2/4 I2C LCD ", line2)