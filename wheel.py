import RPi.GPIO as GPIO
import time

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

class InputQueue():
    def __init__(self,pins,pull_up=True,edge=GPIO.FALLING,
                 bouncetime=20,queue_size=0):
        if pull_up:
            pull_up=GPIO.PUD_UP
        else:
            pull_up=GPIO.PUD_DOWN

        self.bouncetime = bouncetime
        self.edge = edge
        self.queue = Queue(queue_size)

        GPIO.setup(pins,GPIO.IN,pull_up_down=pull_up)
        for pin in pins:
            self.add_pin(pin)
    def add_pin(pin):
        GPIO.add_event_detect(pin,self.edge,callback=self.put,
                                  bouncetime=self.bouncetime)
    def put(self,pin):
        self.queue.put(pin)
    def get():
        return self.queue.get()

class Wheel():
    def __init__(self,pin_a,pin_b,pin_c=None,pull_up=True,bouncetime=20,
                 mod=100):
        if pull_up:
            pull_up=GPIO.PUD_UP
        else:
            pull_up=GPIO.PUD_DOWN

        self.mod = mod

        self.input = InputQueue((pin_a,pin_b),pull_up=pull_up,
                                edge=GPIO.BOTH,bouncetime=bouncetime)
        self.pin_a = pin_a
        self.pin_b = pin_b
        self.pin_c = pin_c
        if pin_c:
            self.input.add_pin(pin_c)

        self.counter = 0
        self.prev = None
        self.button_state = 0
        self.change_flg = [0,0]

    def modify_state(pin):
        if pin == self.pin_c:
            self.button_state = self.button_state ^ 1
            self.change_flg[1] = 1
            return
        if not self.prev:
            self.prev = pin
            return
        if not pin == self.prev:
            if pin == self.pin_a:
                print("[^^^] incrememnt")
                self.counter = self.counter + 1 % self.mod
            if pin == self.pin_b:
                print("[vvv] deincrement")
                self.counter -= self.counter - 1 % self.mod
            self.change_flg[0] = 1
        self.prev = None
            
    def read(self):
        try:
            while True:
                self.modify_state(self.input.get())
        except queue.Empty:
            pass
        
        change_flg = self.change_flg
        self.change_flg = [0,0]
        
        return self.counter,self.button_state,change_flg
        

## class Wheel():
##     def __init__(self,pin_a,pin_b,pin_c=None,pull_up=True,bouncetime=20,
##                  mod=10):
##         if pull_up:
##             pull_up=GPIO.PUD_UP
##             self.edge = GPIO.FALLING
##             self.edge_p = GPIO.RISING
##         else:
##             pull_up=GPIO.PUD_DOWN
##             self.edge = GPIO.RISING
##             self.edge_p = GPIO.FALLING
                        
##         GPIO.setup((pin_a,pin_b),GPIO.IN,pull_up_down=pull_up)
##         GPIO.add_event_detect(pin_a,self.edge,callback=self.incr,
##                               bouncetime=bouncetime)
##         GPIO.add_event_detect(pin_b,self.edge,callback=self.decr,
##                               bouncetime=bouncetime)

##         if pin_c:
##             self.init_button(pin_c,pull_up,bouncetime)

##         self.bouncetime = bouncetime
##         self.button_state = None
##         self.mod = mod
##         self.wheel_state = 0
##         self.counter = 0
##         self.button_change = None
##         self.change_status = None
        
##     def incr(self,foo):
##         print("[^^^]increment")
##         if self.wheel_state < 1:
##             self.wheel_state += 1
##             self.change_status = 1
##         self.counter = (self.counter + self.wheel_state) % self.mod
##     def decr(self,foo):
##         print("[vvv]deincrement")
##         if self.wheel_state > -1:
##             self.wheel_state -= 1
##             self.change_status = 1
##         self.counter = (self.counter + self.wheel_state) % self.mod
##     def read(self):
##         self.reset()
##         return (self.counter,self.button_state)

GPIO.setmode(GPIO.BCM)

wheel = Wheel(27,22,17,bouncetime=40,mod=100)
while True:
    counter,button,change_flg = wheel.read()
    if change_flg:
        print("counter: {}; button: {}".format(*wheel.read()))
        if change_flg[1] == 1:
            break
            
GPIO.cleanup()
