from dotenv import load_dotenv
import os
from slack import WebClient
from flask import Flask, Response
from slackeventsapi import SlackEventAdapter

# Loads the tokens from the ".env" file, which are set up as environment 
# variables. Done to prevent security risks related to revealing the bot 
# token and signing secret in public. 
#load_dotenv()

bot_app = Flask(__name__)

# You can find the signing secret token in the "Basic Information" -> 
# "App Credentials" sections of the Slack workspace developer console.
# By "/slack/events" is the endpoint that you would attach to the end
# of the ngrok link when inputting the request URL in the "Event Subscriptions" 
# -> "Enable Events" section of the Slack workspace developer console.  
# os.environ['SIGNING_SECRET']
slack_event_adapter = SlackEventAdapter("SIGNING_SECRET", "/slack/events", bot_app)

# You can find the bot token in the "OAuth & Permissions" section of the Slack 
# workspace developer console.
# os.environ['BOT_TOKEN']
web_client = WebClient(token="BOT_TOKEN")

# handle_slash_command is the default function called when a slash command is 
# sent by a user in the workspace. Payload sent by Slack is parsed for 
# determining whether it's defective or not, and if not then the relevant 
# handle function for the command is called. 
# TODO: write function.
@bot_app.route('/slash-command', methods=['POST'])
def handle_slash_command():
    return Response(status=501)

# handle_meetup_invocation determines if the parameters for the requested 
# /meetup{string time, [optional: location]} command are valid.
# TODO: write function.
def handle_meetup_invocation(payload):
    return Response(status=501)

# Determines if the parameter to /set_activity_warning_threshold{n_message} 
# is valid.
# TODO: write function.
def handle_set_activity_warning_threshold_invocation(payload):
    return Response(status=501)

# Determines if the parameter to /set_activity_warning_content{string value} 
# is valid. 
# TODO: write function.
def handle_set_activity_warning_content_invocation(payload):
    return Response(status=501)

# Determines if the parameter to /join_class{class number} is valid. 
# TODO: write function.
def handle_join_class_invocation(payload):
    return Response(status=501)

# is_time_format_valid checks if the time string contains nonnegative numbers 
# or not. time_format is measured relative to the time a command was invoked, 
# and is used for commands pertaining to scheduling future 
# events/notifications. Note that this function does not actually compute the 
# time, just determines if it is computable. 
# TODO: write function.
def is_time_format_valid(time_format):
    return False

# /disable_activity_warnings{string downtime} 
# TODO: write function.
def handle_disable_activity_warnings_invocation(payload):
    return Response(status=501)

# /disable_mood_messages{string downtime} 
# TODO: write function.
def handle_disable_mood_messages_invocation(payload):
    return Response(status=501)

# Allows us to set up a webpage with the script, which enables testing using tools like ngrok.
if __name__ == "__main__":
    bot_app.run(debug=True)
    