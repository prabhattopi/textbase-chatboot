import textbase
from textbase.message import Message
from textbase import models
import os
from typing import List
import re
from data import QA_DATABASE, WEATHER_PATTERNS, TIME_PATTERNS, count
# Regular expression patterns to match specific user inputs
# Add more patterns as needed
HELLO_PATTERNS = [r"(hi|hello|hey)"]
GOODBYE_PATTERNS = [r"bye", r"goodbye", r"see you"]
QUESTION_PATTERNS = [r"(what|where|when|why|how)"]
# Load your OpenAI API key
# models.OpenAI.api_key = ""
# or from environment variable:
models.OpenAI.api_key = os.getenv("OPENAI_API_KEY")




# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are chatting with an AI. There are no specific prefixes for responses, so you can ask or talk about anything you like. The AI will respond in a natural, conversational manner. Feel free to start the conversation with any question or topic, and let's have a pleasant chat!
"""

# Keep track of previous user messages for context
previous_messages = []


@textbase.chatbot("talking-bot")
def on_message(message_history: List[Message], state: dict = None):
    """Your chatbot logic here
    message_history: List of user messages
    state: A dictionary to store any stateful information

    Return a string with the bot_response or a tuple of (bot_response: str, new_state: dict)
    """

    if state is None or "counter" not in state:
        state = {"counter": 0}
    else:
        state["counter"] += 1

    # Extract the user's latest message text
    user_message = message_history[-1].content

    # Process the user's message
    processed_message = preprocess_user_message(user_message)
    # Check if the user's message is a repeat
   
    # Check if the user's message matches any pre-defined question-answer pairs
    if processed_message in QA_DATABASE:
            count["counter"]+=1
            if count["counter"]>=3:
                   bot_response = "It looks like you already asked that. Is there anything else you'd like to know?"
                   return bot_response, state  # Return the response without generating a new one

            bot_response = QA_DATABASE[processed_message]
    else:
            count["counter"]=0
            # Check for specific user inputs using regular expressions
            if any(re.search(pattern, processed_message, re.IGNORECASE) for pattern in HELLO_PATTERNS):
                bot_response = "Hello there! How can I assist you today?"

            elif any(re.search(pattern, processed_message, re.IGNORECASE) for pattern in GOODBYE_PATTERNS):
                bot_response = "Goodbye! Have a great day!"

            elif any(re.search(pattern, processed_message, re.IGNORECASE) for pattern in QUESTION_PATTERNS):
                # Handle generic questions
                bot_response = "That's an interesting question! Let me think..."
                # Generate GPT-3.5 Turbo response with the updated system prompt
                bot_response = models.OpenAI.generate(
                    system_prompt=bot_response,
                    message_history=message_history,
                    model="gpt-3.5-turbo",
                )

            else:
                # If no specific pattern matched, use the default GPT-3.5 Turbo response
                bot_response = models.OpenAI.generate(
                    system_prompt=SYSTEM_PROMPT,
                    message_history=message_history,
                    model="gpt-3.5-turbo",
                )

            # Save the new question and its answer to the QA_DATABASE
            QA_DATABASE[processed_message] = bot_response

    # Post-process the bot's response (optional)
    processed_bot_response = postprocess_bot_response(bot_response)

    return processed_bot_response, state


def preprocess_user_message(user_message):
    """Process the user's message before applying logic"""
    # Convert the user's message to lowercase
    processed_message = user_message.lower()

    # Replace specific words with placeholders to remove sensitive information
    sensitive_info = {
        "password": "******",
        "credit card": "**** ****",
    }

    for word, replacement in sensitive_info.items():
        processed_message = processed_message.replace(word, replacement)

    return processed_message


def postprocess_bot_response(bot_response):
    """Post-process the bot's response before returning it"""
    return bot_response
