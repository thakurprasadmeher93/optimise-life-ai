import os, json
from datetime import datetime
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_KEY') or os.getenv('SUPABASE_ANON_KEY')
# This is a lightweight stub for local dev/testing.
LOCAL_STORE = os.getenv('LOCAL_CALC_STORE','/tmp/optimiselife_local_calcs.json')
def save_calculation(user_email, calc_type, input_data, result_data):
    rec = {'id':'local-'+datetime.utcnow().strftime('%Y%m%d%H%M%S'),'user_email':user_email,'calc_type':calc_type,'input':input_data,'result':result_data,'created_at':datetime.utcnow().isoformat()}
    arr = []
    try:
        if os.path.exists(LOCAL_STORE):
            with open(LOCAL_STORE,'r') as rf:
                arr = json.load(rf)
    except Exception:
        arr = []
    arr.insert(0, rec)
    try:
        with open(LOCAL_STORE,'w') as wf:
            json.dump(arr, wf)
    except Exception:
        pass
    return rec

def fetch_user_calculations(user_email, limit=50):
    try:
        if os.path.exists(LOCAL_STORE):
            with open(LOCAL_STORE,'r') as rf:
                arr = json.load(rf)
            return [a for a in arr if a.get('user_email')==user_email][:limit]
    except Exception:
        return []
    return []

def list_recent_calculations(limit=100):
    try:
        if os.path.exists(LOCAL_STORE):
            with open(LOCAL_STORE,'r') as rf:
                arr = json.load(rf)
            return arr[:limit]
    except Exception:
        return []
    return []
