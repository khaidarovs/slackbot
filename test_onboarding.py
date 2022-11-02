import unittest
import onboarding

class TestOnboarding(unittest.TestCase):
    def test_welcome_new_user(self):
        # Function should return True when message is successfully sent
        self.assertTrue(welcome_new_user())

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
        msg_received =  msg_event_received['event'][0]['text']

        #Check that the message sent is equal to the message received
        self.assertEqual(msg_sent, msg_received)
        #Check that the message sent and events are equal
        self.assertEqual(welcome_new_user().payload, msg_event_received)


    def test_handle_onboarding(self):
        new_class = 'CMSC-22001'
        existing_class = 'CMSC-15400'
        
        
        test_user_id = 'ABCD1234'
        
        new_created_channel = {
            "type": "channel_created",
            "channel": {
                "id": "C024BE91L",
                "name": "CMSC-22001",
                "created": 1360782804,
                "creator": "U024BE7LH"
            }
        }

        existing_created_channel = {
            "type": "channel_created",
            "channel": {
                "id": "C024BE91L",
                "name": "CMSC-15400",
                "created": 1360782804,
                "creator": "U024BE7LH"
            }
        }

        # Checks that a new class was created and student added
        self.assertTrue(handle_onboarding(new_class))
        self.assertTrue(new_created_channel in web_client.conversations_list)
        self.assertTrue(test_user_id in web_client.conversations_members)

        # Checks that student was added to an existing class
        self.assertTrue(handle_onboarding(existing_class))
        self.assertTrue(existing_created_channel in web_client.conversations_list)
        self.assertTrue(test_user_id in web_client.conversations_members)
        
        
    def test_check_channel(self):
        new_channel = "CMSC-15400"
        existing_channel = "CMSC-22001"
        lwr_existing_channel = "cmsc-22001"
        channel_obj = web_client.conversations_create(name=existing_channel, is_private=True)

        self.assertFalse(check_channel(new_channel))
        self.assertTrue(check_channel(existing_channel))
        self.assertTrue(check_channel(lwr_existing_channel))

if __name__ == '__main__':
    unittest.main()