# Import utils
from iter2_activity_mood_convo_utils import *
from bot_events_commands import actual_bot_user_id
import nltk
nltk.download("stopwords")
nltk.download("punkt")
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import re

# Helper function that takes in a string as an input and returns 
# another string which is a summary of the input text
def summary_model(text):
    # Tokenizing the text
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text)
    
    # Creating a frequency table to keep the score of each word
    freq_table = dict()
    for word in words:
        word = word.lower()
        if word in stop_words:
            continue
        if word in freq_table:
            freq_table[word] += 1
        else:
            freq_table[word] = 1
    
    # Creating a dictionary to keep the score of each sentence
    sentences = sent_tokenize(text)
    sentence_value = dict()
    
    for sentence in sentences:
        for word, freq in freq_table.items():
            if word in sentence.lower():
                if sentence in sentence_value:
                    sentence_value[sentence] += freq
                else:
                    sentence_value[sentence] = freq

    sum_vals = 0
    for sentence in sentence_value:
        sum_vals += sentence_value[sentence]
    
    # Average value of a sentence from the original text
    if sentence_value != 0:
        average = int(sum_vals / len(sentence_value))
    
    # Storing sentences into our summary
    summary = ''
    for sentence in sentences:
        if (sentence in sentence_value) and (sentence_value[sentence] > (1.2 * average)):
            summary += " " + sentence
    if summary == "":
        for sentence in sentences:
            summary += sentence
    return summary

# Helper function that parses a list of set objects (the output from 
# payload.get('dummy_messages')) to return a single string with all the messages 
def parse_messages(messages, is_test):
    output_string = ''
    for i in range(len(messages)):
        if is_test:
            string = str(messages[i]["text"]) 
            new_str = re.sub("{'", '', string)
            final_str = re.sub("'}", ' ', new_str)
            final_str1 = re.sub('{"', '', final_str)
            final_str2 = re.sub('"}', ' ', final_str1)
            output_string += final_str2
            output_string += "\n"
        elif messages[i]["user"] != actual_bot_user_id:
            user_name = ""
            user_rv = web_client.users_info(user = messages[i]["user"])
            if not user_rv["ok"]:
                print(user_rv["error"]) 
                user_name = "A user says "
            else:
                user_name = user_rv["user"]["name"] + " says "
            string = user_name + str(messages[i]["text"]) 
            new_str = re.sub("{'", '', string)
            final_str = re.sub("'}", ' ', new_str)
            final_str1 = re.sub('{"', '', final_str)
            final_str2 = re.sub('"}', ' ', final_str1)
            output_string += final_str2
            output_string += "\n"
    return output_string

# Main function that calls the above two helper functions
def summarize_conversation(payload):
    # First check if this is a test or not
    is_test = False
    if payload.get('token') == "test_token_1":
        is_test = True
    channel_id = payload.get('channel_id')
    conversation_history = []
    n_msgs = 0
    # Get the msgs
    if is_test:
        conversation_history = payload.get('dummy_messages')
        n_msgs = len(conversation_history)
    else:
        time_6hrago = time.time() - 21600
        history_query = {
        "token":BOT_TOKEN,
        "channel":channel_id,
        "oldest":time_6hrago
        # "limit":activity_warnings_threshold.get()
        }
        retval = web_client.conversations_history(channel=history_query["channel"], limit=10)#, oldest=history_query["oldest"])
        conversation_history = retval["messages"]
        print("================Number of Messages Found by conversations_history===============")
        print(len(conversation_history))
        n_msgs = len(conversation_history)
    # Summarize the messages and send the summary
    msg_sent = False
    if n_msgs > 0:
        parsed_msg = parse_messages(conversation_history, is_test)
        summary = summary_model(parsed_msg)
        msg_construct = {
        "token":BOT_TOKEN,
        "channel":channel_id,
        "text": summary
        }
        if not is_test: # From Slack, not from Tests
            #retval = web_client.chat_postMessage(**msg_construct)
            retval = web_client.chat_postMessage(channel=msg_construct["channel"], text=msg_construct["text"]) 
        else:
            print(summary) # Visual debug if Test
        msg_sent = True
    elif not is_test:
        text_msg = "No analyzable messages found at the moment. Please try again later."
        cmd_output ={"blocks": [{
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": text_msg
        }}]}
        retval = web_client.chat_postEphemeral(channel=channel_id, user=payload["user_id"], text=text_msg, blocks=cmd_output["blocks"])

    return n_msgs, msg_sent


# Allows us to set up a webpage with the script, which enables testing using tools like ngrok.
if __name__ == "__main__":
    bot_app.run(debug=True)
