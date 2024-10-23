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
prompt = "a magical landscape with a castle in the sky"

vertexai.init(project=PROJECT_ID, location=LOCATION)

model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")

images = model.generate_images(
    prompt=prompt,
    # Optional parameters
    number_of_images=1,
    language="en",
    # You can't use a seed value and watermark at the same time.
    # add_watermark=False,
    # seed=100,
    aspect_ratio="1:1",
    safety_filter_level="block_some"
)

images[0].save(location=output_file, include_generation_parameters=False)

# Optional. View the generated image in a notebook.
# images[0].show()

print(f"Created output image using {len(images[0]._image_bytes)} bytes")