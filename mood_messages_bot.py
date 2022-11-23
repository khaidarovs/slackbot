# Import utils
from iter2_activity_mood_convo_utils import *

# firebase_db_init

# Initializes firebase database references for a given channel id. If this is 
# called and the firebase database references already exist, the function
# does nothing
# INPUT
# - channel id
# OUTPUT
# - db references initialized to default values 
# - returns reference to channel in firebase db
def firebase_db_init(channel_id):
    channelref = ref.child(channel_id)
    if channelref.get() != None:
        # already exists in db
        return channelref
    # doesnt exist. So we init the vars
    channelref.set({
        'activity_warning_vars':{
            'activity_warnings_content':"Let's get more active!",
            'activity_warnings_downtime':"",
            'activity_warnings_enabled':False,
            'activity_warnings_threshold':5
        },
        'mood_messages_vars':{
            'mood_message_content':"Let's be more positive!",
            'mood_messages_downtime':"",
            'mood_messages_enabled':False
        }
    })
    return channelref

# Functions we'd implement would be here.

def enable_mood_messages(payload):
    # First check if this is a test or not
    is_test = False
    if payload.get('token') == "test_token_1":
        is_test = True
    # Extract data from payload
    user_id = payload.get('user_id')
    channel_id = payload.get('channel_id')

    # Let's make sure that the Firebase DB has been initialized
    # Also, let's get the channel reference
    channelref = firebase_db_init(channel_id)
    mood_messages_vars_ref = channelref.child('mood_messages_vars')

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
    mood_messages_vars_ref.update({
        'mood_messages_enabled':True
    })
    return cmd_output

def disable_mood_messages(payload):

    # First check if this is a test or not
    is_test = False
    if payload.get('token') == "test_token_1":
        is_test = True
    # Extract data 
    user_id = payload.get('user_id')
    channel_id = payload.get('channel_id')

    # Let's make sure that the Firebase DB has been initialized
    # Also, let's get the channel reference
    channelref = firebase_db_init(channel_id)
    mood_messages_vars_ref = channelref.child('mood_messages_vars')

    # Parse message to send
    user_given_text = payload["text"]
    if user_given_text == "":
        # Payload is empty, disable indefinitely
        downtime_response = "Mood messages disabled indefinitely."
        mood_messages_vars_ref.update({
        'mood_messages_downtime':""
        })
    else:
        # We were given a downtime for mood messages, set accordingly
        finalchar = user_given_text[-1]
        if finalchar != -1:
            downtime_response = "Mood messages disabled for " + payload["text"] + "."
        mood_messages_vars_ref.update({
        'mood_messages_downtime' : payload["text"]
        })
    mood_messages_vars_ref.update({ 'mood_messages_enabled':False
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

def set_mood_messages_content(payload):
    # First check if this is a test or not
    is_test = False
    if payload.get('token') == "test_token_1":
        is_test = True
    # Extract data from payload
    user_id = payload.get('user_id')
    channel_id = payload.get('channel_id')

    # Let's make sure that the Firebase DB has been initialized
    # Also, let's get the channel reference
    channelref = firebase_db_init(channel_id)
    mood_messages_vars_ref = channelref.child('mood_messages_vars')

    # Parse message to send
    if payload["text"] == "":
        # Set to default
        mood_messages_vars_ref.update({
        'mood_message_content':"Let's be more positive!"
        })
    else:
        # Set to that indicated by user
        mood_messages_vars_ref.update({
        'mood_message_content':payload["text"]
        })
    mood_message_content = channelref.child('mood_messages_vars').child('mood_message_content').get()
    fallback_msg = "Set mood messages content to:\n" + mood_message_content
    cmd_output ={"blocks": [{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*Set mood messages content to:*"
        }},{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": mood_message_content
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

#This function sends a message if the mood is negative (-1)
def send_mood_message(payload):
    # First check if this is a test or not
    is_test = False
    if payload.get('token') == "test_token_1":
        is_test = True
    # Extract data from payload
    user_id = payload.get('user_id')
    channel_id = payload.get('channel_id')
    # Let's make sure that the Firebase DB has been initialized
    # Also, let's get the channel reference
    channelref = firebase_db_init(channel_id)
    mood_messages_vars_ref = channelref.child('mood_messages_vars')
    mood_message_content = mood_messages_vars_ref.child('mood_message_content').get()
    cmd_output ={"blocks": [{
    "type": "section",
    "text": {
        "type": "mrkdwn",
        "text": "*Mood Message*"
    }},{
    "type": "section",
    "text": {
        "type": "mrkdwn",
        "text": mood_message_content
    }}]}
    fallback_msg = mood_message_content
    msg_construct = {
    "token":BOT_TOKEN,
    "channel":channel_id,
    "text":fallback_msg,
    "blocks":cmd_output
    }
    if not is_test: # From Slack, not from Tests
        retval = web_client.chat_postMessage(**msg_construct)

    return cmd_output

#Takes in a dictionary representing information from a single message, and determines the
#mood of that message: positive, negative, or neutral, represented by 1, -1, 0 respectively
#The dictionary is of the following type:
#{
    #"token": "z26uFbvR1xHJEdHE1OQiO6t8",
    #"channel": "C2147483705",
    #"user": "U2147483697",
    #"text": "Hello world",
#}
def check_mood(payload, dict_message):
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

#the handle_message_event function calls this function, so this function takes in a dictionary as its input. 
#the dictionary is of the following type:
#{
    #"token": "z26uFbvR1xHJEdHE1OQiO6t8",
    #"channel": "C2147483705",
    #"user": "U2147483697",
    #"text": "Hello world",
#}

def check_send_mood_message(payload, dict_message):
    is_test = False
    if payload.get('token') == "test_token_1":
        is_test = True
    # Extract data from payload
    channel_id = payload.get('channel_id')

    
    # Let's make sure that the Firebase DB has been initialized
    # Also, let's get the channel reference
    channelref = firebase_db_init(channel_id)
    mood_messages_vars_ref = channelref.child('mood_messages_vars')
    mood_messages_enabled_ref = mood_messages_vars_ref.child('mood_messages_enabled')
    # Check conditions for calling our scheduling functions:
    # - activity_warnings_enabled
    # - if disabled
    #      -downtime = "", ignore
    #      -downtime = 0d; then enable, and call func
    #      -otherwise, decrement downtime by 1
    if mood_messages_enabled_ref.get():
        send_msg = True
    else:
        downtime = mood_messages_vars_ref.child('mood_messages_downtime').get()
        if downtime == "":
            # Indef
            send_msg = False
        elif downtime == "0d":
            # timer ended
            # Enable activity msgs
            # Set downtime to ""
            # Send this activity msg, if applicable
            mood_messages_vars_ref.update({
                'mood_messages_enabled':True,
                'mood_messages_downtime':""
            })
            send_msg = True
        else:
            # Timer still going
            # Set downtime to N days - 1
            # Do not send this msg
            dec_time = int(downtime[:-1]) - 1
            dec_time_str = str(dec_time) + "d"
            mood_messages_vars_ref.update({
                'mood_messages_downtime':dec_time_str
            })
            send_msg = False
        #end if/else
    #end if/else
    send_msg = send_msg and (check_mood(payload, dict_message) == 1)
    if (send_msg):
        # We're below the threshold, lets send msg
        send_mood_message(payload)
        print("Sending mood msg!")
    
    return send_msg # True if msg sent, False if not
# Allows us to set up a webpage with the script, which enables testing using tools like ngrok.
if __name__ == "__main__":
    bot_app.run(debug=True)
