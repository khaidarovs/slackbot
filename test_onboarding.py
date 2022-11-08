import unittest
from onboarding import *

class TestOnboarding(unittest.TestCase):
    def setUp(self):
        self.channel_join_payload = {
            "type": "member_joined_channel",
            "user": "W06GH7XHN",
            "channel": "C0698JE0H",
            "channel_type": "C",
            "team": "T061EG9R6",
            "inviter": "U123456789"
        }
    
    def test_welcome_new_user(self):
        # Function should return True when message is successfully sent
        self.assertTrue(welcome_new_user(self.channel_join_payload)) 

        #Check that the sent message is the same as the received message
        #Triggered when Slackbot gets a direct message  
        msg_event_received = {
            "token": "one-long-verification-token",
            "team_id": "T061EG9R6",
            "api_app_id": "A0PNCHHK2",
            "event": {
                "type": "message",
                "channel": "D024BE91L",
                "user": "U2147483697",
                "text": "Welcome to StudyRoom! To join a class, message me with the command `/join_class SUBJ-#####` (for example, `/join_class CMSC-22001), and I'll add you the study group.",
                "ts": "1355517523.000005",
                "event_ts": "1355517523.000005",
                "channel_type": "im"
            },
            "type": "event_callback",
            "authed_teams": [
                "T061EG9R6"
            ],
            "event_id": "Ev0PV52K21",
            "event_time": 1355517523
        }

        #The message received by the user is accessed through the above JSON
        msg_received =  msg_event_received['event']['text']

        #Check that the message sent is equal to the message received
            #self.assertEqual(msg_sent, msg_received)  #<=== commented out because msg_sent was not defined, not sure what that's supposed to be

        #Check that the message sent and events are equal
        self.assertEqual(welcome_new_user(self.channel_join_payload), 
                         msg_event_received)


    def test_handle_onboarding(self):
        new_class = 'cmsc-76001'
        existing_class = 'cmsc-22001'

        #Find a valid user in the workspace to test
        users = web_client.users_list()
        test_user_id = users.get('members')[2].get('id')
    
        # Checks that a new class was created and student added
        #grace--web_client.conversations_kick(channel=get_channel_id(new_class), user=test_user_id)
        rv_new = handle_onboarding(new_class, test_user_id)
        channel_id=get_channel_id(new_class)
        # channel_id = rv_new.get('channel').get('id')
        
        self.assertTrue(rv_new.get('ok'))
        self.assertTrue(check_channel(new_class))

        convo_members = web_client.conversations_members(channel=channel_id)['members']
        self.assertTrue(test_user_id in convo_members)
        # Cleanup tests for next run
        ### web_client.conversations_kick(channel=channel_id, user=test_user_id)


        # Checks that student was added to an existing class
        #grace--web_client.conversations_kick(channel=get_channel_id(existing_class), user=test_user_id)
        rv_existing = handle_onboarding(existing_class, test_user_id) #where are we creating existing class? 
        #also do you mean existing_class here ^  instead of new_class?
        channel_id = rv_existing.get('channel').get('id')
        
        self.assertTrue(rv_existing.get('ok'))
        self.assertTrue(check_channel(existing_class)) 
        
        convo_members = web_client.conversations_members(channel=channel_id)['members']
        self.assertTrue(test_user_id in convo_members)
        # Cleanup tests for next run
        ### web_client.conversations_kick(channel=channel_id, user=test_user_id)
        
        
    def test_check_channel(self):
        new_channel = "CMSC-15400"
        existing_channel = "CMSC-22001"
        lwr_existing_channel = "cmsc-22001"
        mixed_existing_channel = "cMsC-22001"

        self.assertFalse(check_channel(new_channel))
        self.assertTrue(check_channel(existing_channel))
        self.assertTrue(check_channel(lwr_existing_channel))
        self.assertTrue(check_channel(mixed_existing_channel))

if __name__ == '__main__':
    unittest.main()