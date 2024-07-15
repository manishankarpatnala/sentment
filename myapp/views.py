import os
import logging
from django.shortcuts import render
from django.http import HttpResponse
from .sentiment_model import analyze_sentiment as sentiment_analysis
from pymongo import MongoClient

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MongoDB client
client = MongoClient('mongodb://localhost:27017/')
db = client['project']
collection = db['users']

# Directory where model files are stored
MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')
logger.info(f"Model directory: {MODEL_DIR}")

def output(request):
    return render(request, 'output.html')

def login(request):
    return render(request, 'login.html')

def signin(request):
    return render(request, 'signin.html')

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        reenter_password = request.POST.get('reenter_password')

        if password != reenter_password:
            return HttpResponse("Passwords do not match")

        if collection.find_one({'email': email}):
            return HttpResponse("Email already exists")

        user_data = {
            'email': email,
            'password': password,
        }
        try:
            collection.insert_one(user_data)
            return HttpResponse("Signup successful")
        except Exception as e:
            return HttpResponse(f"Signup failed: {e}")
    else:
        return HttpResponse("Method not allowed")

def postlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = collection.find_one({'email': email, 'password': password})
        if user:
            return render(request, 'output.html')
        else:
            return HttpResponse("Invalid email or password")
    else:
        return render(request, 'login.html')

from django.shortcuts import render
from django.http import HttpResponse
from .sentiment_model import analyze_sentiment
import logging

# Initialize logger
logger = logging.getLogger(__name__)

def analyze_sentiment_view(request):
    if request.method == 'POST':
        logger.info(f"Received POST data: {request.POST}")
        text = request.POST.get('review')
        print(text)
        logger.info(f"Received text: {text}")
        
        if text:
            sentiment = analyze_sentiment(text)
            return render(request, 'index.html', {'text': text, 'sentiment': sentiment})
        else:
            logger.error("Error: Text data not provided")
            return HttpResponse("Error: Text data not provided")
    else:
        return render(request, 'index.html')
