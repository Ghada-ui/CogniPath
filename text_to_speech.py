from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google.cloud import aiplatform
from google.cloud import texttospeech
from dotenv import load_dotenv
import os

# aiplatform initiation
load_dotenv()
key_path = "credentials.json"
credentials = Credentials.from_service_account_file(key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"])

if credentials.expired:
    credentials.refresh(Request())
PROJECT_ID = os.getenv("GCP_PROJECT")
LOCATION =  os.getenv('GCP_REGION')   
aiplatform.init(project = PROJECT_ID,location=LOCATION, credentials=credentials)
print("project id : "+PROJECT_ID+" location : "+LOCATION)

#text to speech code with google cloud 

# Initialize the Text-to-Speech client with credentials
client = texttospeech.TextToSpeechClient(credentials=credentials)

# Input text to synthesize
text_input = texttospeech.SynthesisInput(text="Movies, oh my gosh, I just just absolutely love them. They're like time machines taking you to different worlds and landscapes, and um, and I just can't get enough of it.")

# Voice selection with higher-pitched female voice for child-like quality
voice = texttospeech.VoiceSelectionParams(
    name="en-US-Journey-F",  
    language_code="en-US",
    ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
)

# Audio configuration with adjustments for pitch and speaking rate
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3,
    pitch=0,              #  (range -20.0 to 20.0)
    speaking_rate=1.0       # speaking rate (normal is 1.0)
)

# Synthesize the speech
response = client.synthesize_speech(input=text_input, voice=voice, audio_config=audio_config)

# Save the synthesized audio to an MP3 file
with open("output.mp3", "wb") as out:
    out.write(response.audio_content)
    print("The audio has been saved as 'output.mp3'")