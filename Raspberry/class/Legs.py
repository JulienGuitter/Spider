import time

# from machine import I2C 
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