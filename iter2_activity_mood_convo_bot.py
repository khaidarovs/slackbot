# This file is the Iteration 2 run-file for:
# - activity_warnings_bot.py
# - convo_summary_bot.py
# - mood_messages_bot.py
# For all tests related to these features, YOU MUST RUN THIS FILE before running
# the tests

# Import our bots 
from activity_warnings_bot import *
from convo_summary_bot import *
from mood_messages_bot import *


# Allows us to set up a webpage with the script, which enables testing using tools like ngrok.
if __name__ == "__main__":
    bot_app.run(debug=True)

    