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

"""   
@app.route('/')
def homepage():
    return "Wally Flow: Be Mindful"    
"""
@ask.launch
def startSkill():
    readData()
    mstMinutes = round(float(maxStillTime)/60,3)
    #welcomeMsg = render_template('welcome')
    #welcomeMsg = "Would you like to start Wally Flow?"
    
    welcomeMsg = "Starting Wally Flow. Maximum still time is set to {} minutes. Be Mindful!".format(mstMinutes)
    #repromptMsg = render_template('repromptWelcome')
    #repromptMsg = "I didn't quite get that. Would you like to start Wally Flow?"
    #return question(welcomeMsg) \
    #       .reprompt(repromptMsg)
    return question(welcomeMsg)

@ask.intent("YesIntent")
def yesIntent():
    global maxStillTime
    readData()
    #yesMsg = render_template('yes', minutes = str(maxStillTime))
    yesMsg = "Starting Wally Flow. Maximum still time is set to {} minutes. Be Mindful!".format(maxStillTime)
    return question(yesMsg)
    

@ask.intent("NoIntent")
def noIntent():
    noMsg = "Stopping Wally Flow"
    #noMsg = render_template('no')
    return statement(noMsg)

@ask.intent("CancelIntent")
def cancelIntent():
    #cancelMsg = render_template('cancel')
    cancelMsg = "Stopping Wally Flow"
    return statement(cancelMsg)

@ask.intent("MaxStillTimeIntent")
def maxStillTimeIntent():
    global maxStillTime
    readData()
    #maxStillTimeMsg = render_template('maxStillTime', minutes = maxStillTime)
    maxStillTimeMsg = "Your maximum still time is set to {} minutes.".format(maxStillTime)
    return question(maxStillTimeMsg)
    
@ask.intent("MoveCountIntent")
def moveCountIntent():
    global moveCount, startTime
    readData()
    #moveCountMsg = render_template('moveCount', mc = moveCount, st= startTime)
    moveCountMsg = "You have moved {} times since {}.".format(moveCount, startTime)
    return question(moveCountMsg)
    
@ask.intent("StillTimeIntent")
def stillnesIntent():
    global stillTime
    readData()
    stMinutes = round(float(stillTime)/60,3)
    #stillTimeMsg = render_template('stillTime', minutes = stillTime)
    stillTimeMsg = "You have been still for {} minutes".format(stMinutes)
    return question(stillTimeMsg)

@ask.intent("LastMoveTimeIntent")
def lmtIntent():
    global lastMoveTime
    readData()
    #lmtMsg = render_template('lastMoveTime', time = lastMoveTime)
    lmtMsg = "You last moved {}.".format(lastMoveTime)
    return question(lmtMsg)

@ask.intent("StartTimeIntent")
def startTimeIntent():
    global startTime
    readData()
    #startTimeMsg = render_template('startTime', time = startTime)
    startTimeMsg = "You started this session at {}.".format(startTime)
    return question(startTimeMsg)

if __name__ == '__main__':     
    app.run(debug = True)   
