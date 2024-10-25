from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google.cloud import aiplatform
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
