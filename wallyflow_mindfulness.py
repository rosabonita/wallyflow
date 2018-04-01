#!/ust/bin/python

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
maxStillTime = 60 * 1

#Initialize Last Average Position to 0
lastPos = 0

#Minimum Average Change needed to update LAP
minDelta = 10

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

#Set GPIO Mode to Broadcom SOC Channel (A numberins scheme)
GPIO.setmode(GPIO.BCM)

#Set GPIO Pin 4 to output 
GPIO.setup(4, GPIO.OUT)

#Set GPIO Pin 4 Starting at 0 or 'Off'
GPIO.output(4,0)

#Suppress GPIO Warnings
GPIO.setwarnings(False)



class Walabot:
    def __init__(self):
        #Instead of importing Walabot API, load the API directly
        self.wlbt = load_source('WalabotAPI',
                                '/usr/share/walabot/python/WalabotAPI.py')
        #Initialize the Walabot
        self.wlbt.Init()

    #Connection Function
    def connect(self):
        print("Connecting...")
        while True:
            try:
                self.wlbt.ConnectAny()
                print("Walabot Connected")
                return
            except self.wlbt.WalabotError as err:
                #If there is an error, wait 1 second and retry
                print("Connecting...")
                time.sleep(1)

    #Configure Walabot    
    def configure(self):
        print("Configuring...")
        time.sleep(1)

        # Set Profile to PROF_SENSOR_NARROW For lower resolution
        # images but faster capture rate
        self.wlbt.SetProfile(self.wlbt.PROF_SENSOR_NARROW)
        
        #Set Arena Values Using Previously Declared Variables
        self.wlbt.SetArenaR(minInCm, maxInCm, resInCm)
        self.wlbt.SetArenaTheta(minInDeg, maxInDeg, resInDeg)
        self.wlbt.SetArenaPhi(minPhiInDeg, maxPhiInDeg, resPhiInDeg)

        # Wally Flow detects changes in movement, so no filter type
        # MTI would only track targets that move
        self.wlbt.SetDynamicImageFilter(self.wlbt.FILTER_TYPE_NONE)
        
        print("Walabot Configured")

    #Start Walabot
    def start(self):
        print("Starting...")
        time.sleep(1)
        
        while True:
            try:
                self.wlbt.Start()
                print("Walabot Started")
                return
            except self.wlbt.WalabotError as err:
                #Retry if error detected
                print("Starting...")
                time.sleep(1)
                
    # Calibration is optional in Wally Flow
    # Use calibration if Walabot is picking up too much background
    def calibrate(self):
        print("Calibrating...")
        self.wlbt.StartCalibration()
        
        #While the Walabot is still calibrating, trigger Walabot
        while self.wlbt.GetStatus()[0] == self.wlbt.STATUS_CALIBRATING:
            self.wlbt.Trigger()
        print("Calibrated")
        
    # Not used in main program, but useful for debugging    
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

    #The 'Get Action' for Wally Flow is 'GetSensorTargets'
    def getTargets(self):
        self.wlbt.Trigger()
        return self.wlbt.GetSensorTargets()

    #Print out the target info, useful for debugging
    def printSensorTarget(self,target):
            print('Target:\nx: {}\ny: {}\nz: {}\namplitude: {}\n'.format(
                target.xPosCm, target.yPosCm, target.zPosCm, target.amplitude))

    #Stop and Disconnect Walabot at the end of each session to avoid errors
    def stopAndDisconnect(self):
        print("Stopping..")
        time.sleep(1)
        self.wlbt.Stop()
        self.wlbt.Disconnect()
        print("Disconnected")

   #Main WallyFlow Function     
    def WallyFlow(self):
        global lastPos, lastMoveTime, tEnd, moveCount
        
        targets = wlbt.getTargets()
        currPos = 0
        count = len(targets)        


        if count != 0:
            #Detect the 'main' target, i.e. the person sitting
            mainTarget = max(targets, key = lambda t: t[3])

            #Calculate the angle to determine the Main Target's current position
            angle = math.degrees(math.atan(mainTarget.yPosCm/mainTarget.zPosCm))
            currPos += abs(angle)
            #Current Delta is the difference between MT's current and last positions
            currDelta = abs(currPos - lastPos)

            #Check if current delta is greated than specified minimum
            if currDelta > minDelta:
                #Update Last Move Time to Current Time
                lastMoveTime = time.time()
                #End Time is the time when the MT should next move by
                tEnd = lastMoveTime + maxStillTime
                moveCount += 1
                lastPos = currPos
                print("Moved. Delta: ", currDelta)
                return currDelta
            else:
                return 0
        else:
            return 0
        
#This class creates the text files which Alexa will access to get information
class dataEntry:
    def __init__(self):
        #Initialize Start Time and Max Still Time. These only need updating once
        self.stFile = open("st_data.txt","w")
        clean_startTime=  time.strftime("%H:%M",time.localtime(startTime))
        self.stFile.write(str(clean_startTime))
        self.stFile.close()

        self.mstFile = open("mst_data.txt","w")
        self.mstFile.write(str(maxStillTime))
        self.mstFile.close()
        
    #Update these variables each time Current Delta > Min Delta
    def update(self):
        #Update Last Move Time
        self.lmtFile = open("lmt_data.txt","w")
        clean_lastMoveTime=  time.strftime("%H:%M",time.localtime(lastMoveTime))
        self.lmtFile.write(str(clean_lastMoveTime))
        self.lmtFile.close()
        
        #Update Time End        
        self.teFile = open("te_data.txt","w")
        clean_tEnd = time.strftime("%H:%M",time.localtime(tEnd))
        self.teFile.write(str(clean_tEnd))
        self.teFile.close()
        
        #Update Move Count
        self.mcFile = open("mc_data.txt","w") 
        self.mcFile.write(str(moveCount))
        self.mcFile.close()
        
        #Update Still Time
        stillTime = (time.time() - startTime)/60
        self.stillFile = open("still_data.txt","w") 
        self.stillFile.write(str(stillTime))
        self.stillFile.close()

#Main Function
if __name__ == '__main__':
    # This program is set to run at system boot up
    
    # Get desired values for MaxStillTime and MinDelta
    mstMinutes = input("Set maximum stillness time (in minutes): ")
    maxStillTime = float(mstMinutes) * 60
    print("Maximum stillness time set to {} minutes".format(mstMinutes))

    minDelta = input("Set minimum delta (integer between 10 and 60): ")
    print("Minimum delta is set to {}".format(minDelta))

    # Walabot Initialization Cycle
    wlbt = Walabot()
    wlbt.connect()
    wlbt.configure()
    wlbt.start()
    wlbt.calibrate()
    data = dataEntry()
    
    print("Starting WallyFlow. Be Mindful!")

    try:
        #Wally Flow runs continuously until cancelled or machine shutdown
        while True:
            wlbt.WallyFlow()
            if time.time() > tEnd:
                #Turn LED Strip On
                GPIO.output(4,1)
                #Update Values in Text Files
                data.update()
                #Wait 1 Second (Maximizes 'blinking light' effect)
                time.sleep(1)
                #Turn LED Strip Off
                GPIO.output(4,0)
                #Exit If 
                pass
    except KeyboardInterrupt:
        #Turn off LEDS on WallyFlow Cancellation
        GPIO.output(4,0)
        #Stop and Disconnect Walabot
        wlbt.stopAndDisconnect()
