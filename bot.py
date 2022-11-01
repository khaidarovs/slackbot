from dotenv import load_dotenv
import json
import os
from slack import WebClient
from flask import Flask
from slackeventsapi import SlackEventAdapter

# Load the tokens from the ".env" file, which are set up as environment variables. 
# You'll need the signing secret and bot token from the Slack developer console 
# for a workspace, which you put in a file you make called ".env". It prevents a 
# security risk related to revealing secret keys in public. 
load_dotenv()

bot_app = Flask(__name__)

# You can find the signing secret token in the "Basic Information" -> "App Credentials" sections 
# of the Slack workspace developer console. By "/slack/events" is the endpoint that you would
# attach to the end of the ngrok link when inputting the request URL in the "Event Subscriptions"
# -> "Enable Events" section of the Slack workspace developer console.  
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], "/slack/events", bot_app)

# You can find the bot token in the "OAuth & Permissions" section of the Slack workspace developer 
# console.
web_client = WebClient(token=os.environ['BOT_TOKEN'])

# Functions we'd implement would be here.

def enable_activity_warnings(self):
# TODO : actually write the function. This is just for creating unit tests
    cmd_output ={
    "blocks": [
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*Enabled activity warnings.*"
        }
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "Activity warning threshold is set to 5 (default)."
                }
            }
        ]
    }
    return cmd_output

def disable_activity_warnings(self):
# TODO : actually write the function. This is just for creating unit tests
    payload = self.payload

    if payload["text"] == "":
        # Payload is empty, disable indefinitely
        downtime_response = "Activity warnings disabled indefinitely."
    else:
        # We were given a downtime for activity warnings, set accordingly
        downtime_response = "Activity warnings disabled for " + payload.text + "."

    cmd_output ={
    "blocks": [
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*Disabled activity warnings.*"
        }
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": downtime_response
                }
            }
        ]
    }
    return cmd_output

# Allows us to set up a webpage with the script, which enables testing using tools like ngrok.
if __name__ == "__main__":
    bot_app.run(debug=True)
    