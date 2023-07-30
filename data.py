import re
QA_DATABASE = {
    "What is your name?": "I am the Talking Bot!",
    "How are you?": "I'm just a chatbot, but I'm here to help!",
    "What can you do?": "I can answer questions, have conversations, and more!",
}

# Custom patterns for weather and time-related questions
WEATHER_PATTERNS = [r"weather", r"(temperature|rain|sunny|cloudy)"]
TIME_PATTERNS = [r"time", r"(clock|hour|minute)"]
count={
    "counter":0
}