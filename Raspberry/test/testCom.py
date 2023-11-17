from machine import Pin, Timer, UART
import time

NB_LEGS = 3

uart = UART(0, 9600)                         # init with given baudrate
uart.init(9600, bits=8, parity=None, stop=2) # init with given parameters
led = Pin("LED", Pin.OUT)


stepAnim = 0
listAnim = [[-40,0,-20],
            [-40,30,20],
            [-10,30,20],
            [-10,0,-20],]


#uart.write('m1:0:50:50e')


while True:
    for i in range(NB_LEGS):
        command = 'm'+str(i)+':'+str(listAnim[stepAnim][0])+':'+str(listAnim[stepAnim][1])+':'+str(listAnim[stepAnim][2])+'e'
        print(command)
        uart.write(command)
    stepAnim = stepAnim+1 if stepAnim < len(listAnim)-1 else 0
    print(stepAnim)
    time.sleep(1)




'''
led = Pin(21, Pin.OUT)
led2 = Pin(20, Pin.OUT)
timer = Timer()

def blink(timer):
    led.toggle()
    led2.toggle()

timer.init(freq=2.5, mode=Timer.PERIODIC, callback=blink)
'''
