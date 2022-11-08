import unittest
from onboarding import *

class TestOnboarding(unittest.TestCase):
    def setUp(self):
        self.general_join_payload = {
            "type": "member_joined_channel",
            "user": "W06GH7XHN",
            "channel": "C049FJF4VN2",
            "channel_type": "C",
            "team": "T061EG9R6",
            "inviter": "U123456789"
        }

        self.non_general_join_payload = {
            "type": "member_joined_channel",
            "user": "W06GH7XHN",
            "channel": "C04A0RNAV09",
            "channel_type": "C",
            "team": "T061EG9R6",
            "inviter": "U123456789"
        }
    
    def test_welcome_new_user(self):
        # Function should return True when message is successfully sent
        self.assertFalse(welcome_new_user(self.non_general_join_payload))
        self.assertTrue(welcome_new_user(self.general_join_payload).get('ok')) #???


    def test_handle_onboarding(self):
        new_class = 'cmsc-76001'
        existing_class = 'cmsc-15400'
        
        #Find a valid user in the workspace to test
        users = web_client.users_list()
        test_user_id = users.get('members')[2].get('id')

        # Checks that a new class was created and student added
        rv_new = handle_onboarding(new_class, test_user_id)
        channel_id = rv_new.get('channel').get('id')
        
        self.assertTrue(rv_new.get('ok'))
        self.assertTrue(check_channel(new_class))

        convo_members = web_client.conversations_members(channel=channel_id)
        self.assertTrue(test_user_id in convo_members)
        
        # Cleanup tests for next run
        ### web_client.conversations_kick(channel=channel_id, user=test_user_id)


        # Checks that student was added to an existing class
        rv_existing = handle_onboarding(new_class, test_user_id)
        channel_id = rv_existing.get('channel').get('id')
        
        self.assertTrue(rv_existing.get('ok'))
        self.assertTrue(check_channel(existing_class))
        
        convo_members = web_client.conversations_members(channel=channel_id)
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