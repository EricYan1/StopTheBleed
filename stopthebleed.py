"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import twilio.twiml
from twilio.rest import TwilioRestClient


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" + event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    
    if (event['session']['application']['applicationId'] != "amzn1.ask.skill.b359eb23-9a41-4963-a6d8-813f188c8943"):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


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


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "GetHelp":
        return get_help(intent, session)
    elif intent_name == "GetLocation":
        return get_location(intent, session)
    elif intent_name == "WalkthroughHelp":
        return walkthrough(intent, session)

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

#********************************************************************************
# --------------- Functions that control the skill's behavior ------------------
#********************************************************************************

# What the Alexa will say when you open stopthebleed
def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {"stepPosition":-1, "emergencyDescription":"", "flag":1, "prevQuestion":""}
    card_title = "Welcome"
    speech_output = "Please tell me your emergency." \
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me something I can help you with " \
                    
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# What Alexa will say  when you are done using stopthebleed
def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying Movie popularity" \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# This is an example of a method to be called for an intent
def get_help(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """
    
    card_title = intent['name']
    session_attributes = session.get('attributes', {})
    should_end_session = False
    if session_attributes['flag'] == 2: #it's gone through once already
        # account_sid = "AC25112aeeae78fe8aa6f8bf887da63667"
        # auth_token = "4eb512fdd7bfb7b547c09a33e75e92b1"
        # client = TwilioRestClient(account_sid, auth_token)
        # message = client.messages.create(to="4252994583", from_="+12068662338", body="%s at %s" % (session_attributes["emergencyDescription"], intent['slots']['ResponseGetHelpRequest']['value']))
        speech_output = "I have alerted emergency responses with your location %s. Are you safe?" % intent['slots']['ResponseGetHelpRequest']['value']
        reprompt_text = "Please tell me if you are safe."
        session_attributes["prevQuestion"] = speech_output
    elif session_attributes['flag'] == 1:
        session_attributes['emergencyDescription'] = intent['slots']['ResponseGetHelpRequest']['value']
        speech_output = "I heard %s. Please tell me your location" % (session_attributes['emergencyDescription'])
        reprompt_text = "Please tell me your location."
    else:
        # response = ""
        # while response == "":
        #     response = get_response(session_attributes, intent['slots']['ResponseGetHelpRequest']['value'])
        # speech_output = response[0]
        # reprompt_text = response[0]
        speech_output = "I'm sorry, I didn't catch that. %s" % session_attributes["prevQuestion"]
        reprompt_text = "I'm sorry, I didn't catch that. %s" % session_attributes["prevQuestion"]

    session_attributes['flag'] += 1
    # if 'ResponseHelpRequest' in intent['GetHelp']:
    #     phrase = intent['ResponseGetHelpRequest']
    #     twi
    #     speech_output = "The most popular movie of " + year + " is " + title \
                        
    #     reprompt_text = "Try searching for the most popular movie of a year."
    # else:
    #     speech_output = "I'm not sure what year that is. " \h
    #                     "Please try again."
    #     reprompt_text = "Try searching for the most popular movie of a year."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def walkthrough(intent, session):
    card_title = intent['name']
    session_attributes = session.get('attributes', {})
    
    response = ""

    while response == "":
        response = get_response(session_attributes, intent['slots']['Response']['value'])

    speech_output = response[0]
    reprompt_text = response[0]
    session_attributes["prevQuestion"] = speech_output
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, response[1]))


def get_response(session_attributes, answer):
    response = ""
    position = session_attributes['stepPosition']
    should_end_session = False
    if position == -1:
        if answer == "yes":
            position = 0
            response = "Look for life threatening injuries. Do you need me to explain what to look for?"
        elif answer == "no":
            response = "Please remove yourself from danger and find a safe location. An emergency response will be on scene soon. Goodbye"
            should_end_session = True
    elif position == 0:
        if answer == "yes":
            position = 2
            response = "Find where the blood won't stop flowing or where it's spurting. Tell me to go on, or ask me to repeat?"
        elif answer == "no":
            position = 1
            response = "Do you have first aid or trauma kit?"
    # This is where we start branching 
    elif position == 1:
        if answer == "yes":
            response = "Open the clothing over the bleeding wound." \
            "Wipe away any pooled blood. Tell me to go on, or ask me to repeat??"
            position = 4
        elif answer == "no":
            position = 3
            response = "You dont have first aid ok. find a clean cloth. Do you need help with that?"
    # not the first aid kit branch. identify usable cloths
    elif position == 3:
        if answer == "yes":
            position = 8
            response = "You can use a shirt, towel, paper towels, or pads. Would you like me to go on, or ask me to repeat?"
        elif answer == "no":
            position = 4
            response = "Open the clothing over the bleeding wound. Tell me to go on, or ask me to repeat??"  

        
    #vhave first aid kit 
    elif position == 4:
        if answer == "go on":
            response = "Pack the wound with bleeding with the gauze or clean cloth. Tell me to go on, or ask me to repeat??" 
            position = 10
        elif answer == "repeat" or answer == "please repeat" or answer == "repeat yourself":
            response = "Open the clothing over the bleeding wound." \
            "Wipe away any pooled blood. Tell me to go on, or ask me to repeat??" 

    # more examples
    elif position == 2:
        if answer == "go on":
            position = 1
            response = "Do you have first aid or trauma kit?"
        elif answer == "repeat" or answer == "please repeat" or answer == "repeat yourself":
            response = "Find where the blood won't stop flowing or where it's spurting. Tell me to go on, or ask me to repeat??"
      
    elif position == 10:
        if answer == "go on":
            response = "Apply steady pressure with both hands directly on top of the bleeding wound." \
            "Push down as hard as you can. Tell me to go on, or ask me to repeat?" 
            position = 22
        elif answer == "repeat" or answer == "please repeat" or answer == "repeat yourself":
            response = "Pack the wound with bleeding with the gauze or clean cloth. Tell me to go on, or ask me to repeat??" 

    elif position == 22:
        if answer == "go on":
            response = "Hold pressure to stop bleeding. Continue pressure until relieved by medical responders. Goodbye."
            should_end_session = True
        elif answer == "repeat" or answer == "please repeat" or answer == "repeat yourself":
            response = "Push down as hard as you can. Tell me to go on, or ask me to repeat?" 


    elif position == 8:
        if answer == "go on":
            position = 4
            response = "Open the clothing over the bleeding wound. Tell me to go on, or ask me to repeat??"  
        elif answer == "repeat" or answer == "please repeat" or answer == "repeat yourself":
            response = "You can use a shirt, towel, paper towels, or pads. Would you like me to go on, or ask me to repeat?"

    session_attributes['stepPosition'] = position
    return [response, should_end_session]

# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
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