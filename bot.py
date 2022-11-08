from dotenv import load_dotenv
import os
from slack import WebClient
from flask import Flask, Response, request
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

# Functions we'd implement would be here.
"""
Checks if the payload is valid (i.e. has all the fields that we need for processing).
"""
def check_valid_payload(payload):
    print("check_valid_payload is being tested\n")
    valid = True
    return valid

"""
Parses the payload and returns a shortened dictionary object with the relevant information.
In case the subtype is irrelevant OR the user ID is the same as the bot ID, 
meaning the event was triggered by a bot replying in the chat, return an empty dictionary.
"""
def parse_payload(payload, bot_id):
    print("parse_payload is being tested\n")
    info = {}
    if (payload.get("user") == bot_id):
        return info
    else:
        info = payload
    return info

def check_id(payload, bot_id):
    print("check_id is being tested\n")
    rv = True
    if (payload.get("channel").get("creator") == bot_id):
        rv = False
    return rv

@slack_event_adapter.on('message')
def handle_message_event(payload):
    #TODO
    #Check if the payload is valid
    #If it is, parse the payload and return a useful information dictionary
    if (check_valid_payload(payload)):
        bot_id = "1"
        info_dict = parse_payload(payload, bot_id)
        #Call the relevant function and pass info_dict as parameter    
    return Response(status=501)

@slack_event_adapter.on('channel_created')
def handle_workspace_channels(payload):
    #check if the person who created the channel is the bot or a person
    #to delete the channel the function should make an API call
    #look at payload["channel"]["creator"]
    #to get the bot id - do an api call
    bot_id = "1" #https://api.slack.com/methods/auth.test/test -> web_client.api_call("auth.test")['user_id']
    if (check_id(payload, bot_id)):
        #do nothing
        pass
    else:
        #delete the channel
        pass

# handle_slash_command is the default function called when a slash command is 
# sent by a user in the workspace. Payload sent by Slack is parsed for 
# determining whether it's defective or not, and if not then the relevant 
# handle function for the command is called. 
@bot_app.route('/slash-command', methods=['POST'])
def handle_slash_command():
    payload = request.form.to_dict()
    if check_valid_payload(payload) == False:
        return Response(status=400)
    resp = Response(status=200)
    # payload['command'] will always be valid slash command due to Slack 
    # platform filtering for that. 
    if payload['command'] == "/meetup":
        resp = handle_meetup_invocation(payload)
    elif payload['command'] == "/enable_activity_warnings":
        pass # function to enable_activity HERE
    elif payload['command'] == "/disable_activity_warnings":
        resp = handle_disable_activity_warnings_invocation(payload)
    elif payload['command'] == "/set_activity_warning_threshold":
        resp = handle_set_activity_warning_threshold_invocation(payload)
    elif payload['command'] == "/set_activity_warning_content":
        pass # call set_activity_warning_content function HERE
    elif payload['command'] == "/enable_mood_messages":
        pass # function to enable_mood_message HERE
    elif payload['command'] == "/disable_mood_messages":
        resp = handle_disable_mood_messages_invocation(payload)
    elif payload['command'] == "/join_class":
        resp = handle_join_class_invocation(payload)
    return resp

# Determines if the parameter to /set_activity_warning_threshold{n_message} 
# is valid.
def handle_set_activity_warning_threshold_invocation(payload):
    params = payload['text']
    invalid_resp = "Sorry! The number of messages can only be a number and greater than 0. Please try again."
    params_split = params.split(" ")
    if len(params) == 0 or len(params_split) > 1 or params_split[0].isnumeric() == False or int(params_split[0]) <= 0:
        return invalid_resp
    # call set_activity_warning_threshold function HERE
    return Response(status=200)

# Removed handle_set_activity_warning_content_invocation(payload) since we 
# determined the string value in /set_activity_warning_content{string value} 
# is not important to handle.

# Determines if the parameter to /join_class{class number} is valid. 
def handle_join_class_invocation(payload):
    params = payload['text'].split(" ")
    invalid_resp = "Sorry! I can't recognize your class input. Be sure that it follows the following format: <four letter department name> <5 number course code>"
    if len(params) != 2 or len(params[0]) != 4 or len(params[1]) != 5:
        return invalid_resp
    dept_param = params[0]
    code_param = params[1]
    for i in range(len(dept_param)):
        if dept_param[i].isnumeric():
            return invalid_resp 
    for i in range(len(code_param)):
        if code_param[i].isnumeric() == False:
            return invalid_resp 
    # call join_class function HERE
    return Response(status=200)

# is_time_format_valid checks if the time string contains nonnegative numbers 
# or not. time_format is measured relative to the time a command was invoked, 
# and is used for commands pertaining to scheduling future 
# events/notifications. Note that this function does not actually compute the 
# time, just determines if it is computable. 
def is_time_format_valid(time_format):
    t_len = len(time_format)
    if t_len == 0:
        return False
    has_number = False
    for i in range(t_len):
        if time_format[i] == '-':
            if i + 1 < t_len and time_format[i + 1].isnumeric():
                return False # Existence of negative number in time format.
        if time_format[i].isnumeric():
            has_number = True
    return has_number

# compute_time_format calculates the number of seconds from now that is 
# specified in the given time format, if it's of a valid format. 
def compute_time_format(time_format):
    if is_time_format_valid(time_format) == False: 
        # Return negative number since it would be invalid when returning the 
        # time from now. Time from now needs to be a nonzero positive number.
        return -1 
    # Concatenate numerical characters into a string, until a non-numerical 
    # character is reached.
    total_time_sec = 0
    last_num_as_string = "0"
    for i in range(len(time_format)):
        if time_format[i].isnumeric():
            last_num_as_string += time_format[i] 
        else:
            time_part = int(last_num_as_string)
            if time_format[i] == 'd':
                total_time_sec += (time_part * 86400)
            elif time_format[i] == 'h':
                total_time_sec += (time_part * 3600)
            elif time_format[i] == 's':
                total_time_sec += time_part
            else: 
                total_time_sec += (time_part * 60) # Assume minutes
            last_num_as_string = "0"
    if last_num_as_string != "0": # Number with no unit
        time_part = int(last_num_as_string)
        total_time_sec += (time_part * 60)
    return total_time_sec

# handle_meetup_invocation determines if the parameters for the requested 
# /meetup{string time, [optional: location]} command are valid.
def handle_meetup_invocation(payload):
    params = payload['text'].split(", ")
    if len(params) == 1: 
        params = payload['text'].split(",")
    invalid_resp = "Sorry! I couldn't understand the parameters you put for the command. Be sure for the time (1st parameter) you include nonnegative numbers."
    if is_time_format_valid(params[0]) == False:
        return invalid_resp 
    location = ""
    if len(params) > 1:
        location = params[1]
    # meetup function call HERE
    return Response(status=200)
    
# Determines if the parameter to /disable_activity_warnings{string downtime} is 
# valid. 
def handle_disable_activity_warnings_invocation(payload):
    invalid_resp = "Sorry! I couldn't recognize your time format. Please include nonnegative numbers in your input and try again."
    time_from_now = compute_time_format(payload['text'])
    if time_from_now <= 0: 
        return invalid_resp
    # call disable_activity_warnings function HERE
    return Response(status=200)

# Determines if the parameter to /disable_mood_messages{string downtime} is 
# valid.
def handle_disable_mood_messages_invocation(payload):
    invalid_resp = "Sorry! I couldn't recognize your time format. Please include nonnegative numbers in your input and try again."
    time_from_now = compute_time_format(payload['text'])
    if time_from_now <= 0: 
        return invalid_resp
    # call disable_mood_messages function HERE
    return Response(status=200)

# Allows us to set up a webpage with the script, which enables testing using tools like ngrok.
if __name__ == "__main__":
    bot_app.run(debug=True)
    