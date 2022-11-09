from dotenv import load_dotenv
import os
from slack import WebClient
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
import firebase_admin
from firebase_admin import credentials, db

from nltk import download
from nltk.sentiment import SentimentIntensityAnalyzer

load_dotenv()

ref = db.reference('mood_messages_vars/')

# Load the tokens from the ".env" file, which are set up as environment variables. 
# You'll need the signing secret and bot token from the Slack developer console 
# for a workspace, which you put in a file you make called ".env". It prevents a 
# security risk related to revealing secret keys in public. 

bot_app = Flask(__name__)

# You can find the signing secret token in the "Basic Information" -> "App Credentials" sections 
# of the Slack workspace developer console. By "/slack/events" is the endpoint that you would
# attach to the end of the ngrok link when inputting the request URL in the "Event Subscriptions"
# -> "Enable Events" section of the Slack workspace developer console.  
SIGNING_SECRET = os.environ['SIGNING_SECRET']
BOT_TOKEN = os.environ['BOT_TOKEN']
slack_event_adapter = SlackEventAdapter(SIGNING_SECRET, "/slack/events", bot_app)

# You can find the bot token in the "OAuth & Permissions" section of the Slack workspace developer 
# console.

web_client = WebClient(token=BOT_TOKEN)

# You can find the signing secret token in the "Basic Information" -> "App Credentials" sections 
# of the Slack workspace developer console. By "/slack/events" is the endpoint that you would
# attach to the end of the ngrok link when inputting the request URL in the "Event Subscriptions"
# -> "Enable Events" section of the Slack workspace developer console.  

# slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], "/slack/events", bot_app)

# You can find the bot token in the "OAuth & Permissions" section of the Slack workspace developer 
# console.

# web_client = WebClient(token=os.environ['BOT_TOKEN'])

# Variables for the bot

# Mood Messages Variables
mood_messages_enabled = ref.child('mood_messages_enabled')
mood_messages_downtime = ref.child('mood_messages_downtime') # empty str if indefinite
mood_message_content = ref.child('mood_message_content')

# Functions we'd implement would be here.

def enable_mood_messages(self):
    # Get data
    payload = self.payload

    # First check if this is a test or not
    is_test = False
    if payload.get('token') == "test_token_1":
        is_test = True
    # Extract data from payload
    user_id = payload.get('user_id')
    channel_id = payload.get('channel_id')

    # Parse message to send
    fallback_msg = "Enabled mood messages. "
    cmd_output ={"blocks": [{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*Enabled mood messages.*"
    }}]}

    # Send msg to user
    msg_construct = {
        "token":BOT_TOKEN,
        "channel":channel_id,
        "text":fallback_msg,
        "user":user_id,
        "blocks":cmd_output
    }
    if not is_test: # From Slack, not from Tests
        retval = web_client.chat_postEphemeral(**msg_construct) # https://api.slack.com/methods/chat.postEphemeral
    ref.update({
        'mood_messages_enabled':True
    })
    return cmd_output

def disable_mood_messages(self):
    # Get data
    payload = self.payload

    # First check if this is a test or not
    is_test = False
    if payload.get('token') == "test_token_1":
        is_test = True
    # Extract data 
    user_id = payload.get('user_id')
    channel_id = payload.get('channel_id')

    # Parse message to send
    user_given_text = payload["text"]
    if user_given_text == "":
        # Payload is empty, disable indefinitely
        downtime_response = "Mood messages disabled indefinitely."
        ref.update({
        'mood_messages_downtime':""
        })
    else:
        # We were given a downtime for mood messages, set accordingly
        finalchar = user_given_text[-1]
        if finalchar != -1:
            downtime_response = "Mood messages disabled for " + payload["text"] + "."
        ref.update({
        'mood_messages_downtime':payload["text"]
        })
    ref.update({
    'mood_messages_enabled':False
    })
    fallback_msg = "Disabled mood messages. " + downtime_response
    cmd_output ={"blocks": [{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*Disabled mood messages.*"}},{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": downtime_response
        }}]}
    # Send msg to user
    msg_construct = {
        "token":BOT_TOKEN,
        "channel":channel_id,
        "text":fallback_msg,
        "user":user_id,
        "blocks":cmd_output
    }
    if not is_test: # From Slack, not from Tests
        retval = web_client.chat_postEphemeral(**msg_construct) # https://api.slack.com/methods/chat.postEphemeral
    return cmd_output

def set_mood_messages_content(self):
    # Get data
    payload = self.payload

    # First check if this is a test or not
    is_test = False
    if payload.get('token') == "test_token_1":
        is_test = True
    # Extract data from payload
    user_id = payload.get('user_id')
    channel_id = payload.get('channel_id')

    # Parse message to send
    if payload["text"] == "":
        # Set to default
        ref.update({
        'mood_message_content':"Let's be more positive!"
        })
    else:
        # Set to that indicated by user
        ref.update({
        'mood_message_content':payload["text"]
        })
    fallback_msg = "Set mood messages content to:\n" + mood_message_content.get()
    cmd_output ={"blocks": [{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*Set mood messages content to:*"
        }},{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": mood_message_content.get()
                }}]}
    # Send msg to user
    msg_construct = {
        "token":BOT_TOKEN,
        "channel":channel_id,
        "text":fallback_msg,
        "user":user_id,
        "blocks":cmd_output
    }
    if not is_test: # From Slack, not from Tests
        retval = web_client.chat_postEphemeral(**msg_construct) # https://api.slack.com/methods/chat.postEphemeral
    return cmd_output

#This function only sends a message if the check_mood function returns -1, i.e, if the mood is negative
def send_mood_message(self):
    # Get data
    payload = self.payload

    # First check if this is a test or not
    is_test = False
    if payload.get('token') == "test_token_1":
        is_test = True
    # Extract data from payload
    user_id = payload.get('user_id')
    channel_id = payload.get('channel_id')

    cmd_output ={"blocks": [{
    "type": "section",
    "text": {
        "type": "mrkdwn",
        "text": "*Mood Message*"
    }},{
    "type": "section",
    "text": {
        "type": "mrkdwn",
        "text": mood_message_content.get()
    }}]}
    fallback_msg = mood_message_content.get()
    msg_construct = {
    "token":BOT_TOKEN,
    "channel":channel_id,
    "text":fallback_msg,
    "blocks":cmd_output
    }
    if not is_test: # From Slack, not from Tests
        retval = web_client.chat_postMessage(**msg_construct)

    return cmd_output

#the handle_message_event function calls this function, so this function takes in a dictionary as its input. 
#the dictionary is of the following :
#{
    #"token": "z26uFbvR1xHJEdHE1OQiO6t8",
    #"channel": "C2147483705",
    #"user": "U2147483697",
    #"text": "Hello world",
#}

def check_mood(self, dict_message):
    # The SentimentIntensityAnalyzer model needs us to pull down the vader_lexicon
    download('vader_lexicon')
    sia = SentimentIntensityAnalyzer()

    score = sia.polarity_scores(dict_message["text"])["compound"]

    if score > 0:
        return 1
    elif score < 0:
        return -1
    else:
        return 0
        
# Allows us to set up a webpage with the script, which enables testing using tools like ngrok.
if __name__ == "__main__":
    bot_app.run(debug=True)