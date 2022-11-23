import unittest
import time
from bot_meetup import *
import firebase_admin
from firebase_admin import credentials,db

# this first set of unit tests makes sure that the formatting of the time and calculating the value in seconds
# works correctly. "s" after a numerical value represents seconds, "d" represents days, and "h" represents hours, and "m" represents.
# All other letters that are used will cause the number they are after to default to minutes. The omission of s,d,h,m, will cause the input value
# to default to minutes. Arbitrary numbers of spaces should also be valid, and any order of the seconds, minutes, etc. should be valid.
# The unit tests that have #NEW as a comment a line before them are new unit tests for the second iteration. We want to make sure that when the meetup
# function is called with a specific time specified, that it subsequently sends a message to everyone in the channel that there will be a meeting
# in x amount of time, and that depending on what units (s,d,h,m) are used, how the message will be sent. Also, if an opitonal location parameter is 
# added, then that should also be written in the message. Finally, we want to be able to implement firebase in this implementation, so there will be
# unit tests that will test that the database is being updated properly. Those tests will look almost the same, but this time it is going to be testing
# whether firebase is working correctly.

#implement the database
cred = credentials.Certificate(os.environ['SERVICE_KEY'])
firebase_admin.initialize_app(cred, "name")
reminder = db.reference('meetup/')
timestamps = reminder.child('timestamps')

class TestMeetupMessage(unittest.TestCase):
    def test_something(self):
        self.payload = {
                        "type": "message",
                        "channel":"C048LKTG8NS",
                        "user":"U04995560FK",
                        "text":"/meetup 5h",
                        "ts":"13334344"
                }
        # ***THE TESTS FOR THE MEETUP FUNCTION THAT REMAINED THE SAME ARE THAT WAY
        # BECAUSE THESE ARE NEEDED IN ADDITION TO THE NEW FEATURE THAT DETERMINES WHETHER
        # THE MESSAGE THAT IS GENERATED WITH THE MEETUP FUNCTION WAS CORRECTLY SENT TO THE 
        # CHANNEL
        # tests if seconds returns correct second value.
        self.assertEqual(meetup("1s"self.payload), 1)
        #NEW: tests if message is correctly sent in the payload.
        self.assertEqual(self.payload["type"], "meetup in 1 second!")
        # tests if minutes returns correct second value.
        self.assertEqual(meetup("60m",self.payload), 3600)
        #NEW: tests if message is correct sent in the payload.
        self.assertEqual(self.payload["type"], "meetup in 60 minutes!")
        # tests if days returns correct second value.
        self.assertEqual(meetup("1d",self.payload), 86400)
        #NEW: tests if message is correctly sent in the payload.
        self.assertEqual(self.payload["type"], "meetup in 1 day!")
        # tests if multiple units days = d, second = s, minute = m, can return successfully.
        self.assertEqual(meetup("1d30m",self.payload), 88200)
        #NEW: tests if message is correctly sent in the payload.
        self.assertEqual(self.payload["type"], "meetup in 1 day and 30 minutes!")
        # tests whether extra space can return successfully. 
        self.assertEqual(meetup("1d 30m",self.payload), 88200)
        # tests if multipe ordering of the different time units can return successfully.
        self.assertEqual(meetup("30m1d",self.payload), 88200)
        #NEW: the order of the message should be the order that the time(s) were written in the command.
        self.assertEqual(self.payload["type"], "meetup in 30 minutes and 1 day!")
        # tests if an unknown letter/unit is entered that return value defaults to number of seconds
        # per minute
        self.assertEqual(meetup("60q",self.payload), 3600)
        #NEW: tests if message is correctly sent to the payload without s,m,h,d
        self.assertEqual(self.payload["type"],"meetup in 30 minutes!")
        # tests if absence of letter/unit return value defaults to number of seconds per minute
        self.assertEqual(meetup("60",self.payload), 3600)
        # tests whether multiple values, in the absence of a unit, are added together and then
        # return value is converted to number of seconds per minute.
        self.assertEqual(meetup("30 30",self.payload), 3600)
        # check to see if the function works properly with the optional location parameter
        #self.assertEqual(meetup("60m",self.payload, "Zoom"), 3600)
        #check to see that location is added to the message correctly.
        self.assertEqual(self.payload["type"],"meetup up at Zoom in 60 minutes!")

    def test_waitminute(self):
        self.payload = {
            "type": "message",
            "channel": "C048LKTG8NS",
            "user": "U04995560FK",
            "text": "/meetup 5h",
            "ts": "0"
        } 
        # "timestamps" is a reference of the firebase database that holds all of the timestamps that are entered into
        # the database
        # this returns false because no times have been entered into the database yet.
        self.assertFalse(in_five(self.payload))
        # sets the timestamp of the payload to a value that is over five minutes from the current time.
        self.payload["ts"] = time.time() + 1000
        # enteres the d time value, the channel ID, and the message into the database.
        wait_message(self.payload,"reminder for meetup")
        # since d is not within five minutes of the current time, there are no times within the database
        # that are within the current time, so return false.
        self.assertFalse(in_five(self.payload))
        # sets t to a value that is within five seconds of the current time.
        self.payload["ts"] = time.time() + 5
        # this enters a time within five minutes of the current time into database.
        wait_message(self.payload,"reminder for meetup")
        # goes into database, retrieves time value stored at the payload timestamp, and sees if it is successful.
        self.assertEqual(timestamps.child(str(int(self.payload["ts"]))).get(), {self.payload["channel"]: "reminder for meetup"})
        # checks if there are any scheduled reminder messages in five minutes, returns true
        # because t is within five minutes of current time.
        self.assertTrue(in_five(self.payload))


if __name__ == '__main__':
    unittest.main()
# "test.py" 71L, 3315C                                                                                     1, 1           T
