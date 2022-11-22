# Import utils
from iter2_activity_mood_convo_utils import *

# Functions we'd implement would be here.
def summarize_conversation(self):
    # Get dataa
    payload = self.payload

    # First check if this is a test or not
    is_test = False
    if payload.get('token') == "test_token_1":
        is_test = True
    
    if is_test:
        msgs = payload.get('dummy_messages')
        n_msgs = len(msgs)
        msg_sent = False
        if n_msgs > 0:
            msg_sent = True
        return n_msgs, msg_sent
    # The Following lines only apply to only real invocations of this function
    # (non-test)
    

# Allows us to set up a webpage with the script, which enables testing using tools like ngrok.
if __name__ == "__main__":
    bot_app.run(debug=True)