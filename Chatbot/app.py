from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os
import requests
import json

app = Flask(__name__)

# Configure Gemini API
# Get your API key:
# 1. Go directly to https://makersuite.google.com/app/apikey
# 2. Sign in with your Google account if needed
# 3. Click "Create API key" or "Get API key"
# 4. Accept terms and copy the key that starts with "AIza..."
GOOGLE_API_KEY = 'AIzaSyAxmdxUR7_HsWY5kes0MGUk31Aena4IREM'  # Replace with your API key from MakerSuite

try:
    # Configure the API
    genai.configure(api_key=GOOGLE_API_KEY)
    
    # List available models
    print("Available models:")
    for model in genai.list_models():
        print(model.name)
    
    # Create the model instance
    print("\nTrying to create model instance...")
    model = genai.GenerativeModel('models/gemini-1.5-pro')
    
    # Test the connection with a simple prompt
    print("\nTesting connection...")
    test_response = model.generate_content("Say hello")
    print("✓ Successfully connected to Gemini API")
    print("Test response:", test_response.text)
    
except Exception as e:
    print(f"\n❌ Detailed Error: {str(e)}")
    print("\nTo fix this:")
    print("1. Verify your API key is correct")
    print("2. Make sure the Gemini API is enabled in Google Cloud Console")
    print("3. Wait a few minutes after enabling the API")
    print("4. Check if your Google Cloud project has billing enabled")

# Add some context about your college
COLLEGE_CONTEXT = """
This is a chatbot for K.J. Somaiya Institute of Technology.
Key Information:
- Location: Mumbai, Maharashtra, India
- Programs: Computer Engineering, Information Technology, Electronics Engineering, etc.
- Contact: +91 98200 00000
- Admissions: Merit-based admissions through MHT-CET and JEE scores

Campus Life & Activities:
- Hackathons: Regular hackathon events where students work on innovative solutions to real-world problems. These 24-48 hour coding competitions help students develop problem-solving skills and creativity.
- Technical Festivals: Annual tech fest featuring coding competitions, robotics challenges, and project exhibitions
- Student Clubs: Active coding club, robotics club, and innovation cell
- Research Activities: Strong focus on emerging technologies like AI, ML, IoT, and Cybersecurity
- Industry Collaborations: Regular workshops and internship opportunities with leading tech companies

Facilities:
- Modern Computer Labs
- High-speed Internet
- Innovation Center
- Digital Library
- Sports Complex

Achievement Highlights:
- Multiple hackathon winning teams
- Research paper publications by students
- Industry-sponsored projects
- Excellent placement record
"""

def is_college_related(query):
    college_keywords = ['kjsit', 'somaiya', 'college', 'admission', 'campus', 'faculty', 'department', 
                       'course', 'program', 'fee', 'placement', 'hostel', 'library']
    return any(keyword in query.lower() for keyword in college_keywords)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    
    if not GOOGLE_API_KEY:
        return jsonify({'response': 'API key not configured. Please set up your Gemini API key.'})
    
    try:
        # Prepare the prompt based on the query type
        if is_college_related(user_message):
            prompt = f"{COLLEGE_CONTEXT}\nUser: {user_message}\nPlease provide a helpful response:"
        else:
            prompt = f"User: {user_message}\nPlease provide a helpful response:"
        
        # Generate response
        response = model.generate_content(
            prompt,
            generation_config={
                'temperature': 0.7,
                'max_output_tokens': 2048,
            }
        )
        
        if response and hasattr(response, 'text') and response.text:
            return jsonify({'response': response.text})
        else:
            print("Empty response received")
            return jsonify({'response': 'I apologize, but I received an empty response. Please try asking your question differently.'})
            
    except Exception as e:
        error_message = str(e)
        print(f"Detailed chat error: {error_message}")
        
        if "API key" in error_message.lower():
            return jsonify({'response': 'There seems to be an issue with the API key. Please ensure it is valid.'})
        elif "quota" in error_message.lower():
            return jsonify({'response': 'The API quota has been exceeded. Please try again later.'})
        elif "model" in error_message.lower():
            return jsonify({'response': 'Please make sure you have enabled the Gemini API in your Google Cloud Console.'})
        else:
            return jsonify({'response': 'I encountered an error. Please try again in a few moments.'})

if __name__ == '__main__':
    app.run(debug=True) 

