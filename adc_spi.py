import RPi.GPIO as GPIO
import time
import spidev
from matplotlib import pyplot as plt

class Button():
    def __init__(self,pin,pull_up=True,bouncetime=20):
        if pull_up:
            pull_up=GPIO.PUD_UP
            self.edge = GPIO.FALLING
            self.edge_p = GPIO.RISING
        else:
            pull_up=GPIO.PUD_DOWN
            self.edge = GPIO.RISING
            self.edge_p = GPIO.FALLING
            
        self.bouncetime = bouncetime
            
        self.init_button(pin,pull_up,bouncetime)
    def init_button(self,pin,pull_up=True,bouncetime=20):
        GPIO.setup(pin,GPIO.IN,pull_up_down=pull_up)
        GPIO.add_event_detect(pin,self.edge,callback=self.on,
                              bouncetime=bouncetime)

        self.button_state = None
        self.button_change = None
        self.button_pin = pin
    def on(self,foo):
        self.button_state = 1
        self.button_change = 1
        GPIO.add_event_detect(self.button_pin,GPIO.RISING,callback=self.off,
                              bouncetime=self.bouncetime)
    def off(self,foo):
        self.button_state = 0
        self.button_change = 1
    def reset(self):
        self.change_status = 0

class ADC():
    def __init__(self,sgl=False,odd=False,msbf=True,
                 dev=(0,0),bits=10)

        # Open device
        self.spi = spidev.SpiDev()
        self.spi.open(*dev)

        # Setup
        self.set_init(sgl,odd,msbf)

        #self.bits = bits
        #self.msbf = True
        #if not msbf:
        #    self.bits += 10
            
    def set_init(sgl,odd,msbf):
        # MCP3002 setup options
        SGL  = 0x1 << 2
        ODD  = 0x1 << 3
        MSBF = 0x1 << 4
        
        self.init_wrd = 0x1 << 1
        if sgl: self.init_wrd += SGL
        if odd: self.init_wrd += ODD
        if msbf:
            self.msbf = True
            self.init_wrd += MSBF
        else: self.msbf = False
            
    def get_conversion(self):
        init = [self.init_wrd,0x0]
        if not self.msbf:
            send.append(0x0)
        output = self.spi.xfer2(init)
        return self.parse(output)

    def parse(self,output):
        result = output.pop()
        result += output.pop() << 8
        return result

class Oscilloscope(Button):
    def __init__(self,adc,pull_up=True,bouncetime=20,trig_pin):
        self.timeout = timeout
        self.adc = adc

        if pull_up:
            pull_up=GPIO.PUD_UP
            self.edge = GPIO.FALLING
            self.edge_p = GPIO.RISING
        else:
            pull_up=GPIO.PUD_DOWN
            self.edge = GPIO.RISING
            self.edge_p = GPIO.FALLING
            
        self.bouncetime = bouncetime
            
        self.init_button(trig_pin,pull_up,bouncetime)

        self.fig, self.sub = plt.subplots()
    def get_pt(self):
        pass
    def plot(self,freq):
        pass
        
        
        

GPIO.setmode(GPIO.BCM)
adc = ADC()

# doo stuff
            
GPIO.cleanup()
