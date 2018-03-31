# I2C LCD library for LoPy board
# Ported from Adafruit_Python_SSD1306 library by Dmitrii (dmitryelj@gmail.com)
# v0.4 beta

# Display types
kDisplayI2C128x32 = 1
kDisplayI2C128x64 = 2 
kDisplaySPI128x32 = 3 # not tested
kDisplaySPI128x64 = 4

from machine import I2C
from machine import SPI
from machine import Pin
import time

# I2C OLED Wiring: standard
i2c = None

# SPI OLED Wiring: 
# D0 - P10 (CLK)
# D1 - P11 (MOSI)
# DC - P23
# RST - P22
# CS - not used (for some displays needs to be connected with GND)
spi = None
DC_PIN   = Pin('P23', mode=Pin.OUT)
RST_PIN = Pin('P22', mode=Pin.OUT)

# LCD Control constants
SSD1306_I2C_ADDRESS = 0x3C  
SSD1306_SETCONTRAST = 0x81
SSD1306_DISPLAYALLON_RESUME = 0xA4
SSD1306_DISPLAYALLON = 0xA5
SSD1306_NORMALDISPLAY = 0xA6
SSD1306_INVERTDISPLAY = 0xA7
SSD1306_DISPLAYOFF = 0xAE
SSD1306_DISPLAYON = 0xAF
SSD1306_SETDISPLAYOFFSET = 0xD3
SSD1306_SETCOMPINS = 0xDA
SSD1306_SETVCOMDETECT = 0xDB
SSD1306_SETDISPLAYCLOCKDIV = 0xD5
SSD1306_SETPRECHARGE = 0xD9
SSD1306_SETMULTIPLEX = 0xA8
SSD1306_SETLOWCOLUMN = 0x00
SSD1306_SETHIGHCOLUMN = 0x10
SSD1306_SETSTARTLINE = 0x40
SSD1306_MEMORYMODE = 0x20
SSD1306_COLUMNADDR = 0x21
SSD1306_PAGEADDR = 0x22
SSD1306_COMSCANINC = 0xC0
SSD1306_COMSCANDEC = 0xC8
SSD1306_SEGREMAP = 0xA0
SSD1306_CHARGEPUMP = 0x8D
SSD1306_EXTERNALVCC = 0x1
SSD1306_SWITCHCAPVCC = 0x2

# Scrolling constants
SSD1306_ACTIVATE_SCROLL = 0x2F
SSD1306_DEACTIVATE_SCROLL = 0x2E
SSD1306_SET_VERTICAL_SCROLL_AREA = 0xA3
SSD1306_RIGHT_HORIZONTAL_SCROLL = 0x26
SSD1306_LEFT_HORIZONTAL_SCROLL = 0x27
SSD1306_VERTICAL_AND_RIGHT_HORIZONTAL_SCROLL = 0x29
SSD1306_VERTICAL_AND_LEFT_HORIZONTAL_SCROLL = 0x2A

# Font data. Taken from https://github.com/hsmptg/lcd/blob/master/font.py
font = [
    0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x5F, 0x00, 0x00,
    0x00, 0x07, 0x00, 0x07, 0x00,
    0x14, 0x7F, 0x14, 0x7F, 0x14,
    0x24, 0x2A, 0x7F, 0x2A, 0x12,
    0x23, 0x13, 0x08, 0x64, 0x62,
    0x36, 0x49, 0x56, 0x20, 0x50,
    0x00, 0x08, 0x07, 0x03, 0x00,
    0x00, 0x1C, 0x22, 0x41, 0x00,
    0x00, 0x41, 0x22, 0x1C, 0x00,
    0x2A, 0x1C, 0x7F, 0x1C, 0x2A,
    0x08, 0x08, 0x3E, 0x08, 0x08,
    0x00, 0x80, 0x70, 0x30, 0x00,
    0x08, 0x08, 0x08, 0x08, 0x08,
    0x00, 0x00, 0x60, 0x60, 0x00,
    0x20, 0x10, 0x08, 0x04, 0x02,
    0x3E, 0x51, 0x49, 0x45, 0x3E,
    0x00, 0x42, 0x7F, 0x40, 0x00,
    0x72, 0x49, 0x49, 0x49, 0x46,
    0x21, 0x41, 0x49, 0x4D, 0x33,
    0x18, 0x14, 0x12, 0x7F, 0x10,
    0x27, 0x45, 0x45, 0x45, 0x39,
    0x3C, 0x4A, 0x49, 0x49, 0x31,
    0x41, 0x21, 0x11, 0x09, 0x07,
    0x36, 0x49, 0x49, 0x49, 0x36,
    0x46, 0x49, 0x49, 0x29, 0x1E,
    0x00, 0x00, 0x14, 0x00, 0x00,
    0x00, 0x40, 0x34, 0x00, 0x00,
    0x00, 0x08, 0x14, 0x22, 0x41,
    0x14, 0x14, 0x14, 0x14, 0x14,
    0x00, 0x41, 0x22, 0x14, 0x08,
    0x02, 0x01, 0x59, 0x09, 0x06,
    0x3E, 0x41, 0x5D, 0x59, 0x4E,
    0x7C, 0x12, 0x11, 0x12, 0x7C,
    0x7F, 0x49, 0x49, 0x49, 0x36,
    0x3E, 0x41, 0x41, 0x41, 0x22,
    0x7F, 0x41, 0x41, 0x41, 0x3E,
    0x7F, 0x49, 0x49, 0x49, 0x41,
    0x7F, 0x09, 0x09, 0x09, 0x01,
    0x3E, 0x41, 0x41, 0x51, 0x73,
    0x7F, 0x08, 0x08, 0x08, 0x7F,
    0x00, 0x41, 0x7F, 0x41, 0x00,
    0x20, 0x40, 0x41, 0x3F, 0x01,
    0x7F, 0x08, 0x14, 0x22, 0x41,
    0x7F, 0x40, 0x40, 0x40, 0x40,
    0x7F, 0x02, 0x1C, 0x02, 0x7F,
    0x7F, 0x04, 0x08, 0x10, 0x7F,
    0x3E, 0x41, 0x41, 0x41, 0x3E,
    0x7F, 0x09, 0x09, 0x09, 0x06,
    0x3E, 0x41, 0x51, 0x21, 0x5E,
    0x7F, 0x09, 0x19, 0x29, 0x46,
    0x26, 0x49, 0x49, 0x49, 0x32,
    0x03, 0x01, 0x7F, 0x01, 0x03,
    0x3F, 0x40, 0x40, 0x40, 0x3F,
    0x1F, 0x20, 0x40, 0x20, 0x1F,
    0x3F, 0x40, 0x38, 0x40, 0x3F,
    0x63, 0x14, 0x08, 0x14, 0x63,
    0x03, 0x04, 0x78, 0x04, 0x03,
    0x61, 0x59, 0x49, 0x4D, 0x43,
    0x00, 0x7F, 0x41, 0x41, 0x41,
    0x02, 0x04, 0x08, 0x10, 0x20,
    0x00, 0x41, 0x41, 0x41, 0x7F,
    0x04, 0x02, 0x01, 0x02, 0x04,
    0x40, 0x40, 0x40, 0x40, 0x40,
    0x00, 0x03, 0x07, 0x08, 0x00,
    0x20, 0x54, 0x54, 0x78, 0x40,
    0x7F, 0x28, 0x44, 0x44, 0x38,
    0x38, 0x44, 0x44, 0x44, 0x28,
    0x38, 0x44, 0x44, 0x28, 0x7F,
    0x38, 0x54, 0x54, 0x54, 0x18,
    0x00, 0x08, 0x7E, 0x09, 0x02,
    0x18, 0xA4, 0xA4, 0x9C, 0x78,
    0x7F, 0x08, 0x04, 0x04, 0x78,
    0x00, 0x44, 0x7D, 0x40, 0x00,
    0x20, 0x40, 0x40, 0x3D, 0x00,
    0x7F, 0x10, 0x28, 0x44, 0x00,
    0x00, 0x41, 0x7F, 0x40, 0x00,
    0x7C, 0x04, 0x78, 0x04, 0x78,
    0x7C, 0x08, 0x04, 0x04, 0x78,
    0x38, 0x44, 0x44, 0x44, 0x38,
    0xFC, 0x18, 0x24, 0x24, 0x18,
    0x18, 0x24, 0x24, 0x18, 0xFC,
    0x7C, 0x08, 0x04, 0x04, 0x08,
    0x48, 0x54, 0x54, 0x54, 0x24,
    0x04, 0x04, 0x3F, 0x44, 0x24,
    0x3C, 0x40, 0x40, 0x20, 0x7C,
    0x1C, 0x20, 0x40, 0x20, 0x1C,
    0x3C, 0x40, 0x30, 0x40, 0x3C,
    0x44, 0x28, 0x10, 0x28, 0x44,
    0x4C, 0x90, 0x90, 0x90, 0x7C,
    0x44, 0x64, 0x54, 0x4C, 0x44,
    0x00, 0x08, 0x36, 0x41, 0x00,
    0x00, 0x00, 0x77, 0x00, 0x00,
    0x00, 0x41, 0x36, 0x08, 0x00,
    0x02, 0x01, 0x02, 0x04, 0x02,
    0x3C, 0x26, 0x23, 0x26, 0x3C]  
  
# Display data
width = None
height = None
pages = None
buffer = None  

def isConnected():
    if i2c != None:
        # Check I2C devices
        devices = i2c.scan() # returns list of slave addresses
        for d in devices:
            if d == SSD1306_I2C_ADDRESS: return True
        return False
    else:
        # No check for SPI
        return True

def command1(c):
    if i2c != None:
        i2c.writeto(SSD1306_I2C_ADDRESS, bytearray([0,  c]))
    else:
        DC_PIN.value(0)
        spi.write(bytes([c]))
        
def command2(c1,  c2):
    if i2c != None:
        i2c.writeto(SSD1306_I2C_ADDRESS, bytearray([0,  c1,  c2]))
    else:
        DC_PIN.value(0)
        spi.write(bytes([c1,  c2]))
    
def command3(c1,  c2,  c3):
    if i2c != None:
        i2c.writeto(SSD1306_I2C_ADDRESS, bytearray([0,  c1,  c2,  c3]))
    else:
        DC_PIN.value(0)
        spi.write(bytes([c1,  c2,  c3]))
        
def writeSPIData(data):   
    DC_PIN.value(1) 
    spi.write(bytes(data))        

def initialize(type):  
    global width,  height,  pages,  buffer,  i2c,  spi
    if type == kDisplayI2C128x32:
       #128x32 I2C OLED Display
        width  = 128
        height = 32
        pages = 4 #  height/8
        buffer = [0]*512 # 128*32/8
        i2c = I2C(0, I2C.MASTER, baudrate=100000)
        initialize_128x32()
    if type == kDisplayI2C128x64:
       #128x64 I2C OLED Display
        width  = 128
        height = 64
        pages = 8 #  height/8
        buffer = [0]*1024 # 128*64/8
        i2c = I2C(0, I2C.MASTER, baudrate=100000)
        initialize_128x64()
    if type == kDisplaySPI128x32:
       #128x32 SPI OLED Display
        width  = 128
        height = 32
        pages = 4 #  height/8
        buffer = [0]*512 # 128*32/8
        spi = SPI(0, mode=SPI.MASTER, baudrate=1000000, polarity=0, phase=0, firstbit=SPI.MSB)
        RST_PIN.value(0) 
        time.sleep(0.01)
        RST_PIN.value(1)
        initialize_128x32()
    if type == kDisplaySPI128x64:
       #128x64 SPI OLED Display
        width  = 128
        height = 64
        pages = 8 #  height/8
        buffer = [0]*1024 # 128*64/8
        spi = SPI(0, mode=SPI.MASTER, baudrate=1000000, polarity=0, phase=0, firstbit=SPI.MSB)
        RST_PIN.value(0) 
        time.sleep(0.01)
        RST_PIN.value(1) 
        initialize_128x64()

def initialize_128x32():
    command1(SSD1306_DISPLAYOFF)                    # 0xAE
    command2(SSD1306_SETDISPLAYCLOCKDIV,  0x80)            # 0xD5
    command2(SSD1306_SETMULTIPLEX,  0x1F)                  # 0xA8
    command2(SSD1306_SETDISPLAYOFFSET,  0x0)              # 0xD3
    command1(SSD1306_SETSTARTLINE | 0x0)            # line #0
    command2(SSD1306_CHARGEPUMP,  0x14)                    # 0x8D
    command2(SSD1306_MEMORYMODE,  0x00)                    # 0x20
    command3(SSD1306_COLUMNADDR,  0,  width-1)
    command3(SSD1306_PAGEADDR,  0,  pages-1)
    command1(SSD1306_SEGREMAP | 0x1)
    command1(SSD1306_COMSCANDEC)
    command2(SSD1306_SETCOMPINS,  0x02)                    # 0xDA
    command2(SSD1306_SETCONTRAST,  0x8F)                   # 0x81
    command2(SSD1306_SETPRECHARGE,  0xF1)                  # 0xd9
    command2(SSD1306_SETVCOMDETECT,  0x40)                 # 0xDB
    command1(SSD1306_DISPLAYALLON_RESUME)           # 0xA4
    command1(SSD1306_NORMALDISPLAY)                 # 0xA6
    
def initialize_128x64():
    command1(SSD1306_DISPLAYOFF)                    # 0xAE
    command1(SSD1306_DISPLAYALLON_RESUME)           # 0xA4
    command2(SSD1306_SETDISPLAYCLOCKDIV, 0x80)            # 0xD5
    command2(SSD1306_SETMULTIPLEX,  0x3F)                  # 0xA8
    command2(SSD1306_SETDISPLAYOFFSET,  0x0)              # 0xD3
    command1(SSD1306_SETSTARTLINE | 0x0)            # line #0
    command2(SSD1306_CHARGEPUMP,  0x14)                    # 0x8D
    command2(SSD1306_MEMORYMODE,  0x00)                    # 0x20
    command3(SSD1306_COLUMNADDR,  0,  width-1)
    command3(SSD1306_PAGEADDR,  0,  pages-1)
    command1(SSD1306_SEGREMAP | 0x1)
    command1(SSD1306_COMSCANDEC)
    command2(SSD1306_SETCOMPINS,  0x12)                    # 0xDA
    command2(SSD1306_SETCONTRAST,  0xCF)                   # 0x81
    command2(SSD1306_SETPRECHARGE,  0xF1)                  # 0xd9
    command2(SSD1306_SETVCOMDETECT,  0x40)                 # 0xDB
    command1(SSD1306_NORMALDISPLAY)                 # 0xA6
    command1(SSD1306_DISPLAYON)
        
def set_contrast(contrast):
    # Sets the contrast of the display.  Contrast should be a value between 0 and 255.
    if contrast < 0 or contrast > 255:
        print('Contrast must be a value from 0 to 255 (inclusive).')
    command2(SSD1306_SETCONTRAST,  contrast)
        
def displayOff():
    command1(SSD1306_DISPLAYOFF)
        
def displayOn():
    command1(SSD1306_DISPLAYON)
        
def clearBuffer():
     for i in range(0, len(buffer)): 
         buffer[i] = 0
        
def addString(x,  y,  str):
    symPos = width*y + 6*x
    for i in range(0,  len(str)):
        c = 5*(ord(str[i]) - 32)
        buffer[symPos] = font[c]
        buffer[symPos + 1] = font[c+1]
        buffer[symPos + 2] = font[c+2]
        buffer[symPos + 3] = font[c+3]
        buffer[symPos + 4] = font[c+4]
        symPos += 6
             
def drawBuffer():
    command1(SSD1306_SETLOWCOLUMN)
    command1(SSD1306_SETHIGHCOLUMN)
    command1(SSD1306_SETSTARTLINE)
    #Write display buffer to physical display.
    if spi != None:
        writeSPIData(buffer)
    else:        
        line = [0]*17
        line[0] = 0x40
        for i in range(0, len(buffer), 16):
            for p in range(0, 16): 
                line[p+1] = buffer[i + p]            
            i2c.writeto(SSD1306_I2C_ADDRESS, bytearray(line))  
                
if __name__ == "__main__":
    import sys,  machine,  os

    print("Started")

    displayType = kDisplayI2C128x64
    initialize(displayType)
    if isConnected():
        set_contrast(128) # 1-255
        displayOn()
        clearBuffer()
        addString(0, 0,  sys.platform + " " + sys.version)
        addString(0, 1,  "---")
        addString(0, 2,  "CPU: {} MHz".format(machine.freq()/1000000))
        addString(0, 4,  "Version: {}".format(os.uname().release))
        addString(0, 5,  "LoPy font test")
        addString(0, 6,  "AaBbCcDdEeFfGgHhIi")
        addString(0, 7,  "0123456789012345")
        drawBuffer()
    else:    
        print("Error: LCD not found")

    print("Done")
