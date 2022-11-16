# Testing

In order to run the tests:

1. cd into the slackbot directory 
2. Place the `slackbot-v1-firebase-adminsdk-n7ggn-fcdad3e5ca.json` inside the slackbot directory before running the tests
3. Run `pip install -r requirements.txt` to install the necessary requirements
4. Run the tests using the commands below:

`python -m unittest test/test_convo_summary.py`

or 

`python3 -m unittest test/test_convo_summary.py`

Each feature is described in more detail below

# ITER2 - Conversation Summary
Conversation summary is a new feature that is a response to a slash command 
`/summarize_conversation [hrs]` which summarizes the conversation in the past N 
hrs. Because the conversation summary will differ each time due to NLP, our two
test cases check if there are 0 msgs in the past N hrs, or if there are >0 msgs,
and test the correct behavior for each case
