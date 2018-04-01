#!/ust/bin/python

# WallyFlow Ask-Flask App
# Python 3.5.3
# Raspberry Pi 3

import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

#Flask and Flask Ask Initialization
#######################################
app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

#Intialize Time Variables
#######################################
startTime = 0
maxStillTime = 0
stillTime = 0
lastMoveTime = 0
moveCount = 0


#Function to read in updated variables from local text files
#These variables are fed to Alexa when intent is activated
def readData():
    global startTime, maxStillTime, stillTime, lastMoveTime, moveCount

    with open("st_data.txt","r") as stFile:
        startTime = stFile.readline()
    stFile.close()
    
    with open("mst_data.txt", "r") as mstFile:
        maxStillTime = (mstFile.readline())
    mstFile.close()

    with open("lmt_data.txt","r") as lmtFile:
        lastMoveTime = lmtFile.readline()
    lmtFile.close()

    with open("mc_data.txt","r") as mcFile:
        moveCount = mcFile.readline()
    mcFile.close()

    with open("still_data.txt", "r") as stillFile:
        stillTime = stillFile.readline()
    stillFile.close()

#This is run when the skill is invoked by Alexa
@ask.launch
def startSkill():
    readData()
    mstMinutes = round(float(maxStillTime)/60,3)  
    welcomeMsg = "Welcome to Wally Flow."
    return question(welcomeMsg)

#The intents depend on the user's invocations
@ask.intent("YesIntent")
def yesIntent():
    global maxStillTime
    readData()
    yesMsg = "Starting Wally Flow. Maximum still time is set to {} minutes. Be Mindful!".format(maxStillTime)
    return question(yesMsg)
    

@ask.intent("NoIntent")
def noIntent():
    noMsg = "Stopping Wally Flow"
    return statement(noMsg)

@ask.intent("CancelIntent")
def cancelIntent():
    cancelMsg = "Stopping Wally Flow"
    return statement(cancelMsg)

@ask.intent("MaxStillTimeIntent")
def maxStillTimeIntent():
    global maxStillTime
    readData()
    maxStillTimeMsg = "Your maximum still time is set to {} minutes.".format(maxStillTime)
    return question(maxStillTimeMsg)
    
@ask.intent("MoveCountIntent")
def moveCountIntent():
    global moveCount, startTime
    readData()
    moveCountMsg = "You have moved {} times since {}.".format(moveCount, startTime)
    return question(moveCountMsg)
    
@ask.intent("StillTimeIntent")
def stillnesIntent():
    global stillTime
    readData()
    stMinutes = round(float(stillTime)/60,3)
    stillTimeMsg = "You have been still for {} minutes".format(stMinutes)
    return question(stillTimeMsg)

@ask.intent("LastMoveTimeIntent")
def lmtIntent():
    global lastMoveTime
    readData()
    lmtMsg = "You last moved {}.".format(lastMoveTime)
    return question(lmtMsg)

@ask.intent("StartTimeIntent")
def startTimeIntent():
    global startTime
    readData()
    startTimeMsg = "You started this session at {}.".format(startTime)
    return question(startTimeMsg)

#Ask-Flask Application Runs on Local Server Port 5000
#Don't Forget to intialize either localtunnel or ngrok
#Otherwise, Alexa can't communicate with the app
if __name__ == '__main__':
    app.run(debug = True)   
