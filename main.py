import textbase
from textbase.message import Message
from textbase import models
import os
from typing import List

import re

# Regular expression patterns to match specific user inputs
# Add more patterns as needed
HELLO_PATTERNS = [r"(hi|hello|hey)"]
GOODBYE_PATTERNS = [r"bye", r"goodbye", r"see you"]
QUESTION_PATTERNS = [r"(what|where|when|why|how)"]

# Custom patterns for weather and time-related questions
WEATHER_PATTERNS = [r"weather", r"(temperature|rain|sunny|cloudy)"]
TIME_PATTERNS = [r"time", r"(clock|hour|minute)"]
# Load your OpenAI API key
models.OpenAI.api_key = ""
# or from environment variable:
models.OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are chatting with an AI. There are no specific prefixes for responses, so you can ask or talk about anything you like. The AI will respond in a natural, conversational manner. Feel free to start the conversation with any question or topic, and let's have a pleasant chat!
"""


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

    elif any(re.search(pattern, processed_message, re.IGNORECASE) for pattern in WEATHER_PATTERNS):
        # Handle weather-related questions
        bot_response = "The weather is nice today! It's sunny with a temperature of 25°C."

    elif any(re.search(pattern, processed_message, re.IGNORECASE) for pattern in TIME_PATTERNS):
        # Handle time-related questions
        bot_response = "The current time is 2:30 PM."

    else:
        # If no specific pattern matched, use the default GPT-3.5 Turbo response
        bot_response = models.OpenAI.generate(
            system_prompt=SYSTEM_PROMPT,
            message_history=message_history,
            model="gpt-3.5-turbo",
        )

    # Post-process the bot's response (optional)
    processed_bot_response = postprocess_bot_response(bot_response)

    return processed_bot_response, state


def preprocess_user_message(user_message):
    """Process the user's message before applying logic"""
    # Add any pre-processing steps as needed (e.g., removing sensitive information)
    return user_message


def postprocess_bot_response(bot_response):
    """Post-process the bot's response before returning it"""
    # Add any post-processing steps as needed (e.g., formatting the response)
    return bot_response
