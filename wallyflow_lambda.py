db = MySQLdb.connect(user="wallyflow",
                     passwd="wallyflow",
                     port=3306,
                     host="wallyflow.czadegulsxh8.us-east-1.rds.amazonaws.com",
                     db="wallyflowdb")
cursor = db.cursor()


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet -" + output
        },
        'reprompt':{
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

########################################################
def get_welcome_response():
    session_attributes={}
    card_title = "Welcome"
    speech_output = "Welcome to Wally Flow, mindfulness with Walabot and Alexa."\
                    "How can I help you?"
    reprompt_text = "I'm sorry. I didn't catch that." \
                    "How can I help you?"
                    
    should_end_session = False
    return build_response(session_attributes,
                          build_speechlet_response(card_title,speech_output,
                                                   reprompt_text,should_end_session))
def get_mst_response():
    session_attributes={}
    card_title = "Maximum Still Time"
    sql = "SELECT MaxStillTime FROM wallyflowdb.mstTable ORDER BY initTime DESC LIMIT 1"
    cursor.execute(sql)   
    mst = cursor.fetchone()
    speech_output = "Your maximum still time is set to {}.".format(mst[0])
    reprompt_text = None
    should_end_session = False
    return build_response(session_attributes,
                          build_speechlet_response(card_title,speech_output,
                                                   reprompt_text,should_end_session))
def get_mc_response():
    session_attributes={}
    card_title="Move Count"
    sql = "SELECT MoveCount FROM wallyflowdb.mcTable ORDER BY initTime DESC LIMIT 1"
    cursor.execute(sql)
    mc = cursor.fetchone()
    speech_output = "Your current movement count is {}.".format(mc[0])
    reprompt_text = None
    should_end_session = False
    return build_response(session_attributes,
                          build_speechlet_response(card_title,speech_output,
                                                   reprompt_text,should_end_session))
def get_stillTime_response():
    session_attributes={}
    card_title="Stillness Time"
    sql = "SELECT StillTime FROM wallyflowdb.stillTable ORDER BY initTime DESC LIMIT 1"
    cursor.execute(sql)
    stillTime = cursor.fetchone()
    speech_output = "Your current movement count is {}.".format(stillTime[0])
    reprompt_text=None
    should_end_session=False
    return build_response(session_attributes,
                          build_speechlet_response(card_title,speech_output,
                                                   reprompt_text,should_end_session))
def get_lmt_response():
    session_attributes={}
    card_title="Last Move Time"
    sql = "SELECT LastMoveTime FROM wallyflowdb.lmtTable ORDER BY initTime DESC LIMIT 1"
    cursor.execute(sql)
    lmt = cursor.fetchone()
    speech_output = "Your last move time was {}".format(lmt[0])
    reprompt_text=None
    should_end_session=False
    return build_response(session_attributes,
                          build_speechlet_response(card_title,speech_output,
                                                   reprompt_text,should_end_session))
def get_startTime_response():
    session_attributes = {}
    card_title="Start Time"
    sql = "SELECT StartTime FROM wallyflowdb.stTable ORDER BY initTime DESC LIMIT 1"
    cursor.execute(sql)
    startTime = cursor.fetchone()
    speech_output = "You started this mindfulness session at {}".format(startTime[0])
    reprompt_text=None
    should_end_session=False
    return build_response(session_attributes,
                          build_speechlet_response(card_title,speech_output,
                                                   reprompt_text,should_end_session))    
def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using Wally Flow, mindfulness with Walabot and Alexa."\
                    "Have a mindful day!"
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

###########################################################################
#Events

def on_session_started(session_started_request, session):
    #Called when session starts
    print("on_session_started requestId=" + session_started_request['requestId']
          +", sessionId=" +session['sessionId'])

def on_launch(launch_request, session):
    #Called when the user launches the skill without specifiying what they want
    print("on_launch requestId=" + launch_request['requestId'] +
          " , sessionId =" + session['sessionId'])
    #Dispatch to your skill's launch
    return get_welcome_response()

def on_intent(intent_request, session):
    #Called when the user specifies an intent for this skill
    print("on_intent requestId =" + intent_request['requestId'] +
          ", sessiodId=" + session['sessionId'])
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    if intent_name == "MaxStillTimeIntent":
        return get_mst_response()
    elif intent_name == "MoveCountIntent":
        return get_mc_response()
    elif intent_name == "StillTimeIntent":
        return get_stillTime_response()
    elif intent_name == "LastMoveTimeIntent":
        return get_lmt_response()
    elif intent_name == "StartTimeIntent":
        return get_startTime_response()
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CANCELIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")
    

def on_session_ended(session_ended_request, session):
    #Called when the user ends the session
    #Not called when the skil returns should_ends_session=True
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    #add cleanup logic here

###############################################################
#Main Handler
def lambda_handler(event, context):
    """
    Route the incoming request based on type (LaunchRequest, IntentRequest, etc.)
    The JSON body of the request is provided in the event parameter
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])
    
    if (event['session']['application']['applicationId'] !=
        "amzn1.ask.skill.1a61b436-2b39-448c-a2bb-1ad391fe666b"):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},event['session'])
        
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'],event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
