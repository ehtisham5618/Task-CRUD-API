"""Supabase authentication client initialization module."""
import os
from supabase import create_client


_supabase_client = None


def get_supabase_client():
    """Initialize and return Supabase client."""
    global _supabase_client
    
    if _supabase_client is not None:
        return _supabase_client
    
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")
    
    if not supabase_url:
        raise ValueError("SUPABASE_URL environment variable not set")
    if not supabase_key:
        raise ValueError("SUPABASE_KEY environment variable not set")
    
    try:
        _supabase_client = create_client(supabase_url, supabase_key)
    except Exception as e:
        # Log the error for debugging purposes
        error_msg = f"Failed to initialize Supabase client: {str(e)}"
        print(f"WARNING: {error_msg}")
        raise RuntimeError(error_msg)
    
    return _supabase_client

