from typing import Optional
from backend.config import settings

def get_supabase_client():
    """
    Initializes and returns the Supabase client using credentials from .env.
    """
    if not settings.SUPABASE_URL or not (settings.SUPABASE_SERVICE_ROLE_KEY or settings.SUPABASE_ANON_KEY):
        raise ValueError(
            "Supabase credentials missing. Please set SUPABASE_URL and SUPABASE_ANON_KEY / SUPABASE_SERVICE_ROLE_KEY in .env"
        )
    
    try:
        from supabase import create_client, Client
        key = settings.SUPABASE_SERVICE_ROLE_KEY or settings.SUPABASE_ANON_KEY
        client: Client = create_client(settings.SUPABASE_URL, key)
        return client
    except ImportError:
        raise ImportError(
            "The 'supabase' Python package is not installed. Run 'pip install supabase' to enable Supabase integration."
        )
