# HackHorizon Project

A web application with a chatbot and user management system.

## Project Structure
- `PBL/` - Frontend files (HTML, CSS, JS)
- `Chatbot/` - Flask chatbot application with Supabase integration
- `core/` - Django main application
- `hackhorizon/` - Django project settings

## Features
- AI Chatbot using Google's Gemini AI
- User authentication and profiles
- All data stored in Supabase (users, chat history, profiles)
- Responsive web interface

## Prerequisites
- Python 3.x
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd HackHorizon
```

2. Install required packages:
```bash
pip install -r requirements.txt
pip install Pillow  # Required for handling profile pictures and image uploads
```

3. Create a `.env` file in the root directory with:
```
# Django Settings
DEBUG=True
SECRET_KEY=django-insecure-#b4f-woj*(g+y@53qa%58fc_s$vo_r7yg&pp5y4w6rp^9_7m7%

# Supabase Configuration
SUPABASE_URL=https://oahjuioqrywxbdiqfwzb.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9haGp1aW9xcnl3eGJkaXFmd3piIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDMyMjc3MDgsImV4cCI6MjA1ODgwMzcwOH0.AbXKSajKDViAmn9GjUN9rGhNtS99wr4NzaNFL_CPWYw

# Google API Key
GOOGLE_API_KEY=AIzaSyAxmdxUR7_HsWY5kes0MGUk31Aena4IREM
```

## Running the Project

1. Start the Django development server:
```bash
python manage.py runserver
```
The server will run at http://127.0.0.1:8000/

2. Start the Flask chatbot (in a separate terminal):
```bash
python Chatbot/app.py
```

## Database Information
- All data (users, chat history, profiles) is stored in Supabase
- Supabase provides:
  - User authentication
  - Real-time database
  - File storage (for profile pictures)
  - Row Level Security (RLS) for data protection

## Required Packages Explanation
- `supabase`: For connecting to Supabase database
- `Pillow`: Required for handling profile pictures and image uploads in Django
- `flask`: For the chatbot web server
- `google-generativeai`: For the AI chatbot functionality
- `python-dotenv`: For managing environment variables
- `Django`: For the main web application
- `djangorestframework`: For API endpoints
- `django-cors-headers`: For handling cross-origin requests

## Important Notes
- All data is stored in Supabase for consistency and real-time features
- Make sure to keep your API keys secure
- The Django secret key should be changed in production
- Profile pictures are stored in Supabase storage

## Troubleshooting
If you encounter any issues:
1. Make sure all required packages are installed
2. Check if the `.env` file is properly configured
3. Ensure both Django and Flask servers are running
4. Check the console for any error messages
5. If you get image-related errors, make sure Pillow is installed 