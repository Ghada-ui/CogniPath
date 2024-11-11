# Imports
import pathlib
import os
from flask import render_template, request, url_for, redirect, send_from_directory, jsonify, session ,abort, make_response
from flask_login import login_user, logout_user, current_user, login_required
from flask_socketio import SocketIO, emit
import firebase_admin
from firebase_admin import credentials, firestore, auth
from werkzeug.exceptions import HTTPException, NotFound, abort
from jinja2 import TemplateNotFound
from openai import AzureOpenAI
from app import app, lm, db, bc
from app.models import *
import requests
import numpy as np
from dotenv import load_dotenv
import base64
import azure.cognitiveservices.speech as speechsdk
import re
import time
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

from array import array
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from io import BytesIO
from flask import send_file
from azure.cognitiveservices.speech import SpeechSynthesizer
from azure.cognitiveservices.speech.audio import AudioConfig
import json
import random
import google.generativeai as genai
import time
from array import array
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from io import BytesIO
from flask import send_file
from azure.cognitiveservices.speech import SpeechSynthesizer
from azure.cognitiveservices.speech.audio import AudioConfig
import json
import random
from PIL import Image
import io
import sqlite3


from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google.cloud import aiplatform
from google.cloud import texttospeech
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
import asyncio