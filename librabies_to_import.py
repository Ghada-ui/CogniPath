import google.generativeai as genai
import os 
import time 
import json
from dotenv import load_dotenv
import random

load_dotenv()

# gemini init
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
model_emotions = genai.GenerativeModel('gemini-1.5-flash', generation_config={"response_mime_type": "application/json"})
