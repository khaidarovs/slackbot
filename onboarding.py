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
channels = []
def fetch_conversations():
    try:
        # Call the conversations.list method using the WebClient
        result = web_client.conversations_list()
        save_conversations(result["channels"])
    except SlackApiError as e:
        logger.error("Error fetching conversations: {}".format(e))

# Put conversations into the JavaScript object
def save_conversations(conversations):
    conversation_id = ""
    for conversation in conversations:
        # Key conversation info on its unique ID
        conversation_id = conversation["id"]
        channels.append([conversation["id"], conversation["name"]])
        # Store the entire conversation object
        # (you may not need all of the info)
        conversations_store[conversation_id] = conversation

fetch_conversations()


#member joined channel event listener
@slack_event_adapter.on('member_joined_channel')
def welcome_new_user(payload):
    event = payload.get('event', {})
    channel_name = get_channel_name(event.get('channel'))
    welcome_text = "Welcome to StudyRoom! To join a class, message me with the command `/join_class SUBJ-#####` (for example, `/join_class CMSC-22001), and I'll add you the study group."
    if(channel_name == 'general'):
        return send_im_message(event.get('user'), welcome_text)
    return True

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

#returns private message channel id of the App
def get_im_id(user):
    #TODO next iteration
    pass
#sends a message to the private channel between user and app
def send_im_message(userid, text):
    #TODO next iteration
    pass

def check_channel(channel):
    '''
        Check if a given class currently exists in the workspace.
        
        Input: channel (str) The name of the class to check for
        Output: (bool) Whether or not the channel exists
    '''
    channels = fetch_conversations()

    #access second element in channels (which is list of [id, channel_names]s)
    channel_names = [el[1] for el in channels]
    return channel in channel_names

def handle_onboarding(class_name, user_id):
    '''
        Adds a user to the channel for the given class, creating the channel if
        it doesn't exist.

        Input: 
            class_name (str): class to add user to
            user_id (str): id of user to add to class

        Output (dict): A dictionary of the channel information on success, or a
                       dictionary with error information on failure
    '''
    is_channel = check_channel(class_name)
    name_normalized = normalize_channel_name(class_name)
    if not is_channel:
        new_channel = web_client.conversations_create(name_normalized, 
                                                      is_private=True)
        channel_id = new_channel.get('id')
    else:
        channels = fetch_conversations()
        for id, name in channels:
            if name == name_normalized:
                channel_id = id
                break

    rv = web_client.conversations_invite(channel_id, user_id)
    return rv

# web_client.chat_postMessage(channel='#general', text='Hello World!')
# Allows us to set up a webpage with the script, which enables testing using tools like ngrok.
if __name__ == "__main__":
    bot_app.run(debug=True, port=3000)



