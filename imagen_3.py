from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google.cloud import aiplatform
from dotenv import load_dotenv
import os
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel

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

output_file = "my-output.png"
prompt = "man holding a child in the air"

vertexai.init(project=PROJECT_ID, location=LOCATION)

model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")

try:
    images = model.generate_images(
        prompt=prompt,
        number_of_images=1,
        language="en",
        aspect_ratio="1:1",
        safety_filter_level="block_some"
    )
    
    # Check if images were returned
    if images:
        print("Image generated successfully.")
        images[0].save(location=output_file, include_generation_parameters=False)
        print(f"Created output image using {len(images[0]._image_bytes)} bytes")
    else:
        print("No images returned from the model.")
        
except Exception as e:
    print(f"An error occurred: {e}")
