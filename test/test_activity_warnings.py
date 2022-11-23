import unittest
from unittest.mock import patch
from iter2_activity_mood_convo_bot import *
import requests

# Filename: test_activity_warnings.py
# 
# Purpose: Test suite containing unit tests for the functionality of the
# activity warnings of the Slack Bot

class Test_Slash_Command_Activity_Warnings(unittest.TestCase): 
    # Expected JSON responses for the relevant events you want to handle for your feature can be 
    # found here: https://api.slack.com/events?filter=Events
    def setUp(self):
        self.payload = {}
        
    # This test case tests the functionality of the function
    # enable_activity_warnings() 
    def test_enable_activity_warnings(self):
        # First let's set input of the slash command
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"CTEST1",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/enable_activity_warnings",
            "text":"",
            "response_url":"https://hooks.slack.com/commands/1234/5678",
            "trigger_id":"13345224609.738474920.8088930838d88f008e0",
            "api_app_id":"A123456"
        }
        self.payload = slash_cmd
        # Get channel ref in firebase db
        channelref = ref.child("CTEST1")
        activity_warnings_threshold = channelref.child('activity_warning_vars').child('activity_warnings_threshold')
        activity_warnings_enabled = channelref.child('activity_warning_vars').child('activity_warnings_enabled')
        # Now we indicate our expected output
        # Note: this is an ephemeral message. This message will only be visible
        # To the user who called the command
        threshold_text = "Activity warning threshold is set to "  + str(activity_warnings_threshold.get())
        if activity_warnings_threshold.get() == 5:
            threshold_text += " (default)."
        else:
            threshold_text += "."
        expected_cmd_output ={
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
                "text": threshold_text
                    }
                }
            ]
        }
        # This is where we call the function
        cmd_output = enable_activity_warnings(self.payload)
        # Now check our values
        self.assertEqual(cmd_output, expected_cmd_output)
        self.assertTrue(activity_warnings_enabled.get()) 
    
    # This test case tests the functionality of the function
    # disable_activity_warnings(), where activity warnings are disabled
    # indefinitely (no parameter given in the function)
    def test_disable_activity_warnings_indefinite(self):
        # First let's set input of the slash command
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"CTEST1",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/disable_activity_warnings",
            "text":"",
            "response_url":"https://hooks.slack.com/commands/1234/5678",
            "trigger_id":"13345224609.738474920.8088930838d88f008e0",
            "api_app_id":"A123456"
        }
        self.payload = slash_cmd
        # Get channel ref
        channelref = ref.child("CTEST1")
        activity_warnings_enabled = channelref.child('activity_warning_vars').child('activity_warnings_enabled')
        activity_warnings_downtime = channelref.child('activity_warning_vars').child('activity_warnings_downtime')

        # Now we indicate our expected output
        # Note: this is an ephemeral message. This message will only be visible
        # To the user who called the command

        expected_cmd_output ={
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
                "text": "Activity warnings disabled indefinitely."
                    }
                }
            ]
        }
        # This is where we call the function
        cmd_output = disable_activity_warnings(self.payload)
        # Now check our values
        self.assertEqual(cmd_output, expected_cmd_output)
        # uncomment when implementing
        self.assertFalse(activity_warnings_enabled.get())
        self.assertEqual("", activity_warnings_downtime.get())
    # This test case tests the functionality of the function
    # disable_activity_warnings(), where activity warnings are disabled
    # for a specified definite downtime
    def test_disable_activity_warnings_definite(self):
        # First let's set input of the slash command
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"CTEST1",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/disable_activity_warnings",
            "text":"3d",
            "response_url":"https://hooks.slack.com/commands/1234/5678",
            "trigger_id":"13345224609.738474920.8088930838d88f008e0",
            "api_app_id":"A123456"
        }
        self.payload = slash_cmd
        payload = self.payload
        # Get channel ref
        channelref = ref.child("CTEST1")
        activity_warnings_downtime = channelref.child('activity_warning_vars').child('activity_warnings_downtime')
        # Now we indicate our expected output
        # Note: this is an ephemeral message. This message will only be visible
        # To the user who called the command
        downtime_response = "Activity warnings disabled for " + payload["text"] + "."
        expected_cmd_output ={
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
        # This is where we call the function
        cmd_output = disable_activity_warnings(self.payload)
        # Now check our values
        self.assertEqual(cmd_output, expected_cmd_output)
        self.assertEqual("3d", activity_warnings_downtime.get())
    
    # This test case is for set_activity_warning_content function where 
    # no text is given (reset to original)
    def test_set_activity_warnings_content_none(self):
    # First let's set input of the slash command
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"CTEST1",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/set_activity_warning_content",
            "text":"",
            "response_url":"https://hooks.slack.com/commands/1234/5678",
            "trigger_id":"13345224609.738474920.8088930838d88f008e0",
            "api_app_id":"A123456"
        }
        self.payload = slash_cmd
        # Get channel ref
        channelref = ref.child("CTEST1")
        activity_warnings_content = channelref.child('activity_warning_vars').child('activity_warnings_content')
        # Now we indicate our expected output
        # Note: this is an ephemeral message. This message will only be visible
        # To the user who called the command
        expected_cmd_output ={
        "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Set activity warnings content to:*"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Let's get more active!"
                    }
                }
            ]
        }
        # This is where we call the function
        cmd_output = set_activity_warnings_content(self.payload)
        # Now check our values
        self.assertEqual(expected_cmd_output, cmd_output)
        self.assertEqual(activity_warnings_content.get(), "Let's get more active!")
    
    # This test case is for the set_activity_warning_threshold function, and 
    # tests to make sure the message returned by the bot is correct
    def test_set_activity_warnings_threshold(self):
    # First let's set input of the slash command
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"CTEST1",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/set_activity_warning_threshold",
            "text":"10",
            "response_url":"https://hooks.slack.com/commands/1234/5678",
            "trigger_id":"13345224609.738474920.8088930838d88f008e0",
            "api_app_id":"A123456"
        }
        self.payload = slash_cmd
        # Get channel ref
        channelref = ref.child("CTEST1")
        activity_warnings_threshold = channelref.child('activity_warning_vars').child('activity_warnings_threshold')
        # Now we indicate our expected output
        # Note: this is an ephemeral message. This message will only be visible
        # To the user who called the command
        expected_cmd_output = {
        "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Set activity warning threshold to 10.*"
            }
        }
            ]
        }
        # This is where we call the function
        cmd_output = set_activity_warnings_threshold(self.payload)
        # Now check our values
        self.assertEqual(expected_cmd_output, cmd_output)
        self.assertEqual(10, activity_warnings_threshold.get()) 
    
    # This test case is for set_activity_warning_content function where 
    # text is given 
    def test_set_activity_warnings_content_given(self):
    # First let's set input of the slash command
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"CTEST1",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/set_activity_warning_content",
            "text":"lol",
            "response_url":"https://hooks.slack.com/commands/1234/5678",
            "trigger_id":"13345224609.738474920.8088930838d88f008e0",
            "api_app_id":"A123456"
        }
        self.payload = slash_cmd
        # Get channel ref
        channelref = ref.child("CTEST1")
        activity_warnings_content = channelref.child('activity_warning_vars').child('activity_warnings_content')
        # Now we indicate our expected output
        # Note: this is an ephemeral message. This message will only be visible
        # To the user who called the command
        expected_cmd_output ={
        "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Set activity warnings content to:*"
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
        cmd_output = set_activity_warnings_content(self.payload)
        # Now check our values
        self.assertEqual(expected_cmd_output, cmd_output)
        # uncomment when implementing
        self.assertEqual(activity_warnings_content.get(), "lol")

    # This test case is for check_activity, a function called by the script 
    # that checks how many messages have been sent in a channel in the past 24hr
    def test_check_activity(self):
        input = {
        "token":"test_token_1",
        "channel_id":"CTEST1"
        }
        self.payload = input
        # Set what we expect
        expected_cmd_output = 10
        
        # This is where we call the function
        cmd_output = check_activity(self.payload)

        # Now check our values
        self.assertEqual(expected_cmd_output, cmd_output)

    # This test case is for send_activity_warning, a function called by the 
    # script that sends a message to the channel encouraging users to chat
    def test_send_activity_warning(self):
        channelref = ref.child("CTEST1")
        activity_warnings_content = channelref.child('activity_warning_vars').child('activity_warnings_content')
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
            "text": "*Activity Warning Message*"
        }},{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": activity_warnings_content.get()
        }}]}
        # This is where we call the function
        cmd_output = send_activity_warning(self.payload)
        # Now check our values
        self.assertEqual(expected_cmd_output, cmd_output)
    
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

    # This test case tests all of the previous activity warning functionality
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
        # - activity_warnings_enabled
        # - activity_warnings_threshold
        # - activity_warnings_downtime
        # - activity_warnings_content
        # We want differing values for each of these.
        # First, activity_warnings_enabled & activity_warnings_downtime
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"CTEST3",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/enable_activity_warnings",
            "text":"",
            "response_url":"https://hooks.slack.com/commands/1234/5678",
            "trigger_id":"13345224609.738474920.8088930838d88f008e0",
            "api_app_id":"A123456"
        }
        self.payload = slash_cmd
        enable_activity_warnings(self.payload)
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"CTEST4",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/disable_activity_warnings",
            "text":"3d",
            "response_url":"https://hooks.slack.com/commands/1234/5678",
            "trigger_id":"13345224609.738474920.8088930838d88f008e0",
            "api_app_id":"A123456"
        }
        self.payload = slash_cmd
        disable_activity_warnings(self.payload)
        # Next, activity_warnings_threshold
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"CTEST3",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/set_activity_warning_threshold",
            "text":"10",
            "response_url":"https://hooks.slack.com/commands/1234/5678",
            "trigger_id":"13345224609.738474920.8088930838d88f008e0",
            "api_app_id":"A123456"
        }
        self.payload = slash_cmd
        set_activity_warnings_threshold(self.payload)
        # Finally, activity_warnings_content
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"CTEST3",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/set_activity_warning_content",
            "text":"lol",
            "response_url":"https://hooks.slack.com/commands/1234/5678",
            "trigger_id":"13345224609.738474920.8088930838d88f008e0",
            "api_app_id":"A123456"
        }
        self.payload = slash_cmd
        set_activity_warnings_content(self.payload)
        # This is what we expect for CTEST3, CTEST4
        expected_vals_CTEST3 = {
        'activity_warning_vars':{
            'activity_warnings_content':"lol",
            'activity_warnings_downtime':"",
            'activity_warnings_enabled':True,
            'activity_warnings_threshold':10
        },
        'mood_messages_vars':{
            'mood_message_content':"Let's be more positive!",
            'mood_messages_downtime':"",
            'mood_messages_enabled':False
        }}
        expected_vals_CTEST4 = {
        'activity_warning_vars':{
            'activity_warnings_content':"Let's get more active!",
            'activity_warnings_downtime':"3d",
            'activity_warnings_enabled':False,
            'activity_warnings_threshold':5
        },
        'mood_messages_vars':{
            'mood_message_content':"Let's be more positive!",
            'mood_messages_downtime':"",
            'mood_messages_enabled':False
        }}
        self.assertEqual(expected_vals_CTEST3, channelref3.get())
        self.assertEqual(expected_vals_CTEST4, channelref4.get())
        # Cleanup
        ref.child('CTEST3').delete()
        ref.child('CTEST4').delete()
    # This test case is for the the check_send_activiy_warnings function which
    # calls check_activity and send_activity_message, and this function is called
    # on a schedule every 24hrs. This checks the case when no activity msg is sent
    def test_check_send_activity_warnings_nosend(self):

        # The test for check_activity uses 10 msgs. So we want to change the 
        # threshold real quick to a value less than 10
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"CTEST1",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/set_activity_warning_threshold",
            "text":"5",
            "response_url":"https://hooks.slack.com/commands/1234/5678",
            "trigger_id":"13345224609.738474920.8088930838d88f008e0",
            "api_app_id":"A123456"
        }
        self.payload = slash_cmd
        set_activity_warnings_threshold(self.payload)
        # Now we can proceed
        input = {
        "token":"test_token_1",
        "channel_id":"CTEST1",
        "user_id":"Test_User_1"
        }
        self.payload = input

        cmd_output = check_send_activity_warning(self.payload)
        self.assertFalse(cmd_output)
        

    # This test case is for the the check_send_activiy_warnings function which
    # calls check_activity and send_activity_message, and this function is called
    # on a schedule every 24hrs. This checks the case when the activity msg is sent
    def test_check_send_activity_warnings_dosend(self):
    

        # The test for check_activity uses 10 msgs. So we want to change the 
        # threshold real quick to a value more than or equal to 10
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"CTEST1",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/set_activity_warning_threshold",
            "text":"15",
            "response_url":"https://hooks.slack.com/commands/1234/5678",
            "trigger_id":"13345224609.738474920.8088930838d88f008e0",
            "api_app_id":"A123456"
        }
        self.payload = slash_cmd
        set_activity_warnings_threshold(self.payload)
        # Now we can proceed
        input = {
        "token":"test_token_1",
        "channel_id":"CTEST1",
        "user_id":"Test_User_1"
        }
        self.payload = input

        cmd_output = check_send_activity_warning(self.payload)
        self.assertTrue(cmd_output)
    
    # Acceptance test where we call multiple functions and verify values
    # are correctly stored in the DB
    def test_acceptance_enabled(self):
        # 1. enable
        # 2. set threshold
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
            "command":"/enable_activity_warnings",
            "text":"",
            "response_url":"https://hooks.slack.com/commands/1234/5678",
            "trigger_id":"13345224609.738474920.8088930838d88f008e0",
            "api_app_id":"A123456"
        }
        self.payload = slash_cmd
        enable_activity_warnings(self.payload)
        # 2.
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"CTEST1",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/set_activity_warning_threshold",
            "text":"15",
            "response_url":"https://hooks.slack.com/commands/1234/5678",
            "trigger_id":"13345224609.738474920.8088930838d88f008e0",
            "api_app_id":"A123456"
        }
        self.payload = slash_cmd
        set_activity_warnings_threshold(self.payload)
        # 3.
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"CTEST1",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/set_activity_warning_content",
            "text":"lol",
            "response_url":"https://hooks.slack.com/commands/1234/5678",
            "trigger_id":"13345224609.738474920.8088930838d88f008e0",
            "api_app_id":"A123456"
        }
        self.payload = slash_cmd
        set_activity_warnings_content(self.payload)
        # 4. threshold is 15 (see above) so we expect it to send msg
        input = {
        "token":"test_token_1",
        "channel_id":"CTEST1",
        "user_id":"Test_User_1"
        }
        self.payload = input
        # we want to check output here
        cmd_output = check_send_activity_warning(self.payload)
        self.assertTrue(cmd_output)

        # 5. Vars we need to check
        # enabled = true
        # threshold = 15
        # content = "lol"
        channelref = ref.child("CTEST1")
        activity_warnings_threshold = channelref.child('activity_warning_vars').child('activity_warnings_threshold')
        activity_warnings_enabled = channelref.child('activity_warning_vars').child('activity_warnings_enabled')
        activity_warnings_content = channelref.child('activity_warning_vars').child('activity_warnings_content')

        self.assertTrue(activity_warnings_enabled.get())
        self.assertEqual(activity_warnings_threshold.get(), 8)
        self.assertEqual(activity_warnings_content.get(), "lol")

        # Let's delete this DB entry
        ref.child('CTEST1').delete()
    # def test_acceptance_disabled(self):

        

if __name__ == '__main__':
    unittest.main()