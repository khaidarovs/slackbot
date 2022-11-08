import json
import os
import logging as logger
from dotenv import load_dotenv
from slack import WebClient
from flask import Flask
from slackeventsapi import SlackEventAdapter
from slack_sdk.errors import SlackApiError
from pathlib import Path

env_path = Path('.')/'.env'
load_dotenv(dotenv_path = env_path)

bot_app = Flask(__name__)

slack_event_adapter = SlackEventAdapter(os.environ["SIGNING_SECRET"], "/slack/events", bot_app)

web_client = WebClient(token=os.environ["BOT_TOKEN"])

# database to store any conversations information
conversations_store = {}
#list of lists of format [[id, channel_name], [id, channel_name]]
def fetch_conversations():
    channels = []
    try:
        # Call the conversations.list method using the WebClient
        result = web_client.conversations_list(types="public_channel, private_channel", 
                                               limit=9999)
        channels = save_conversations(result["channels"])
    except SlackApiError as e:
        logger.error("Error fetching conversations: {}".format(e))
    else:
        return channels

# Put conversations into the JavaScript object
def save_conversations(conversations):
    channels = []
    conversation_id = ""
    for conversation in conversations:
        # Key conversation info on its unique ID
        conversation_id = conversation["id"]
        channels.append([conversation["id"], conversation["name"]])
        # Store the entire conversation object
        # (you may not need all of the info)
        conversations_store[conversation_id] = conversation
    return channels

#member joined channel event listener
@slack_event_adapter.on('member_joined_channel')
def welcome_new_user(payload):
    '''
        Instructs the user on how to use StudyGroup when they first join 
        the workspace.

        Input: payload (type?): Payload from the member_joined_channel event
        
        Output: (type?) The output of send_im_message, or False if the channel joined was not the general channel
    '''
    event = payload.get('event', {})
    channel_name = get_channel_name(event.get('channel'))
    welcome_text = "Welcome to StudyRoom! To join a class, message me with the command `/join_class SUBJ-#####` (for example, `/join_class CMSC-22001), and I'll add you the study group."
    if(channel_name == 'general'):
        return send_im_message(event.get('user'), welcome_text)
    return False

def normalize_channel_name(channel_name):
    '''
        Converts the name of a class channel (in the format XXXX-#####) to the 
        proper slack format (includes only lowercase letters, numbers, 
        and a hyphen).

        Input: channel_name (str): the name of the channel to be normalized

        Output: (str) the normalized version of the channel_name.
    '''
    subject = channel_name[0:4]
    return subject.lower() + channel_name[4:]

#returns channel name with a search by id
def get_channel_name(id):
    #TODO next iteration
    pass

#returns channel name with a search by id
def get_channel_id(name_normalized):
    channels = fetch_conversations()
    for id, name in channels:
        if name == name_normalized:
            return id
    pass

def send_im_message(userid, text):
    '''
        Sends a direct message to the user with the given user id.

        Input:
            userid (str): The user to receive the message
            text(str): The message to send to the user

        Output (type?): Success response containing channel and message text, or 
                        SlackApiError on failure
    '''

    channel_id = ""
    try:
        channel_id = web_client.conversations_open(users=userid)
    except SlackApiError as e:
        logger.error("Error fetching conversations: {}".format(e))
        return e
    else:
        rv = web_client.chat_postMessage(channel=channel_id, text=text)
        return rv

def check_channel(channel):
    '''
        Check if a given class currently exists in the workspace.
        
        Input: channel (str) The name of the class to check for
        Output: (bool) Whether or not the channel exists
    '''
    channels = fetch_conversations()
    normalized_channel = normalize_channel_name(channel)

    #access second element in channels (which is list of [id, channel_names]s)
    channel_names = [el[1] for el in channels]
    return normalized_channel in channel_names

def handle_onboarding(class_name, user_id):
    '''
        Adds a user to the channel for the given class, creating the channel if
        it doesn't exist.

        Input: 
            class_name (str): class to add user to
            user_id (str): id of user to add to class

        Output: A dictionary of the channel information on success, or 
                error information on failure (SlackApiError)
    '''
    is_channel = check_channel(class_name)
    name_normalized = normalize_channel_name(class_name)
    if not is_channel:
        try:
            new_channel = web_client.conversations_create(name=name_normalized, 
                                                          is_private=True)
        except SlackApiError as e:
            logger.error("Error creating channel: {}".format(name_normalized, e))
            return e
        else:
            channel_id = new_channel.get('channel').get('id')
    else:
        #made this into a helper function bc i needed to use it in tester too
        channel_id = get_channel_id(name_normalized)
        # channels = fetch_conversations()
        # for id, name in channels:
        #     if name == name_normalized:
        #         channel_id = id
        #         break

    if not channel_id:
        logger.error("Error finding channel_id: id not found")
        return "id for channel " + name_normalized + " not found"

    rv = web_client.conversations_invite(channel=channel_id, users=user_id)
    return rv

# web_client.chat_postMessage(channel='#general', text='Hello World!')
# Allows us to set up a webpage with the script, which enables testing using tools like ngrok.
if __name__ == "__main__":
    bot_app.run(debug=True, port=3000)


