# This file helps our robot remember important things
from dotenv import load_dotenv
import os

# Load our secret information
load_dotenv()

# Get our secret information ready to use
MONGODB_URI = os.getenv('mongodburl')
TWITTER_USERNAME = os.getenv('__')
TWITTER_PASSWORD = os.getenv('__')
PROXYMESH_USERNAME = os.getenv('__')
PROXYMESH_PASSWORD = os.getenv('__')