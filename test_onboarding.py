import unittest

# I wrote comments to outline what we should look to test in each func as a jumping off point.
# We can get rid of these once we implement them. -Sabine

class TestOnboarding(unittest.TestCase):
    def test_welcome_new_user(self):
        msg = "Welcome to StudyRoom! To join a class, message me with the command `/join_class SUBJ-#####` (for example, `/join_class CMSC-22001), and I'll add you the study group."
        user = test_user 
        
        # Function should return True when message is successfully sent
        self.assertTrue(welcome_new_user()) 

        #check what was sent somehow and verify that it matches msg

    def test_handle_onboarding(self):
        ''' 
        Uses input from /handle_slash_command to first check if class exists, then add student to class.
        - also handles creating class if it doesn't exist

        Calls check_channel, create_channel (where applicable), join_channel

        I think we can assume that the class will be formatted well based on discord notes.

        Returns True on success, error code on failure.
        '''

    def test_check_channel(self):
        '''
        Test cases:
            - behavior when class channel doesn't exist
            - behavior when class channel does exist
        '''

        new_channel = "CMSC-15400"
        existing_channel = "CMSC-22001"
        lwr_existing_channel = "cmsc-22001"
        channel_obj = client.conversations_create(name=existing_channel, is_private=True)

        self.assertFalse(check_channel(new_channel))
        self.assertTrue(check_channel(existing_channel))
        self.assertTrue(check_channel(lwr_existing_channel))

if __name__ == '__main__':
    unittest.main()