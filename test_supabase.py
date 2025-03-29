from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def test_connection():
    try:
        # Try to fetch the table structure
        response = supabase.table('chat_history').select('*').limit(1).execute()
        print("✅ Successfully connected to Supabase!")
        print("✅ chat_history table exists!")
        print("\nTable structure:")
        print(response)
        return True
    except Exception as e:
        print("❌ Error connecting to Supabase:")
        print(str(e))
        return False

def create_test_record():
    try:
        # Insert a test record
        data = {
            'user_message': 'Test message',
            'bot_response': 'Test response'
        }
        response = supabase.table('chat_history').insert(data).execute()
        print("\n✅ Successfully inserted test record!")
        print("Test record:", response.data)
        return True
    except Exception as e:
        print("\n❌ Error inserting test record:")
        print(str(e))
        return False

if __name__ == "__main__":
    print("Testing Supabase connection...")
    if test_connection():
        print("\nTesting record insertion...")
        create_test_record() 