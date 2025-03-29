from supabase import create_client
import os
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()

@lru_cache(maxsize=1)
def get_supabase_client():
    """Get a cached Supabase client instance."""
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_KEY')
    if not url or not key:
        raise ValueError("Supabase URL and KEY must be set in environment variables")
    return create_client(url, key)

# Example functions for database operations
def execute_sql(query, params=None):
    """Execute a raw SQL query."""
    client = get_supabase_client()
    try:
        result = client.rpc('execute_sql', {'query': query, 'params': params}).execute()
        return result.data
    except Exception as e:
        print(f"Error executing SQL: {e}")
        return None

def get_table_data(table_name):
    """Get all data from a table."""
    client = get_supabase_client()
    try:
        result = client.table(table_name).select("*").execute()
        return result.data
    except Exception as e:
        print(f"Error fetching table data: {e}")
        return None

def insert_data(table_name, data):
    """Insert data into a table."""
    client = get_supabase_client()
    try:
        result = client.table(table_name).insert(data).execute()
        return result.data
    except Exception as e:
        print(f"Error inserting data: {e}")
        return None

def update_data(table_name, data, match_criteria):
    """Update data in a table."""
    client = get_supabase_client()
    try:
        result = client.table(table_name).update(data).match(match_criteria).execute()
        return result.data
    except Exception as e:
        print(f"Error updating data: {e}")
        return None

def delete_data(table_name, match_criteria):
    """Delete data from a table."""
    client = get_supabase_client()
    try:
        result = client.table(table_name).delete().match(match_criteria).execute()
        return result.data
    except Exception as e:
        print(f"Error deleting data: {e}")
        return None 