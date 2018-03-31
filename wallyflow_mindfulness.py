# WallyFlow Mindfullnes App
# Python 3.5.3
# Raspberry Pi 3

from os import system
from imp import load_source

import RPi.GPIO as GPIO
import math
import time

#Walabot Parameters
#######################################
# Walabot_SetArenaR - input parameters 
minInCm, maxInCm, resInCm = 10, 150, 5

# Walabot_SetArenaTheta - input parameters
minInDeg, maxInDeg, resInDeg = -45, 45, 5

# Walabot_SetArenaPhi - input parameters
minPhiInDeg, maxPhiInDeg, resPhiInDeg = -90, 90, 10  

#Threshold
threshold = 100


#Mindfullness Parameters
#######################################
#Maximum Stillness Time (in seconds)
maxStillTime = 60 * 10

#Initialize Last Average Position to 0
lastAvgPos = 0

#Minimum Average Change needed to update LAP
minAvgDelta = 60

#Initialize Last Move Time to current time
lastMoveTime = time.time()

#Initialize tEnd to lastMoveTime plus maxStillTime
tEnd = lastMoveTime + maxStillTime

#Initialize Starting Time
startTime = time.time()

#Initialize Movement Count
moveCount = 0

#Configure Raspberry Pi GPIO for LED Strip
#######################################
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
GPIO.output(4,0)
GPIO.setwarnings(False)


class Walabot:
    def __init__(self):
        self.wlbt = load_source('WalabotAPI',
                                '/usr/share/walabot/python/WalabotAPI.py')
        self.wlbt.Init()

    def connect(self):
        print("Connecting...")
        while True:
            try:
                self.wlbt.ConnectAny()
                print("Walabot Connected")
                return
            except self.wlbt.WalabotError as err:
                print("Connecting...")
                time.sleep(1)
        
    def configure(self):
        print("Configuring...")
        time.sleep(1)
        self.wlbt.SetProfile(self.wlbt.PROF_SENSOR)
        self.wlbt.SetArenaR(minInCm, maxInCm, resInCm)
        self.wlbt.SetArenaTheta(minInDeg, maxInDeg, resInDeg)
        self.wlbt.SetArenaPhi(minPhiInDeg, maxPhiInDeg, resPhiInDeg)
        self.wlbt.SetDynamicImageFilter(self.wlbt.FILTER_TYPE_NONE)
        print("Walabot Configured")

    def start(self):
        print("Starting...")
        time.sleep(1)
        while True:
            try:
                self.wlbt.Start()
                print("Walabot Started")
                return
            except self.wlbt.WalabotError as err:
                print("Starting...")
                time.sleep(1)
                
    def calibrate(self):
        print("Calibrating...")
        self.wlbt.StartCalibration()
        while self.wlbt.GetStatus()[0] == self.wlbt.STATUS_CALIBRATING:
            self.wlbt.Trigger()
        print("Calibrated")
        
        
    def getStatusString(self):
        status = self.wlbt.GetStatus()[0]
        if status == 0:
            return "STATUS_DISCONNECTED"
        elif status == 1:
            return "STATUS_CONNECTED"
        elif status == 2:
            return "STATUS_IDLE"
        elif status == 3:
            return "STATUS_SCANNING"
        elif status == 4:
            return "STATUS_CALIBRATING"

    def getTargets(self):
        self.wlbt.Trigger()
        return self.wlbt.GetSensorTargets()
    
    def printSensorTarget(self,target):
            print('Target:\nx: {}\ny: {}\nz: {}\namplitude: {}\n'.format(
                target.xPosCm, target.yPosCm, target.zPosCm, target.amplitude))

    def stopAndDisconnect(self):
        print("Stopping..")
        time.sleep(1)
        self.wlbt.Stop()
        self.wlbt.Disconnect()
        print("Disconnected")

        
    def WallyFlow(self):
        global lastAvgPos, lastMoveTime, tEnd, moveCount
        
        targets = wlbt.getTargets()
        currAvgPos = 0
        count = len(targets)        


        if count != 0:
            mainTarget = max(targets, key = lambda t: t[3])
            angle = math.degrees(math.atan(mainTarget.yPosCm/mainTarget.zPosCm))
            currAvgPos += abs(angle)
            currAvgDelta = abs(currAvgPos - lastAvgPos)
            
            if currAvgDelta > minAvgDelta:
                lastMoveTime = time.time()
                tEnd = lastMoveTime + maxStillTime
                moveCount += 1
                lastAvgPos = currAvgPos
                print("Moved. Delta: ", currAvgDelta)
                return currAvgDelta
            else:
                return 0
        else:
            return 0

class dataEntry:
    def __init__(self):
        self.stFile = open("st_data.txt","w")
        clean_startTime=  time.strftime("%H:%M",time.localtime(startTime))
        self.stFile.write(str(clean_startTime))
        self.stFile.close()

        self.mstFile = open("mst_data.txt","w")
        self.mstFile.write(str(maxStillTime))
        self.mstFile.close()
        
        
    def update(self):
        self.lmtFile = open("lmt_data.txt","w")
        clean_lastMoveTime=  time.strftime("%H:%M",time.localtime(lastMoveTime))
        self.lmtFile.write(str(clean_lastMoveTime))
        self.lmtFile.close()
                
        self.teFile = open("te_data.txt","w")
        clean_tEnd = time.strftime("%H:%M",time.localtime(tEnd))
        self.teFile.write(str(clean_tEnd))
        self.teFile.close()
        
        self.mcFile = open("mc_data.txt","w") 
        self.mcFile.write(str(moveCount))
        self.mcFile.close()

        stillTime = (time.time() - startTime)/60
        self.stillFile = open("still_data.txt","w") 
        self.stillFile.write(str(stillTime))
        self.stillFile.close()

if __name__ == '__main__':
    mstMinutes = input("Set maximum stillness time (in minutes): ")
    maxStillTime = int(mstMinutes) * 60
    wlbt = Walabot()
    wlbt.connect()
    wlbt.configure()
    wlbt.start()
    wlbt.calibrate()
    data = dataEntry()
    
    print("Starting WallyFlow. Be Mindful!")

    try:
        while True:
            clean_tEnd = time.strftime("%H:%M",time.localtime(tEnd))
            clean_lastMoveTime=  time.strftime("%H:%M",time.localtime(lastMoveTime))
            wlbt.WallyFlow()
            if time.time() > tEnd:
                GPIO.output(4,1)
                data.update()
                time.sleep(1)
                GPIO.output(4,0)
                pass
    except KeyboardInterrupt:
        GPIO.output(4,0)
        wlbt.stopAndDisconnect()
