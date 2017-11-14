"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import brasileirao

# --------------- Helpers that build all of the responses ----------------------

def get_ordinal(cardinal):
    ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])
    return ordinal(cardinal)
    
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
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


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the 2017 Brazilian Championship Serie A. " \
                    "You can ask for the league standings, team position, team points, " \
                    "G7 group, relegation or Z4 group and leader."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "You can ask for the league standings, team position, team points, " \
                    "G7 group, relegation or Z4 group and leader."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the 2017 Brazilian Championship Serie A... Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def get_team_info(intent, session, league):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    if 'Team' in intent['slots']:
        teams = league.equipes 
        try:
            team = intent['slots']['Team']['value']
        except KeyError, e:
                        team = "UNDEFINED"
                        print ('I got a KeyError - reason "%s"' % str(e))
        points = "0"
        for key in teams:
            #print(str(teams[key])+" - "+team)
            #str(intent)
            if str(teams[key]).lower() == team.lower():
                squad = league.equipes.get(key)
                points = str(squad.pg.total)
                position = str(get_ordinal(int(squad.pos)))
                print (position)
                print (points)
                info="";
                if 'Info' in intent['slots']:
                    try:
                        info = str(intent['slots']['Info']['value'])
                    except KeyError, e:
                        print ('I got a KeyError - reason "%s"' % str(e))
                    if info.lower() == "points":
                        speech_output = team + " has "+ points +" points"
                        reprompt_text = team + " has "+ points +" points"
                    elif info.lower() == "position":   
                        speech_output = team + " is in "+ position +" place"
                        reprompt_text = team + " is in "+ position +" place"
                    else:
                        speech_output = team + " has "+ points +" points and is in "+ position +" place"
                        reprompt_text = team + " has "+ points +" points and is in "+ position +" place"
                else:
                    speech_output = team + " is in "+ position +" place, with "+ points +" points"
                    reprompt_text = team + " is in "+ position +" place, with "+ points +" points"
                break
            else:  
                speech_output = "Sorry, I couldn't understand the team's name"
                reprompt_text = "Sorry, I couldn't understand the team's name"
    else:  
                speech_output = "Sorry, I couldn't understand the request"
                reprompt_text = "Sorry, I couldn't understand the request"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_leader(intent, session, league):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    team = str(league.classificacao[0])
    speech_output = "The leader of the championship is "+ team
    reprompt_text = "The leader of the championship is "+ team
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_gseven(intent, session, league):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    teamstr = ""
    for n in range(0,7):
        teamstr = teamstr + str(league.classificacao[n]) + ", "
    teamstr = teamstr[:-2]
    speech_output = "The seven first teams of the championship are " + teamstr
    reprompt_text = "The seven first teams of the championship are " + teamstr
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def get_zfour(intent, session, league):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    teamstr = ""
    for n in range(16,20):
        teamstr = teamstr + str(league.classificacao[n]) + ", "
    teamstr = teamstr[:-2]
    speech_output = "The last four teams of the championship are " + teamstr
    reprompt_text = "The last four teams of the championship are " + teamstr
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_table(intent, session, league):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    teamstr = ""
    teams = league.equipes 
    points = "0"
    for n in range(0,20):
        position = str(get_ordinal(n+1))
        for key in teams:
            if str(teams[key]).lower() == str(league.classificacao[n]).lower():
                squad = league.equipes.get(key)
                points = str(squad.pg.total)
                teamstr = teamstr + str(league.classificacao[n]) + " is in "+ position + " with "+ points + " points, "
    teamstr = teamstr[:-2]
    speech_output = "The championship standings are " + teamstr
    reprompt_text = "The championship standings are " + teamstr
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

""" Stub Function 
def get_xxx(intent, session, league):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    speech_output = ""
    reprompt_text = ""
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
"""

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()
    

def on_intent(intent_request, session, league):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "TeamIntent":
        return get_team_info(intent, session, league)
    elif intent_name == "LeaderIntent":
        return get_leader(intent, session, league)
    elif intent_name == "GSevenIntent":
        return get_gseven(intent, session, league)
    elif intent_name == "RelegationIntent":
        return get_zfour(intent, session, league)
    elif intent_name == "TableIntent":
        return get_table(intent, session, league)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])
    league = brasileirao.get()
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'], league)
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


