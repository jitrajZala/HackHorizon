from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

# Configure Gemini API
GOOGLE_API_KEY = 'AIzaSyAde8BbfKexV-2O-NiGn6he10Da7qWqhRk'  # Get this from Google AI Studio
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

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
    
    try:
        if is_college_related(user_message):
            # Use college context for college-related queries
            prompt = f"{COLLEGE_CONTEXT}\nUser: {user_message}\nPlease provide a helpful response:"
        else:
            # For general knowledge queries
            prompt = f"""You are a helpful AI assistant. Please answer the following question using your general knowledge.
            If the question requires very recent information, please mention that the information might not be up to date.
            
            User: {user_message}
            Please provide a helpful response:"""
        
        response = model.generate_content(prompt)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'response': f"I apologize, but I'm having trouble responding right now. Please try again later."})

if __name__ == '__main__':
    app.run(debug=True) 