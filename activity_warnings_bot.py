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

def enable_activity_warnings(payload):
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
    activity_warning_vars_ref = channelref.child('activity_warning_vars')
    activity_warnings_threshold = activity_warning_vars_ref.child('activity_warnings_threshold').get()

    # Parse message to send
    threshold_text = "Activity warning threshold is set to " + str(activity_warnings_threshold)
    if activity_warnings_threshold == 5:
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

    activity_warning_vars_ref.update({
        'activity_warnings_enabled':True
    })
    return cmd_output

def disable_activity_warnings(payload):

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
    activity_warning_vars_ref = channelref.child('activity_warning_vars')

    # Parse message to send
    user_given_text = payload["text"]
    if user_given_text == "":
        # Payload is empty, disable indefinitely
        downtime_response = "Activity warnings disabled indefinitely."
        activity_warning_vars_ref.update({
        'activity_warnings_downtime':""
        })
    else:
        # We were given a downtime for activity warnings, set accordingly
        finalchar = user_given_text[-1]
        if finalchar != -1:
            downtime_response = "Activity warnings disabled for " + payload["text"] + "."
        activity_warning_vars_ref.update({
        'activity_warnings_downtime':payload["text"]
        })
    activity_warning_vars_ref.update({
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

def set_activity_warnings_threshold(payload):
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
    activity_warning_vars_ref = channelref.child('activity_warning_vars')

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
    activity_warning_vars_ref.update({
    'activity_warnings_threshold':int(payload["text"])
    })
    return cmd_output

def set_activity_warnings_content(payload):
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
    activity_warning_vars_ref = channelref.child('activity_warning_vars')

    #Update firebase DB vars
    if payload["text"] == "":
        # Set to default
        activity_warning_vars_ref.update({
        'activity_warnings_content':"Let's get more active!"
        })
    else:
        # Set to that indicated by user
        activity_warning_vars_ref.update({
        'activity_warnings_content':payload["text"]
        })
    activity_warnings_content = channelref.child('activity_warning_vars').child("activity_warnings_content").get()
    # Parse message to send
    fallback_msg = "Set activity warnings content to:\n" + activity_warnings_content
    cmd_output ={"blocks": [{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*Set activity warnings content to:*"
        }},{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": activity_warnings_content
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

def check_activity(payload):
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

def send_activity_warning(payload):
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
    activity_warning_vars_ref = channelref.child('activity_warning_vars')
    activity_warnings_content = activity_warning_vars_ref.child('activity_warnings_content').get()

    cmd_output ={"blocks": [{
    "type": "section",
    "text": {
        "type": "mrkdwn",
        "text": "*Activity Warning Message*"
    }},{
    "type": "section",
    "text": {
        "type": "mrkdwn",
        "text": activity_warnings_content
    }}]}
    fallback_msg = activity_warnings_content
    msg_construct = {
    "token":BOT_TOKEN,
    "channel":channel_id,
    "text":fallback_msg,
    "blocks":cmd_output
    }
    if not is_test: # From Slack, not from Tests
        retval = web_client.chat_postMessage(**msg_construct)
    return cmd_output

def check_send_activity_warning(payload):
    is_test = False
    if payload.get('token') == "test_token_1":
        is_test = True
    # Extract data from payload
    channel_id = payload.get('channel_id')

    # If it's test, then we have dummy messages return from check_activity
    n_msgs = check_activity(payload)
    
    # Let's make sure that the Firebase DB has been initialized
    # Also, let's get the channel reference
    channelref = firebase_db_init(channel_id)
    activity_warning_vars_ref = channelref.child('activity_warning_vars')
    activity_warnings_threshold_ref = activity_warning_vars_ref.child('activity_warnings_threshold')
    activity_warnings_enabled_ref = activity_warning_vars_ref.child('activity_warnings_enabled')
    # Check conditions for calling our scheduling functions:
    # - activity_warnings_enabled
    # - if disabled
    #      -downtime = "", ignore
    #      -downtime = 0d; then enable, and call func
    #      -otherwise, decrement downtime by 1
    if activity_warnings_enabled_ref.get():
        send_msg = True
    else:
        downtime = activity_warning_vars_ref.child('activity_warnings_downtime').get()
        if downtime == "":
            # Indef
            send_msg = False
        elif downtime == "0d":
            print(downtime)
            # timer ended
            # Enable activity msgs
            # Set downtime to ""
            # Send this activity msg, if applicable
            activity_warning_vars_ref.update({
                'activity_warnings_enabled':True,
                'activity_warnings_downtime':""
            })
            send_msg = True
        else:
            # Timer still going
            # Set downtime to N days - 1
            # Do not send this msg
            dec_time = int(downtime[:-1]) - 1
            dec_time_str = str(dec_time) + "d"
            activity_warning_vars_ref.update({
                'activity_warnings_downtime':dec_time_str
            })
            send_msg = False
        #end if/else
    #end if/else
    send_msg = send_msg and (activity_warnings_threshold_ref.get() >= n_msgs)
    if (send_msg):
        # We're below the threshold, lets send msg
        send_activity_warning(payload)
        print("Sending activity msg!")
    return send_msg # True if msg sent, False if not

# Allows us to set up a webpage with the script, which enables testing using tools like ngrok.
if __name__ == "__main__":
    bot_app.run(debug=True)

    