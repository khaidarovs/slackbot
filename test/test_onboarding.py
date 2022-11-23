import unittest
from onboarding import *

class TestOnboarding(unittest.TestCase):
    def setUp(self):
        self.test_user_id = 'T3sTID'

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

        existing_class = 'cmsc-22002'
        if not check_channel(existing_class):
            web_client.conversations_create(name=existing_class, is_private=True)
    

    # Tests if the welcome message is sent when an new user joins the workspace
    def test_welcome_new_user(self):
        def make_event_payload(event):
            base_event = {
                "event": event,
            }
            return base_event

        # Function should return True when message is successfully sent
        self.assertFalse(welcome_new_user(make_event_payload(self.non_general_join_event)))

        rv = welcome_new_user(make_event_payload(self.general_join_event))
        self.assertTrue(rv.get('ok'))

    # Deferred 
    def test_handle_onboarding(self):
        new_class = 'cmsc-99998'
        existing_class = 'cmsc-22002'
    
        # Checks that a new class was created and student added
        rv_new = handle_onboarding(new_class, self.test_user_id)
        
        self.assertTrue(rv_new.get('ok'))
        self.assertTrue(check_channel(new_class))

        # Checks that student was added to an existing class
        rv_existing = handle_onboarding(existing_class, self.test_user_id)
        
        self.assertTrue(rv_existing.get('ok'))
        self.assertTrue(check_channel(existing_class)) 

    # Tests if the channel exists     
    def test_check_channel(self):
        new_channel = "CMSC-15400"
        existing_channel = "CMSC-22002"
        lwr_existing_channel = "cmsc-22002"
        mixed_existing_channel = "cMsC-22002"
        
        self.assertFalse(check_channel(new_channel))
        self.assertTrue(check_channel(existing_channel))
        self.assertTrue(check_channel(lwr_existing_channel))
        self.assertTrue(check_channel(mixed_existing_channel))

    # Tests if the course name in channel name becomes all lowercase
    def test_normalize_channel_name(self):
        capital = "CMSC-22222"
        lower = "span-12345"
        mixed = "sOSc-87462"

        self.assertEqual(normalize_channel_name(capital), "cmsc-22222")
        self.assertEqual(normalize_channel_name(lower), "span-12345")
        self.assertEqual(normalize_channel_name(mixed), "sosc-87462")


    # Tests for get_channel_name and get_channel_id
    def test_get_channel_info(self):
        channels = fetch_conversations()
        channel_ids = [el[0] for el in channels]

        general_id = get_channel_id("general")
        self.assertTrue(general_id in channel_ids)
        
        general_name = get_channel_name(general_id)
        self.assertEqual(general_name, "general")
        

        random_id = get_channel_id("random")
        self.assertTrue(random_id in channel_ids)

        random_name = get_channel_name(random_id)
        self.assertEqual(random_name, "random")

        fake_channel_id = get_channel_id("fake-channel")
        self.assertFalse(fake_channel_id in channel_ids)

        fake_channel_name = get_channel_name(fake_channel_id)
        self.assertEqual(fake_channel_name, None)

    # Tests that a IM message was sent successfully
    def test_send_im_message(self):
        rv = send_im_message(self.test_user_id, "this is a test message")
        self.assertTrue(rv.get('ok'))

        rv = send_im_message("NotAUser", "this is a test message")
        self.assertTrue(isinstance(rv, SlackApiError))

if __name__ == '__main__':
    unittest.main()
