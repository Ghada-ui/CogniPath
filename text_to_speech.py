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

client = texttospeech.TextToSpeechClient(credentials=credentials)

text_input = texttospeech.SynthesisInput(text="Cognipath is the best platform in the world.")

voice = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)

audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

response = client.synthesize_speech(input=text_input, voice=voice, audio_config=audio_config)

with open("output.mp3", "wb") as out:
    out.write(response.audio_content)
    print("L'audio a été sauvegardé dans 'output.mp3'")