# I2C LCD Experimental code 
# Was ported from Adafruit_Python_GPIO library by Dmitrii (dmitryelj@gmail.com)
# v0.1 beta

width  = 128
height = 32
pages = 4 #  height/8

from machine import I2C

# i2C LCD Control constants
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

i2c = I2C(0, I2C.MASTER, baudrate=100000)

def command(c):
        i2c.writeto(SSD1306_I2C_ADDRESS, bytearray([0,  c]))

def initialize():
        # 128x32 pixel specific initialization.
        command(SSD1306_DISPLAYOFF)                    # 0xAE
        command(SSD1306_SETDISPLAYCLOCKDIV)            # 0xD5
        command(0x80)                                  # the suggested ratio 0x80
        command(SSD1306_SETMULTIPLEX)                  # 0xA8
        command(0x1F)
        command(SSD1306_SETDISPLAYOFFSET)              # 0xD3
        command(0x0)                                   # no offset
        command(SSD1306_SETSTARTLINE | 0x0)            # line #0
        command(SSD1306_CHARGEPUMP)                    # 0x8D
        command(0x14) #  SSD1306_EXTERNALVCC 0 - 0x10
        command(SSD1306_MEMORYMODE)                    # 0x20
        command(0x00)                                  # 0x0 act like ks0108
        command(SSD1306_SEGREMAP | 0x1)
        command(SSD1306_COMSCANDEC)
        command(SSD1306_SETCOMPINS)                    # 0xDA
        command(0x02)
        command(SSD1306_SETCONTRAST)                   # 0x81
        command(0x8F)
        command(SSD1306_SETPRECHARGE)                  # 0xd9
        command(0xF1) # SSD1306_EXTERNALVCC - 0x22
        command(SSD1306_SETVCOMDETECT)                 # 0xDB
        command(0x40)
        command(SSD1306_DISPLAYALLON_RESUME)           # 0xA4
        command(SSD1306_NORMALDISPLAY)                 # 0xA6
        
def set_contrast(contrast):
        # Sets the contrast of the display.  Contrast should be a value between 0 and 255.
        if contrast < 0 or contrast > 255:
            print('Contrast must be a value from 0 to 255 (inclusive).')
        command(SSD1306_SETCONTRAST)
        command(contrast)
        
def displayOff():
        command(SSD1306_DISPLAYOFF)
        
def displayOn():
        command(SSD1306_DISPLAYON)
        
def display():
        #Write display buffer to physical display.
        command(SSD1306_COLUMNADDR)
        command(0)              # Column start address. (0 = reset)
        command(width-1)     # Column end address.
        command(SSD1306_PAGEADDR)
        command(0)              # Page start address. (0 = reset)
        command(pages-1)    # Page end address.
        # Write buffer data.
        for i in range(0, 32):
            i2c.writeto_mem(SSD1306_I2C_ADDRESS, 0x40, bytearray([255, 255, 255, 255, 0, 0, 0, 0,  255, 255, 255, 255,  0, 0, 0, 0]))
            # To clear display:
            #i2c.writeto_mem(SSD1306_I2C_ADDRESS, 0x40, bytearray([0, 0, 0, 0, 0, 0, 0, 0,  0, 0, 0, 0,  0, 0, 0, 0]))

print("Started")

# configure the I2C bus
res = i2c.scan() # returns list of slave addresses

print("Devices: " + str(res))
if len(res) < 1 or res[0] != SSD1306_I2C_ADDRESS:
    print("Error: LCD not found")
    exit(0)
    
initialize()
set_contrast(128)
displayOn()
display()

print("Done")
