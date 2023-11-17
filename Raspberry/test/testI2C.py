# from machine import Pin, I2C 
# import time

# print("start")
# MSG_SIZE = 15

# i2c = I2C(0, freq=100000)
# addr = i2c.scan()
# print(addr)
# if(len(addr)):
#     i2c.writeto(addr[0], 'm1:0:50:50e')
#     time.sleep(0.1)

#     print("done")
# else:
#     print("Not connected")






from machine import Pin, I2C
import time

NB_LEGS = 6
MSG_SIZE = 20

i2c = I2C(0, freq=100000)
addr = i2c.scan()


stepAnim = 0
listAnim = [[-40,0,-20],
            [-40,30,20],
            [-10,30,20],
            [-10,0,-20],]


#uart.write('m1:0:50:50e')

print(addr)
if(len(addr)):
    while True:
        for i in range(NB_LEGS):
            command = 'm'+str(i)+':'+str(listAnim[stepAnim][0])+':'+str(listAnim[stepAnim][1])+':'+str(listAnim[stepAnim][2])+'e'
            print(command)
            i2c.writeto(addr[0 if i<=2 else 1], command)
            time.sleep(0.1)
        stepAnim = stepAnim+1 if stepAnim < len(listAnim)-1 else 0
        print(stepAnim)
        time.sleep(1)
        
else:
    print("Not connected")

