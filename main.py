# FastAPI starter for Optimise Life - AI (development)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict
import uvicorn, os
from datetime import datetime
try:
    from supabase_integration import save_calculation, fetch_user_calculations, list_recent_calculations
    from backup_manager import snapshot_and_backup, list_backups, restore_backup
    from exports import generate_simple_report
except Exception:
    # local fallback stubs if modules missing
    def save_calculation(email, calc, inp, res): return {"id":"local-1","user_email":email,"calc_type":calc,"input":inp,"result":res,"created_at":datetime.utcnow().isoformat()}
    def fetch_user_calculations(email, limit=20): return []
    def list_recent_calculations(limit=50): return []
    def snapshot_and_backup(a,b=None): return None
    def list_backups(a): return []
    def restore_backup(a): return None
    def generate_simple_report(n,i,r,filename=None): return None

app = FastAPI(title="Optimise Life - AI (Dev)")

class CalcPayload(BaseModel):
    email: str
    calculator: str
    input: Dict[str, Any]
    result: Dict[str, Any]
    auto_backup: bool = False

@app.get('/')
def root():
    return {'status':'ok','app':'Optimise Life - AI (backend)'}

@app.post('/api/calc/save')
def api_save_calc(payload: CalcPayload):
    try:
        saved = save_calculation(payload.email, payload.calculator, payload.input, payload.result)
        backup_path = None
        if payload.auto_backup:
            backup_path = snapshot_and_backup(saved.get('id') or saved.get('user_id'), payload.email)
        return {'status':'ok','record':saved,'backup':backup_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/api/calc/list/{email}')
def api_list_calc(email: str, limit: int = 20):
    try:
        data = fetch_user_calculations(email, limit)
        return {'status':'ok','data':data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/api/admin/recent')
def api_admin_recent(limit: int = 50):
    try:
        data = list_recent_calculations(limit)
        return {'status':'ok','data':data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
