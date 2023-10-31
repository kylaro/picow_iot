import neopixel
import time
import machine

# 32 LED strip connected to X8.
p = machine.Pin(22)
n = neopixel.NeoPixel(p, 16)

def pulse_cyan():
    
    brightness = 0.05
    while brightness > 0:
        # Draw a red gradient.
        #for i in range(16):
            #n[i] = (brightness, 0, brightness)
            
        #    n.write()
        n.fill( (0, int(255*brightness),int(255*brightness) ) )
        n.write()
        brightness -= .001
        time.sleep(0.01)
    
    n.fill( (0,0,0) )
    n.write()
    
def pulse_cyan_small():
    
    brightness = 0.01
    while brightness > 0:
        # Draw a red gradient.
        #for i in range(16):
            #n[i] = (brightness, 0, brightness)
            
        #    n.write()
        n.fill( (int(255*brightness), int(255*brightness),0 ) )
        n.write()
        brightness -= .001
        time.sleep(0.01)
    
    n.fill( (0,0,0) )
    n.write()


def pulse_purple():
    brightness = 0.07
    while brightness > 0:
        # Draw a red gradient.
        #for i in range(16):
            #n[i] = (brightness, 0, brightness)
            
        #    n.write()
        n.fill( (int(255*brightness), 0, int(255*brightness)) )
        n.write()
        brightness -= .0015
        time.sleep(0.01)
    
    n.fill( (0,0,0) )
    n.write()
        
def pulse_green():
    brightness = 0.07
    while brightness > 0:
        # Draw a red gradient.
        #for i in range(16):
            #n[i] = (brightness, 0, brightness)
            
        #    n.write()
        n.fill( (0, int(255*brightness),0) )
        n.write()
        brightness -= .003
        time.sleep(0.01)
    
    n.fill( (0,0,0) )
    n.write()

def pulse_red():
    brightness = 0.07
    while brightness > 0:
        # Draw a red gradient.
        #for i in range(16):
            #n[i] = (brightness, 0, brightness)
            
        #    n.write()
        n.fill( (int(255*brightness),0,0) )
        n.write()
        brightness -= .006
        time.sleep(0.01)
    brightness = 0.1
    while brightness > 0:
        # Draw a red gradient.
        #for i in range(16):
            #n[i] = (brightness, 0, brightness)
            
        #    n.write()
        n.fill( (int(255*brightness),0,0) )
        n.write()
        brightness -= .006
        time.sleep(0.01)
    
    n.fill( (0,0,0) )
    n.write()

