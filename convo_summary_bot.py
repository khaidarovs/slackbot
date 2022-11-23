# Import utils
from iter2_activity_mood_convo_utils import *

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
    return summary

# Helper function that parses a list of set objects (the output from 
# payload.get('dummy_messages')) to return a single string with all the messages 
def parse_messages(messages):
    output_string = ''
    for i in range(len(messages)):
        string = str(messages[i])
        new_str = re.sub("{'", '', string)
        final_str = re.sub("'}", ' ', new_str)
        final_str1 = re.sub('{"', '', final_str)
        final_str2 = re.sub('"}', ' ', final_str1)
        output_string += final_str2
    return output_string

# Main function that calls the above two helper functions
def summarize_conversation(self):
    # Get dataa
    payload = self.payload

    # First check if this is a test or not
    is_test = False
    if payload.get('token') == "test_token_1":
        is_test = True
    channel_id = payload.get('channel_id')
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
        retval = web_client.conversations_history(**history_query)
        conversation_history = retval["messages"]
        n_msgs = len(conversation_history)
    # Summarize the messages and send the summary
    if n_msgs > 0:
        parsed_msg = parse_messages(conversation_history)
        summary = summary_model(parsed_msg)
        msg_construct = {
        "token":BOT_TOKEN,
        "channel":channel_id,
        "text": summary
        }
        if not is_test: # From Slack, not from Tests
            retval = web_client.chat_postMessage(**msg_construct) 
        else:
            print(summary) # Visual debug if Test
        msg_sent = True

    return n_msgs, msg_sent


# Allows us to set up a webpage with the script, which enables testing using tools like ngrok.
if __name__ == "__main__":
    bot_app.run(debug=True)
