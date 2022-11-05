# slackbot
## Running the tests
**TESTS NOT CURRENTLY WORKING IN THIS BRANCH DUE TO ENV VARIABLES, WILL BE FIXED SOON** <br />
First create the server:<br />
    `python3 bot.py`<br />
Then, to run these tests, use the following command:<br />
    `python -m unittest discover`<br />
*Note* there is a possibility that the local server hostname is inconsistent, <br />
in the event of this, update the GLOB_LOCAL_SERVER variable in test_activity_warnings.py<br /><br />
## Functions tested
These tests are unit tests for the *"Activity Warnings"* functionality of the Slack Bot. This includes the following functions:<br />
 - `enable_activity_warnings()`<br />
 - `disable_activity_warnings()`<br />
 - `set_activity_warnings_threshold()`<br />
 - `set_activity_warnings_content()`<br />
 - `check_activity()`<br />
 - `send_activity_warning()` <br />