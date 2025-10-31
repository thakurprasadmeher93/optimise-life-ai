import os, json
from datetime import datetime
from pathlib import Path
BACKUP_DIR = Path(os.getenv('BACKUP_DIR','/tmp/optimiselife_backups'))
BACKUP_DIR.mkdir(parents=True, exist_ok=True)
def create_backup(user_id, data):
    ts = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    fn = f'backup_{user_id}_{ts}.json'
    p = BACKUP_DIR / fn
    with open(p,'w') as f:
        json.dump(data, f)
    return str(p)
def snapshot_and_backup(user_id, email=None):
    # read local store and make a bundle
    path = os.getenv('LOCAL_CALC_STORE','/tmp/optimiselife_local_calcs.json')
    arr = []
    try:
        if os.path.exists(path):
            with open(path,'r') as rf:
                arr = json.load(rf)
    except Exception:
        arr = []
    payload = {'user_email': email, 'calculations': arr}
    return create_backup(user_id, payload)
def list_backups(user_id):
    files = sorted(BACKUP_DIR.glob(f'backup_{user_id}_*.json'), reverse=True)
    return [str(p) for p in files]
def restore_backup(path):
    with open(path,'r') as f:
        return json.load(f)
