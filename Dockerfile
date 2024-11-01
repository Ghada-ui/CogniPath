# Use a base image with Python and Flask pre-installed
FROM python:3.10.8

# Set the working directory within the container
WORKDIR /app

# Copy the requirements.txt file and install dependencies
COPY requirements.txt requirements.txt

# Install system dependencies without attempting to sync time with ntpdate
RUN apt-get update && \
    apt-get install -y libasound2 libasound2-dev portaudio19-dev && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port your Flask app will run on
EXPOSE 3000

# Define the command to run your application
CMD ["python", "run.py"]
