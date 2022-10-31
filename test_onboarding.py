import unittest

# I wrote comments to outline what we should look to test in each func as a jumping off point.
# We can get rid of these once we implement them. -Sabine

class TestOnboarding(unittest.TestCase):
    def test_member_joined_workspace(self):
        '''
            ngl I'm not quite sure what this is/why it's needed in addition to 
            welcome_new_user- it seemed to me like this is an event, not a function
            we have to implement? Am I wrong?
        '''
        pass

    def test_welcome_new_user(self):
        '''
        Test cases:
            - team_join event
        '''
        pass

    def test_slash_class_input(self):
        '''
        Test cases:
            - valid slash command with existing class
            - valid slash command with non-existing class
            - invalid slash command

            Note - why is this needed as a middleman between handle_slash_command
                   and check_classes? What's the output of handle_slash_command?
        '''
        pass

    def test_check_channel(self):
        '''
        Test cases:
            - behavior when class channel doesn't exist
            - behavior when class channel does exist
        '''
        pass

    def test_output_msg_class_channels(self):
        '''
        Test cases:
            - behavior when class channel exists
            - behavior when class channel doesn't exist
        '''
        pass

    def test_slash_create_channel(self):
        '''
        Test cases:
            - valid class as input
            - invalid class as input

            Note - should we be instructing the user to do this command when
                   a class doesn't exist, or should the bot just run this 
                   command on its own in the background?
        '''
        pass

    def test_join_channel(self):
        '''
        Test cases:
            - existing channels
            - nonexisting channels
        '''
        pass

if __name__ == '__main__':
    unittest.main()