import os
import sys
import shutil
import tempfile
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# TOP-LEVEL APPLICATION ASSIGNMENTS FOR VERCEL AST SCANNER
app = FastAPI(
    title="RetailIQ – AI-Powered Inventory Intelligence",
    description="Intelligent Inventory Monitoring and Automated Replenishment Agent",
    version="1.0.0"
)
handler = app

# Enable CORS for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)

for p in [CURRENT_DIR, PARENT_DIR, os.path.join(CURRENT_DIR, "backend"), os.path.join(PARENT_DIR, "backend")]:
    if os.path.exists(p) and p not in sys.path:
        sys.path.insert(0, p)

# Seed database into writable /tmp for Vercel serverless environment
is_serverless = bool(os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"))
tmp_dir = "/tmp" if (os.path.exists("/tmp") and os.access("/tmp", os.W_OK)) else tempfile.gettempdir()
target_db = os.path.join(tmp_dir, "retailiq.db")

candidates = [
    os.path.join(CURRENT_DIR, "retailiq.db"),
    os.path.join(CURRENT_DIR, "data", "retailiq.db"),
    os.path.join(CURRENT_DIR, "backend", "data", "retailiq.db"),
    os.path.join(PARENT_DIR, "data", "retailiq.db"),
    os.path.join(PARENT_DIR, "backend", "data", "retailiq.db"),
]

src_db = None
for c in candidates:
    if os.path.exists(c) and os.path.getsize(c) > 100000:
        src_db = c
        break

if src_db:
    if not os.path.exists(target_db) or os.path.getsize(target_db) < 100000:
        try:
            shutil.copyfile(src_db, target_db)
            print(f"[RetailIQ Init] Seeded database from {src_db} ({os.path.getsize(src_db):,} bytes) to {target_db}")
        except Exception as e:
            print(f"[RetailIQ Init Warning] Copy to tmp failed: {e}")

if os.path.exists(target_db) and os.path.getsize(target_db) > 100000:
    os.environ["DATABASE_URL"] = f"sqlite:///{target_db}"
elif src_db:
    os.environ["DATABASE_URL"] = f"sqlite:///{src_db}"

# Register core API router on both /api and root level
try:
    try:
        from backend.app.api.endpoints import router as api_router
    except ImportError:
        from app.api.endpoints import router as api_router
        
    app.include_router(api_router, prefix="/api")
    app.include_router(api_router)
except Exception as e:
    import traceback
    err_tb = traceback.format_exc()
    print(f"[RetailIQ Router Registration Warning]: {err_tb}")
    
    @app.get("/api/health")
    @app.get("/health")
    def fallback_health():
        return {"status": "degraded", "error": str(e), "traceback": err_tb}

@app.on_event("startup")
def startup_event():
    try:
        try:
            from backend.app.models.database import engine, Base
            from sqlalchemy import inspect
        except ImportError:
            from app.models.database import engine, Base
            from sqlalchemy import inspect
            
        inspector = inspect(engine)
        if not inspector.has_table("products"):
            Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"[RetailIQ Startup] Schema note: {e}")
