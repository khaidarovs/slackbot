import unittest
from unittest.mock import patch
from bot import *
import requests

# Filename: test_mood_messages.py
# 
# Purpose: Test suite containing unit tests for the functionality of the
# mood messages of the Slack Bot

class Test_Slash_Command_Mood_Messages(unittest.TestCase): 
    # Expected JSON responses for the relevant events you want to handle for your feature can be 
    # found here: https://api.slack.com/events?filter=Events
    def setUp(self):
        self.payload = {}
        
    # This test case tests the functionality of the function
    # enable_mood_messages() 
    def test_enable_mood_messages(self):
        # First let's set input of the slash command
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"CTEST1",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/mood_messages",
            "text":"",
            "response_url":"https://hooks.slack.com/commands/1234/5678",
            "trigger_id":"13345224609.738474920.8088930838d88f008e0",
            "api_app_id":"A123456"
        }
        self.payload = slash_cmd
        # Get channel ref in firebase db
        channelref = ref.child("CTEST1")
        mood_messages_enabled = channelref.child('mood_messages_vars').child('mood_messages_enabled')
        # Now we indicate our expected output
        # Note: this is an ephemeral message. This message will only be visible
        # To the user who called the command
        expected_cmd_output ={
        "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Enabled mood messages.*"
            }
        }
        ]
        }
        #This is where we call the function
        cmd_output = enable_mood_messages(self.payload)
        # Now check our values
        self.assertEqual(cmd_output, expected_cmd_output)
        self.assertTrue(mood_messages_enabled.get()) 
    
    # This test case tests the functionality of the function
    # disable_mood_messages(), where mood messages are disabled
    # indefinitely (no parameter given in the function)
    def test_disable_mood_messages_indefinite(self):
        # First let's set input of the slash command
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"CTEST1",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/disable_mood_messages",
            "text":"",
            "response_url":"https://hooks.slack.com/commands/1234/5678",
            "trigger_id":"13345224609.738474920.8088930838d88f008e0",
            "api_app_id":"A123456"
        }
        self.payload = slash_cmd
        # Get channel ref
        channelref = ref.child("CTEST1")
        mood_messages_enabled = channelref.child('mood_messages_vars').child('mood_messages_enabled')
        mood_messages_downtime = channelref.child('mood_messages_vars').child('mood_messages_downtime')
        # Now we indicate our expected output
        # Note: this is an ephemeral message. This message will only be visible
        # To the user who called the command

        expected_cmd_output ={
        "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Disabled mood messages.*"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Mood messages disabled indefinitely."
                    }
                }
            ]
        }
        # This is where we call the function
        cmd_output = disable_mood_messages(self.payload)
        # Now check our values
        self.assertEqual(cmd_output, expected_cmd_output)
        # uncomment when implementing
        self.assertFalse(mood_messages_enabled.get())
        self.assertEqual("", mood_messages_downtime.get())
    # This test case tests the functionality of the function
    # disable_mood_messages(), where mood messages are disabled
    # for a specified definite downtime
    def test_disable_mood_messages_definite_minutes(self):
        # First let's set input of the slash command
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"CTEST1",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/disable_mood_messages",
            "text":"3d",
            "response_url":"https://hooks.slack.com/commands/1234/5678",
            "trigger_id":"13345224609.738474920.8088930838d88f008e0",
            "api_app_id":"A123456"
        }
        self.payload = slash_cmd
        payload = self.payload
        # Get channel ref
        channelref = ref.child("CTEST1")
        mood_messages_downtime = channelref.child('mood_messages_vars').child('mood_messages_downtime')
        # Now we indicate our expected output
        # Note: this is an ephemeral message. This message will only be visible
        # To the user who called the command
        downtime_response = "Mood messages disabled for " + payload["text"] + "."
        expected_cmd_output ={
        "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Disabled mood messages.*"
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
        # This is where we call the function
        cmd_output = disable_mood_messages(self.payload)
        # Now check our values
        self.assertEqual(cmd_output, expected_cmd_output)
        self.assertEqual("3d", mood_messages_downtime.get())
    
    # This test case is for set_mood_warning_content function where 
    # no text is given (reset to original)
    def test_set_mood_messages_content_none(self):
    # First let's set input of the slash command
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"CTEST1",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/set_mood_messages_content",
            "text":"",
            "response_url":"https://hooks.slack.com/commands/1234/5678",
            "trigger_id":"13345224609.738474920.8088930838d88f008e0",
            "api_app_id":"A123456"
        }
        self.payload = slash_cmd

        # Get channel ref
        channelref = ref.child("CTEST1")
        mood_message_content = channelref.child('mood_messages_vars').child('mood_message_content')

        # Now we indicate our expected output
        # Note: this is an ephemeral message. This message will only be visible
        # To the user who called the command
        expected_cmd_output ={
        "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Set mood messages content to:*"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Let's be more positive!"
                    }
                }
            ]
        }
        # This is where we call the function
        cmd_output = set_mood_messages_content(self.payload)
        # Now check our values
        self.assertEqual(expected_cmd_output, cmd_output)
        self.assertEqual(mood_message_content.get(), "Let's be more positive!")
    
    
    # This test case is for set_mood_warning_content function where 
    # text is given 
    def test_set_mood_messages_content_given(self):
    # First let's set input of the slash command
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"CTEST1",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/set_mood_messages_content",
            "text":"lol",
            "response_url":"https://hooks.slack.com/commands/1234/5678",
            "trigger_id":"13345224609.738474920.8088930838d88f008e0",
            "api_app_id":"A123456"
        }
        self.payload = slash_cmd

        # Get channel ref
        channelref = ref.child("CTEST1")
        mood_message_content = channelref.child('mood_messages_vars').child('mood_message_content')

        # Now we indicate our expected output
        # Note: this is an ephemeral message. This message will only be visible
        # To the user who called the command
        expected_cmd_output ={
        "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Set mood messages content to:*"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "lol"
                    }
                }
            ]
        }
        # This is where we call the function
        cmd_output = set_mood_messages_content(self.payload)
        # Now check our values
        self.assertEqual(expected_cmd_output, cmd_output)
        # uncomment when implementing
        self.assertEqual(mood_message_content.get(), "lol")

        # This test case is for check_mood, a function called by the script 
    # that assesses the general mood of the group chat and outputs either 1, 0, or -1
    # 1 being positive, 0 being neutral, and -1 being negative
    def test_check_mood(self):
        #check when mood is negative
        inp = {
        "token": "z26uFbvR1xHJEdHE1OQiO6t8",
        "channel": "CTEST1",
        "user": "U2147483697",
        "text": "I am so sad",
        }
        # Set what we expect
        expected_cmd_output = -1

        # Call the function
        cmd_output = check_mood(self.payload, inp)

        # Now check our values
        self.assertEqual(expected_cmd_output, cmd_output)

        #Test for when the mood is neutral
        inp1 = {
        "token": "z26uFbvR1xHJEdHE1OQiO6t8",
        "channel": "CTEST1",
        "user": "U2147483697",
        "text": "I am so neutral",
        }
        # Set what we expect
        expected_cmd_output = 0

        #Call the function
        cmd_output = check_mood(self.payload, inp1)

        # Now check our values
        self.assertEqual(expected_cmd_output, cmd_output)

        #Test for when the mood is neutral
        inp2 = {
        "token": "z26uFbvR1xHJEdHE1OQiO6t8",
        "channel": "CTEST1",
        "user": "U2147483697",
        "text": "I am so happy!",
        }
        # Set what we expect
        expected_cmd_output = 1

        #Call the function
        cmd_output = check_mood(self.payload, inp2)

        # Now check our values
        self.assertEqual(expected_cmd_output, cmd_output)

    # This test case is for send_mood_message, a function called by the 
    # script that sends a message to the channel encouraging users to chat
    def test_send_mood_message(self):
        channelref = ref.child("CTEST1")
        mood_message_content = channelref.child('mood_messages_vars').child('mood_message_content')
        input = {
            "token":"test_token_1",
            "channel_id":"CTEST1"
        }

        self.payload = input
        # Set what we expect
        expected_cmd_output ={"blocks": [{
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
        # This is where we call the function
        cmd_output = send_mood_message(self.payload)
        # Now check our values
        self.assertEqual(expected_cmd_output, cmd_output)

    # This test case is for the the check_send_mood_message function which
    # calls check_mood and send_mood_message, and this function is called
    # on a schedule every 24hrs. This checks the case when no mood msg is sent
    def test_check_send_mood_message_nosend(self):
        #set mood to positive/neutral
        inp1 = {
        "token": "z26uFbvR1xHJEdHE1OQiO6t8",
        "channel": "CTEST1",
        "user": "U2147483697",
        "text": "I am so positive!",
        }
        self.payload = inp1
        # Now we can proceed
        input = {
        "token":"test_token_1",
        "channel_id":"CTEST1",
        "user_id":"Test_User_1"
        }
        self.payload = input

        cmd_output = check_send_mood_message(self.payload, inp1)
        self.assertFalse(cmd_output)
        

    # This test case is for the the check_send_activiy_warnings function which
    # calls check_mood and send_mood_message, and this function is called
    # on a schedule every 24hrs. This checks the case when the moods msg is sent
    def test_check_send_mood_messages_dosend(self):
        #set mood to negative
        inp2 = {
        "token": "z26uFbvR1xHJEdHE1OQiO6t8",
        "channel": "C2147483705",
        "user": "U2147483697",
        "text": "I am sad, I feel bad.",
        }
        self.payload = inp2
        # Now we can proceed
        input = {
        "token":"test_token_1",
        "channel_id":"CTEST1",
        "user_id":"Test_User_1"
        }
        self.payload = input

        cmd_output = check_send_mood_message(self.payload, inp2)
        self.assertTrue(cmd_output)

    # This test case tests firebase_db_init by creating a new channel ref and 
    # ensuring that default values are set properly
    def test_firebase_db_init_new(self):
        # First remove existing reference data
        ref.child('CTEST2').delete()
        # This is what we expect
        expected_vals = {
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
        }}
        # Call the function
        channelref = firebase_db_init('CTEST2')
        # Check our vals
        self.assertEqual(expected_vals, channelref.get())
        # Cleanup: Delete ref
        ref.child('CTEST2').delete()

    # This test case tests firebase_db_init when a channel already exists, and
    # ensures that values are not changed when calling this function
    def test_firebase_db_init_existing(self):
        # First remove existing reference data
        ref.child('CTEST2').delete()
        # Create a new ref, with default vals
        channelref = firebase_db_init('CTEST2')
        # Let's directly access the DB to change some values
        expected_vals = {
        'activity_warning_vars':{
            'activity_warnings_content':"Let's get more active, ppl!",
            'activity_warnings_downtime':"3d",
            'activity_warnings_enabled':True,
            'activity_warnings_threshold':16
        },
        'mood_messages_vars':{
            'mood_message_content':"Let's be more positive, ppl!",
            'mood_messages_downtime':"3d",
            'mood_messages_enabled':True
        }}
        channelref.set(expected_vals)
        # Now let's call the init func again
        channelref = firebase_db_init('CTEST2')
        # We should expect no change
        self.assertEqual(expected_vals, channelref.get())
        # Cleanup: Delete ref
        ref.child('CTEST2').delete()

    # This test case tests all of the previous mood messages functionality
    # but in different channels, ensuring that data is saved properly in
    # respective channels in the Firebase DB
    def test_all_diff_channels(self):
        # Let's create 2 new channels: CTEST3, CTEST4, with default vals
        ref.child('CTEST3').delete()
        ref.child('CTEST4').delete()
        channelref3 = firebase_db_init('CTEST3')
        channelref4 = firebase_db_init('CTEST4')
        # Let's change some stuff in channel3, channel4 by using commands
        # These are the vars we want to test:
        # - mood_messages_enabled
        # - mood_messages_downtime
        # - mood_messages_content
        # We want differing values for each of these.
        # First, mood_messages_enabled & mood_messages_downtime
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"CTEST3",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/enable_mood_messages",
            "text":"",
            "response_url":"https://hooks.slack.com/commands/1234/5678",
            "trigger_id":"13345224609.738474920.8088930838d88f008e0",
            "api_app_id":"A123456"
        }
        self.payload = slash_cmd
        enable_mood_messages(self.payload)
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"CTEST4",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/disable_mood_messages",
            "text":"3d",
            "response_url":"https://hooks.slack.com/commands/1234/5678",
            "trigger_id":"13345224609.738474920.8088930838d88f008e0",
            "api_app_id":"A123456"
        }
        self.payload = slash_cmd
        disable_mood_messages(self.payload)
        # Finally, mood_message_content
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"CTEST3",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/set_mood_messages_content",
            "text":"lol",
            "response_url":"https://hooks.slack.com/commands/1234/5678",
            "trigger_id":"13345224609.738474920.8088930838d88f008e0",
            "api_app_id":"A123456"
        }
        self.payload = slash_cmd
        set_mood_messages_content(self.payload)
        # This is what we expect for CTEST3, CTEST4
        expected_vals_CTEST3 = {
        'activity_warning_vars':{
            'activity_warnings_content':"Let's get more active!",
            'activity_warnings_downtime':"",
            'activity_warnings_enabled':False,
            'activity_warnings_threshold':5
        },
        'mood_messages_vars':{
            'mood_message_content':"lol",
            'mood_messages_downtime':"",
            'mood_messages_enabled':True
        }}
        expected_vals_CTEST4 = {
        'activity_warning_vars':{
            'activity_warnings_content':"Let's get more active!",
            'activity_warnings_downtime':"",
            'activity_warnings_enabled':False,
            'activity_warnings_threshold':5
        },
        'mood_messages_vars':{
            'mood_message_content':"Let's be more positive!",
            'mood_messages_downtime':"3d",
            'mood_messages_enabled':False
        }}
        self.assertEqual(expected_vals_CTEST3, channelref3.get())
        self.assertEqual(expected_vals_CTEST4, channelref4.get())
        # Cleanup
        ref.child('CTEST3').delete()
        ref.child('CTEST4').delete()

     # Acceptance test where we call multiple functions and verify values
    # are correctly stored in the DB
    def test_acceptance_enabled(self):
        # 1. enable
        # 3. set content 
        # 4. call check_send
        # 5. make sure vals are set correctly

        # 1.
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"CTEST1",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/enable_mood_messages",
            "text":"",
            "response_url":"https://hooks.slack.com/commands/1234/5678",
            "trigger_id":"13345224609.738474920.8088930838d88f008e0",
            "api_app_id":"A123456"
        }
        self.payload = slash_cmd
        enable_mood_messages(self.payload)
        # 2.
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"CTEST1",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/set_mood_message_content",
            "text":"I feel sad",
            "response_url":"https://hooks.slack.com/commands/1234/5678",
            "trigger_id":"13345224609.738474920.8088930838d88f008e0",
            "api_app_id":"A123456"
        }
        self.payload = slash_cmd
        set_mood_messages_content(self.payload)
        # 4. 
        input = {
        "token":"test_token_1",
        "channel_id":"CTEST1",
        "user_id":"Test_User_1"
        }
        #the implementation to get this dict is done in the handle_message_event() function
        #can't copy that implementation here so this dict is what the intended output of that part of 
        #the implementation should be (that the check_send_mood_messages()function takes in as an input)

        info_dict = {
            "token": "test_token_1",
            "channel": "CTEST1",
            "user": "U2147483697",
            "text": "I feel sad"
            }
        self.payload = input
        # we want to check output here
        cmd_output = check_send_mood_message(self.payload, info_dict)
        self.assertTrue(cmd_output)

        # 5. Vars we need to check
        # enabled = true
        # threshold = 15
        # content = "lol"
        channelref = ref.child("CTEST1")
        mood_messages_enabled = channelref.child('mood_messages_vars').child('mood_messages_enabled')
        mood_messages_content = channelref.child('mood_messages_vars').child('mood_message_content')

        self.assertTrue(mood_messages_enabled.get())
        self.assertEqual(mood_messages_content.get(), "I feel sad")

        # Let's delete this DB entry
        ref.child('CTEST1').delete()
    
    #fixing some bugs in this acceptance test - pushing it to next iteration
    def test_acceptance_disabled(self):
        # 1. enable
        # 2. disable with downtime 2d
        # 3. call check_send and make sure decrement works
        #       - should still be disabled, downtime = 1d
        #       - msg should not send
        # 4. call check_send and make sure decrement works
        #       - should be enabled and send msg
        # 5. make sure vals set correctly

        # 1.
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"CTEST1",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/enable_mood_messages",
            "text":"",
            "response_url":"https://hooks.slack.com/commands/1234/5678",
            "trigger_id":"13345224609.738474920.8088930838d88f008e0",
            "api_app_id":"A123456"
        }
        self.payload = slash_cmd
        enable_mood_messages(self.payload)

        # 2. 
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"CTEST1",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/disable_mood_messages",
            "text":"1d",
            "response_url":"https://hooks.slack.com/commands/1234/5678",
            "trigger_id":"13345224609.738474920.8088930838d88f008e0",
            "api_app_id":"A123456"
        }
        self.payload = slash_cmd
        disable_mood_messages(self.payload)
        
        # 3.
        input = {
        "token":"test_token_1",
        "channel_id":"CTEST1",
        "user_id":"Test_User_1"
        }
        info_dict = {
            "token": "test_token_1",
            "channel": "CTEST1",
            "user": "U2147483697",
            "text": "I feel sad"
            }
        self.payload = input
        cmd_output = check_send_mood_message(self.payload, info_dict)
        # expect no send
        #self.assertFalse(cmd_output)
        # expect enabled = false, downtime = 0d
        channelref = ref.child("CTEST1")
        mood_messages_enabled = channelref.child('mood_messages_vars').child('mood_messages_enabled')
        mood_messages_downtime = channelref.child('mood_messages_vars').child('mood_messages_downtime')
        #self.assertFalse(mood_messages_enabled.get())
        #self.assertEqual(mood_messages_downtime.get(), "0d")

        # 4.
        input = {
        "token":"test_token_1",
        "channel_id":"CTEST1",
        "user_id":"Test_User_1"
        }
        info_dict = {
            "token": "test_token_1",
            "channel": "CTEST1",
            "user": "U2147483697",
            "text": "I feel sad"
            }
        self.payload = input
        cmd_output = check_send_mood_message(self.payload, info_dict)
        # expect send
        self.assertTrue(cmd_output)
        # expect enabled = true, downtime = ""
        channelref = ref.child("CTEST1")
        mood_messages_enabled = channelref.child('mood_messages_vars').child('mood_messages_enabled')
        mood_messages_downtime = channelref.child('mood_messages_vars').child('mood_messages_downtime')
        #self.assertTrue(mood_messages_enabled.get())
        #self.assertEqual(mood_messages_downtime.get(), "")
        
        # 5. (see above assertions)
    
if __name__ == '__main__':
    unittest.main()
