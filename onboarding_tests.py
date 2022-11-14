import unittest
from onboarding import *

'''
    Note: We discovered that these tests require a user to be active in the workspace; 
          since we were unable to find a workaround for this in the given time frame,
          the onboarding tests have been temporarily omitted from the test suite.
'''

class TestOnboarding(unittest.TestCase):
    def setUp(self):
        #Find a valid user in the workspace to test
        users = web_client.users_list() 
        self.test_user_id = users.get('members')[2].get('id')

        self.general_join_event = {
            "type": "member_joined_channel",
            "user": self.test_user_id,
            "channel": get_channel_id("general"),
            "channel_type": "C",
            "team": "T061EG9R6",
            "inviter": "U123456789"
        }

        self.non_general_join_event = {
            "type": "member_joined_channel",
            "user": self.test_user_id,
            "channel": get_channel_id("random"),
            "channel_type": "C",
            "team": "T061EG9R6",
            "inviter": "U123456789"
        }

        existing_class = 'cmsc-22001'
        if not check_channel(existing_class):
            web_client.conversations_create(name=existing_class, is_private=True)
    
    def test_welcome_new_user(self):
        def make_event_payload(event):
            base_event = {
                "token": "z26uFbvR1xHJEdHE1OQiO6t8",
                "team_id": "T061EG9RZ",
                "api_app_id": "A0FFV41KK",
                "event": event,
                "type": "event_callback",
                "authed_users": [
                    "U061F7AUR"
                ],
                "authorizations": [
                    {
                        "enterprise_id": "E12345",
                        "team_id": "T12345",
                        "user_id": "U12345",
                        "is_bot": False
                    }
                ],
                "event_id": "Ev9UQ52YNA",
                "event_context": "EC12345",
                "event_time": 1234567890
            }

            return base_event

        # Function should return True when message is successfully sent
        self.assertFalse(welcome_new_user(make_event_payload(self.non_general_join_event)))

        rv = welcome_new_user(make_event_payload(self.general_join_event))
        self.assertTrue(rv.get('ok'))

    def test_handle_onboarding(self):
        new_class = 'cmsc-76001'
        existing_class = 'cmsc-22001'
    
        # Checks that a new class was created and student added
        web_client.conversations_kick(channel=get_channel_id(new_class), user=self.test_user_id)
        rv_new = handle_onboarding(new_class, self.test_user_id)
        channel_id = get_channel_id(new_class)
        
        self.assertTrue(rv_new.get('ok'))
        self.assertTrue(check_channel(new_class))

        convo_members = web_client.conversations_members(channel=channel_id)['members']
        self.assertTrue(self.test_user_id in convo_members)

        # Checks that student was added to an existing class
        web_client.conversations_kick(channel=get_channel_id(existing_class), user=self.test_user_id)
        rv_existing = handle_onboarding(existing_class, self.test_user_id)
        channel_id = rv_existing.get('channel').get('id')
        
        self.assertTrue(rv_existing.get('ok'))
        self.assertTrue(check_channel(existing_class)) 
        
        convo_members = web_client.conversations_members(channel=channel_id)['members']
        self.assertTrue(self.test_user_id in convo_members)
        
        
    def test_check_channel(self):
        new_channel = "CMSC-15400"
        existing_channel = "CMSC-22001"
        lwr_existing_channel = "cmsc-22001"
        mixed_existing_channel = "cMsC-22001"
        
        self.assertFalse(check_channel(new_channel))
        self.assertTrue(check_channel(existing_channel))
        self.assertTrue(check_channel(lwr_existing_channel))
        self.assertTrue(check_channel(mixed_existing_channel))

    def test_normalize_channel_name(self):
        pass

    def test_get_channel_name(self):
        pass

    def test_get_channel_id(self):
        pass

    def test_send_im_message(self):
        pass

if __name__ == '__main__':
    unittest.main()
