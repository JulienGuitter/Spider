from machine import I2C, UART, Pin
import time

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

    if newPos[1]:
        if playedAnim == "left" or playedAnim == "right":
            legPacks[1].setLegArtsAngles(0, [-(newPos[1][0]), newPos[1][1], newPos[1][2]])
            legPacks[1].setLegArtsAngles(1, newPos[1])
            legPacks[1].setLegArtsAngles(2, newPos[1])
        else:
            legPacks[1].setSameLegsArtsAngles(newPos[1])
        legPacks[1].writeLegsArtsAngles()

    iAnim = 0 if iAnim == len(AnimList[playedAnim])-1 else iAnim+1


playedAnim = "stay"
time.sleep(1)
while True:
    lastAnim = playedAnim
    msg = camUart.read()
    if not msg:
        msg = bluUart.read()
    
    #execute action from msg
    
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