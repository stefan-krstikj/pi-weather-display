# Driver for the LCD Display 16x2
# Created by Stefan Krstikj
# st.krstic@gmail.com
# 15.02.2019

from time import *
import smbus

address = 0x3f # alternative address is 0x27
num_lines = 2 # number of lines on the device
num_chars = 16 # number of characters per line
centered = 0 # 0 - Not centered, 1 - Centered

# Device constants
CHR = 1 # Mode - Sending data
CMD = 0 # Mode - Sending command
# Device addressesses (refer to the data sheet)
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

    i2c.write_byte(address, bitsHigh)
    sleep(eDelay)
    i2c.write_byte(address, (bitsHigh | 0b00000100)) # 0b00000100: enable
    sleep(ePulse)
    i2c.write_byte(address, (bitsHigh & ~0b00000100))
    sleep(eDelay)
    i2c.write_byte(address, bitsLow)
    sleep(eDelay)
    i2c.write_byte(address, (bitsLow | 0b00000100))
    sleep(ePulse)
    i2c.write_byte(address, (bitsLow & ~0b00000100))
    sleep(eDelay)

def setBacklightOn():
    i2c.write_byte(address, backlightOn)
    sleep(eDelay)

def setBacklightOff():
    i2c.write_byte(address, backlightOff)
    sleep(eDelay)

def clear():
    sendByte(0x01, CMD)

def calculateCentered(message):
    if len(message) >= 16:
        return message
    empty_spaces = 16 - len(message)
    left_spaces = empty_spaces / 2
    final_message = " " * int(left_spaces) + message
    return final_message

def printString(message, line):
    printing_line = line
    printing_message = message
    if line == 1:
        printing_line = line1
    elif line == 2:
        printing_line = line2
    elif line == 3:
        printing_line = line3
    elif line == 4:
        printing_line = line4
    if centered == 1:
        printing_message = calculateCentered(message)
    printing_message = printing_message.ljust(num_chars, " ")
    sendByte(printing_line, CMD)
    for i in range(num_chars):
        sendByte(ord(printing_message[i]), CHR)
        
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
