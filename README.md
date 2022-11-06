# slackbot
## Running the tests
First, run the bot to set up connection to the Firebase DB<br />
    `python bot.py`<br />
To run the tests, use the following command:<br />
    `python -m unittest discover`<br />
*Note:* 
Running the bot requires access to the .env file and Firebase DB, which 
contain sensitive information and cannot be posted on GitHub.
Contact a SlackBot dev if you do not have these files.<br />

## Functions tested
These tests are unit tests for the *"Activity Warnings"* functionality of the 
Slack Bot. This includes the following functions:<br />
 - `enable_activity_warnings()`<br />
 - `disable_activity_warnings()`<br />
 - `set_activity_warnings_threshold()`<br />
 - `set_activity_warnings_content()`<br />
 - `check_activity()`<br />
 - `send_activity_warning()` <br />

 ## Notes
 Currently, the Activity Warnings feature only can be run in one place at a time,
 as the Firebase DB has not been fully configured to handle multiple channels and 
 servers. This will be fixed in a future sprint.