import unittest
from bot import *

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
        class_name = 'CMSC-15400'
        created_channel = {
            "type": "channel_created",
            "channel": {
                "id": "C024BE91L",
                "name": "CMSC-15400",
                "created": 1360782804,
                "creator": "U024BE7LH"
            }
        }

        invite = {
        "type": "shared_channel_invite_received",
        "invite": {
            "id": "C024BE91L",
            "date_created": 1626876000,
            "date_invalid": 1628085600,
            "inviting_team": {
            "id": "T12345678",
            "name": "CMSC-15400",
            "icon": "https://placekitten.com/24/24",
            "is_verified": false,
            "domain": "corgis",
            "date_created": 1480946400
            },
            "inviting_user": {
            "id": "U12345678",
            "team_id": "T12345678",
            "name": "crus",
            "updated": 1608081902,
            "profile": {
                "real_name": "Corgis Rus",
                "display_name": "Corgis Rus",
                "real_name_normalized": "Corgis Rus",
                "display_name_normalized": "Corgis Rus",
                "team": "T12345678",
                "avatar_hash": "gcfh83a4c72k",
                "email": "corgisrus@slack-corp.com",
                "image_24": "https://placekitten.com/24/24",
                "image_32": "https://placekitten.com/32/32",
                "image_48": "https://placekitten.com/48/48",
                "image_72": "https://placekitten.com/72/72",
                "image_192": "https://placekitten.com/192/192",
                "image_512": "https://placekitten.com/512/512"
            }
            },
            "recipient_user_id": "U87654321"
        },
        "channel": {
            "id": "C12345678",
            "is_private": false,
            "is_im": false,
            "name": "test-slack-connect"
        },
        "event_ts": "1626876010.000100"
        }

        channel_list = {
            "ok": true,
            "channels": [
                {
                    "id": "C012AB3CD",
                    "name": "general",
                    "is_channel": true,
                    "is_group": false,
                    "is_im": false,
                    "created": 1449252889,
                    "creator": "U012A3CDE",
                    "is_archived": false,
                    "is_general": true,
                    "unlinked": 0,
                    "name_normalized": "general",
                    "is_shared": false,
                    "is_ext_shared": false,
                    "is_org_shared": false,
                    "pending_shared": [],
                    "is_pending_ext_shared": false,
                    "is_member": true,
                    "is_private": false,
                    "is_mpim": false,
                    "topic": {
                        "value": "Company-wide announcements and work-based matters",
                        "creator": "",
                        "last_set": 0
                    },
                    "purpose": {
                        "value": "This channel is for team-wide communication and announcements. All team members are in this channel.",
                        "creator": "",
                        "last_set": 0
                    },
                    "previous_names": [],
                    "num_members": 4
                },
                {
                    "id": "C024BE91L",
                    "name": "CMSC-15400",
                    "is_channel": true,
                    "is_group": false,
                    "is_im": false,
                    "created": 1449252889,
                    "creator": "U061F7AUR",
                    "is_archived": false,
                    "is_general": false,
                    "unlinked": 0,
                    "name_normalized": "random",
                    "is_shared": false,
                    "is_ext_shared": false,
                    "is_org_shared": false,
                    "pending_shared": [],
                    "is_pending_ext_shared": false,
                    "is_member": true,
                    "is_private": false,
                    "is_mpim": false,
                    "topic": {
                        "value": "Non-work banter and water cooler conversation",
                        "creator": "",
                        "last_set": 0
                    },
                    "purpose": {
                        "value": "A place for non-work-related flimflam, faffing, hodge-podge or jibber-jabber you'd prefer to keep out of more focused work-related channels.",
                        "creator": "",
                        "last_set": 0
                    },
                    "previous_names": [],
                    "num_members": 4
                }
            ],
            "response_metadata": {
                "next_cursor": "dGVhbTpDMDYxRkE1UEI="
            }
        }

        #Returns true when a channel is created
        self.assertTrue(create_channel())
        #Checks that there is a Channel created for the class with the class name
        self.assertEqual(create_channel(class_name).payload, created_channel)

        #Returns true when an invite to a channel is sent
        self.assertTrue(join_channel())
        #Checks that the user was invited to the channel for their class
        self.assertEqual(join_channel(class_name).payload, invite)

        #there should be an additional test case for an existing class.
        
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