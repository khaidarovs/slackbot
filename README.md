# Overview
For Iter2 Submission A, Please see iter2-activity-mood-convo branch for instructions
on running tests. This branch should NOT be used in grading for this submission. :)

# Testing

In order to run the tests:

1. cd into the slackbot directory 
2. Place the `slackbot-v1-firebase-adminsdk-n7ggn-fcdad3e5ca.json` inside the slackbot directory before running the tests
3. Run `pip install -r requirements.txt` to install the necessary requirements
4. Run the tests using the commands below:

`python -m unittest test/test_mood_messages.py test/test_convo_summary.py test/test_activity_warnings.py`

or 

`python3 -m unittest test/test_mood_messages.py test/test_convo_summary.py test/test_activity_warnings.py`

Each feature is described in more detail below

# ITER2 - Activity Warnings
The iteration finalized the activity warnings feature. 
This encompasses the following<br>
1. Scheduling messages to send
2. Firebase support for multiple channels <br>
Unit tests for both of these features have been added. However, there are 
some practical issues with testing scheduling that make it difficult to test (i.e.
making sure the functions are called at the right times). Thus, we are just 
testing the functionality of the functions called by the scheduler. <br>
# ITER2 - Conversation Summary
Conversation summary is a new feature that is a response to a slash command 
`/summarize_conversation` which summarizes the conversation in the past 6 
hrs. Because the conversation summary will differ each time due to NLP, our two
test cases check if there are 0 msgs in the past 6 hrs, or if there are >0 msgs,
and test the correct behavior for each case<br>
Note that we plan to extend this feature to allow for an aribtrary amount of 
time as opposed to fixed 6 hour conversation history period
# ITER2 - Mood Messages
This iteration finalized the mood messages feature
This encompasses the following<br>
1. Making sure send message is only implemented when the mood is negative
2. Scheduling messages to send
3. Firebase support for multiple channels <br>
Unit tests for all three of these features have been added. However, there are 
some practical issues with testing scheduling that make it difficult to test (i.e.
making sure the functions are called at the right times). Thus, we are just 
testing the functionality of the functions called by the scheduler. <br>
