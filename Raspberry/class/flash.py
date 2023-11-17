from machine import I2C, UART, Pin
import time


class LegPack:
    def __init__(self, id, i2c, addr, deltas1, deltas2, deltas3):
        self.id = id
        self.i2c = i2c
        self.addr = addr
        self.legs = [Leg(0+id, i2c, addr, deltas1), Leg(2+id, i2c, addr, deltas2), Leg(4+id, i2c, addr, deltas3)]

    def setLegArtAngle(self, idLeg, artId, angle):
        self.legs[idLeg].setArtAngle(artId, angle)

    def addLegArtAngle(self, idLeg, artId, angle):
        self.legs[idLeg].addArtAngle(artId, angle)
    
    def setLegArtsAngles(self, idLeg, angles):
        self.legs[idLeg].setArtAngles(angles)
    
    def addLegArtsAngles(self, idLeg, angles):
        self.legs[idLeg].addArtAngles(angles)
    
    def setLegsArtsAngles(self, angles):
        for i in range(0, len(angles)):
            self.setLegArtsAngles(i, angles[i])

    def addLegsArtsAngles(self, angles):
        for i in range(0, len(angles)):
            self.addLegArtsAngles(i, angles[i])

    def setLegsArtAngle(self, artId, angle):
        for i in range(0, len(self.legs)):
            self.setLegArtAngle(i, artId, angle)

    def addLegsArtAngle(self, artId, angle):
        for i in range(0, len(self.legs)):
            self.addLegArtAngle(i, artId, angle)
    
    def setSameLegsArtsAngles(self, angles):
        for i in range(0, len(self.legs)):
            self.setLegArtsAngles(i, angles)
    
    def writeLegsArtsAngles(self):
        for i in range(0, len(self.legs)):
            self.legs[i].writeArtAngles()

# Class leg of the robot
class Leg:
    def __init__(self, id, i2c, addr, deltas):
        self.id = id
        self.arts = [Art(deltas[0]), Art(deltas[1]), Art(deltas[2])]
        self.i2c = i2c
        self.addr = addr

    def setArtAngle(self, id, angle):
        self.arts[id].setAngle(angle)

    def addArtAngle(self, id, angle):
        self.arts[id].addAngle(angle)
    
    def setArtAngles(self, angles):
        for i in range(0, len(angles)):
            self.setArtAngle(i, angles[i])

    def addArtAngles(self, angles):
        for i in range(0, len(angles)):
            self.addArtAngle(i, angles[i])
    
    def writeArtAngles(self):
        command = "m"+str(self.id)+':'+str(self.arts[0].angle)+":"+str(self.arts[1].angle)+":"+str(self.arts[2].angle)+"e";
        #print(command);
        self.i2c.writeto(self.addr[0 if self.id<=2 else 1], command)
        time.sleep(0.1)


# Class articulation of the leg
class Art:
    def __init__(self, delta):
        self.delta = delta
        self.angle = 0
    
    def setAngle(self, angle):
        self.angle = angle + self.delta

    def addAngle(self, angle):
        self.angle = self.angle + angle + self.delta






# main code

#init uart
camUart = UART(1, baudrate=115200, tx=Pin(8), rx=Pin(9))
bluUart = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17))

#init I2C
i2c = I2C(0, freq=100000)
addr = i2c.scan()
print(addr)


#variables
step = 0
iAnim = 0
timer = 0
playedAnim = "stay"
AnimList = {
    "stay":[
        [   [10,70,-60],       [10,70,-60]     ]
    ],
    "forward":[
        [   [-20, 90, -20],    None            ],
        [   [20, 90, -20],     [-20, 50, -30]  ],
        [   [20, 50, -30],     None            ],
        [   None,              [-20, 90, -20]  ],
        [   [-20, 50, -30],    [20, 90, -20]   ],
        [   None,              [20, 50, -30]   ]
    ],
    "backward":[
        [   [20, 90, -20],      None            ],
        [   [-20, 90, -20],     [20, 50, -30]   ],
        [   [-20, 50, -30],     None            ],
        [   None,               [20, 90, -20]   ],
        [   [20, 50, -30],      [-20, 90, -20]  ],
        [   None,               [-20, 50, -30]  ]
    ],
    "right":[
        [   [-20, 90, -20],    None             ],
        [   [20, 90, -20],     [20, 50, -30]    ],
        [   [20, 50, -30],     None             ],
        [   None,              [20, 90, -20]    ],
        [   [-20, 50, -30],    [-20, 90, -20]   ],
        [   None,              [-20, 50, -30]   ]
    ],
    "left":[
        [   [20, 90, -20],    None              ],
        [   [-20, 90, -20],     [-20, 50, -30]  ],
        [   [-20, 50, -30],     None            ],
        [   None,              [-20, 90, -20]   ],
        [   [20, 50, -30],    [20, 90, -20]     ],
        [   None,              [20, 50, -30]    ]
    ]
}

legPacks = [LegPack(0, i2c, addr, [0,0,0], [0,0,0], [0,0,0]),
            LegPack(1, i2c, addr, [0,0,0], [0,0,0], [0,0,0])]


def playStepAnim():
    global playedAnim, iAnim
    print(playedAnim, iAnim)
    newPos = AnimList[playedAnim][iAnim]

    if newPos[0]:
        if playedAnim == "left" or playedAnim == "right":
            legPacks[0].setLegArtsAngles(0, newPos[0])
            legPacks[0].setLegArtsAngles(1, newPos[0])
            legPacks[0].setLegArtsAngles(2, [-(newPos[0][0]), newPos[0][1], newPos[0][2]])
        else:
            legPacks[0].setSameLegsArtsAngles(newPos[0])
        legPacks[0].writeLegsArtsAngles()

    if newPos[0] and newPos[1]:
        print("time")
        #time.sleep(0.5)

    if newPos[1]:
        if playedAnim == "left" or playedAnim == "right":
            legPacks[1].setLegArtsAngles(0, [-(newPos[1][0]), newPos[1][1], newPos[1][2]])
            legPacks[1].setLegArtsAngles(1, newPos[1])
            legPacks[1].setLegArtsAngles(2, newPos[1])
        else:
            legPacks[1].setSameLegsArtsAngles(newPos[1])
        legPacks[1].writeLegsArtsAngles()

    iAnim = 0 if iAnim == len(AnimList[playedAnim])-1 else iAnim+1


# playedAnim = "right"
# while True:
#     timer+=1
#     if timer >= 1000:
#         playStepAnim()
#         timer = 0


playedAnim = "stay"
time.sleep(1)
while True:
    lastAnim = playedAnim
    msg = camUart.read()
    if not msg:
        msg = bluUart.read()
    
    if msg == b'left':
        print("turn left")
        step = 3
    elif msg == b'right':
        print("turn right")
        step = 4
    elif msg == b'up':
        print("forward")
        step = 1
    elif msg == b'down':
        print("backward")
        step = 2
    elif msg == b'stop':
        print("stop")
        step = 0
    
    if step == 0:
        playedAnim = "stay"
    elif step == 1:
        playedAnim = "forward"
    elif step == 2:
        playedAnim = "backward"
    elif step == 3:
        playedAnim = "left"
    elif step == 4:
        playedAnim = "right"
    
    if lastAnim != playedAnim:
        iAnim = 0
    playStepAnim()
