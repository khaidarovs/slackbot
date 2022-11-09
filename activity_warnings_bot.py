from dotenv import load_dotenv
import json
import os
from slack import WebClient
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
import firebase_admin
from firebase_admin import credentials, db
import time

load_dotenv()

cred = credentials.Certificate(os.environ['SVC_ACCT_KEY'])
firebase_admin.initialize_app(cred, {
    'databaseURL': os.environ['DBURL']
})
ref = db.reference('activity_warning_vars/')

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

# Variables for the bot

# Activity Warning Variables
activity_warnings_enabled = ref.child('activity_warnings_enabled')
activity_warnings_threshold = ref.child('activity_warnings_threshold')
activity_warnings_downtime = ref.child('activity_warnings_downtime')
activity_warnings_content = ref.child('activity_warnings_content')

# Functions we'd implement would be here.

# enable_activity_warnings
#
# Handles the /enable_activity_warnings slash command when run by the user.
# Enables activity warnings in a channel. Tells the user the activity warning 
# threshold and any other necessary information
# INPUT:
# - Payload data
# OUTPUT:
# - Sends an ephemeral message back to the user indicating necessary information
# - Enables activity warnings in the channel

def enable_activity_warnings(self):
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
    threshold_text = "Activity warning threshold is set to "  + activity_warnings_threshold.get()
    if activity_warnings_threshold.get() == 5:
        threshold_text += " (default)."
    else:
        threshold_text += "."
    fallback_msg = "Enabled activity warnings. " + threshold_text
    cmd_output ={"blocks": [{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*Enabled activity warnings.*"
    }},{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": threshold_text
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
        'activity_warnings_enabled':True
    })
    return cmd_output

def disable_activity_warnings(self):
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
        downtime_response = "Activity warnings disabled indefinitely."
        ref.update({
        'activity_warnings_downtime':""
        })
    else:
        # We were given a downtime for activity warnings, set accordingly
        finalchar = user_given_text[-1]
        if finalchar != -1:
            downtime_response = "Activity warnings disabled for " + payload["text"] + "."
        ref.update({
        'activity_warnings_downtime':payload["text"]
        })
    ref.update({
    'activity_warnings_enabled':False
    })
    fallback_msg = "Disabled activity warnings. " + downtime_response
    cmd_output ={"blocks": [{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*Disabled activity warnings.*"}},{
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

def set_activity_warnings_threshold(self):
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
    response_text = "*Set activity warning threshold to " + str(payload["text"]) + ".*"
    fallback_msg = response_text
    cmd_output = {"blocks": [{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": response_text
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
    # Set values
    ref.update({
    'activity_warnings_threshold':str(payload["text"])
    })
    return cmd_output

def set_activity_warnings_content(self):
    # Get dataa
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
        'activity_warnings_content':"Let's get more active!"
        })
    else:
        # Set to that indicated by user
        ref.update({
        'activity_warnings_content':payload["text"]
        })
    fallback_msg = "Set activity warnings content to:\n" + activity_warnings_content.get()
    cmd_output ={"blocks": [{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*Set activity warnings content to:*"
        }},{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": activity_warnings_content.get()
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

def check_activity(self):
    # Get dataa
    payload = self.payload

    # First check if this is a test or not
    is_test = False
    if payload.get('token') == "test_token_1":
        is_test = True
    
    # Extract data from payload
    channel_id = payload.get('channel_id')
    time_1dayago = time.time() - 86400
    history_query = {
    "token":BOT_TOKEN,
    "channel":channel_id,
    "oldest":time_1dayago
    # "limit":activity_warnings_threshold.get()
    }
    if is_test:
        retval = {"messages":[{},{},{},{},{},{},{},{},{},{}]} # 10 msgs
    else:
        retval = web_client.conversations_history(**history_query)
    conversation_history = retval["messages"]
    
    return len(conversation_history)

def send_activity_warning(self):
    # Get dataa
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
        "text": "*Activity Warning Message*"
    }},{
    "type": "section",
    "text": {
        "type": "mrkdwn",
        "text": activity_warnings_content.get()
    }}]}
    fallback_msg = activity_warnings_content.get()
    msg_construct = {
    "token":BOT_TOKEN,
    "channel":channel_id,
    "text":fallback_msg,
    "blocks":cmd_output
    }
    if not is_test: # From Slack, not from Tests
        retval = web_client.chat_postMessage(**msg_construct)
    return cmd_output
        
# Allows us to set up a webpage with the script, which enables testing using tools like ngrok.
if __name__ == "__main__":
    bot_app.run(debug=True)

    