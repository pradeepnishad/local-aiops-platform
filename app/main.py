from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import os

from .database import Base, engine, SessionLocal
from .models import Metric
from .data_generator import generate_metric
from .ml_engine import run_anomaly_detection
import threading
import time
from fastapi import Query
import math


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="aiops-secret")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "../templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "../static")), name="static")

# -------------------------
# DEMO CREDENTIALS
# -------------------------
USERNAME = "admin"
PASSWORD = "admin123"

def metric_scheduler():
    """
    Runs in background and inserts a new metric every 60 seconds
    """
    while True:
        time.sleep(60)  # 1 minute
        db = SessionLocal()
        db.add(generate_metric())
        db.commit()
        db.close()
        print("✅ New metric added")




# -------------------------
# STARTUP DATA
# -------------------------
@app.on_event("startup")
def startup_tasks():
    db = SessionLocal()

    # Initial seed (only once)
    if db.query(Metric).count() < 50:
        for _ in range(50):
            db.add(generate_metric())
        db.commit()

    db.close()

    # Start background scheduler
    thread = threading.Thread(
        target=metric_scheduler,
        daemon=True
    )
    thread.start()


# -------------------------
# LOGIN
# -------------------------
@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == USERNAME and password == PASSWORD:
        request.session["user"] = username
        return RedirectResponse("/", status_code=302)
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": "Invalid credentials"}
    )

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=302)

# -------------------------
# AUTH CHECK
# -------------------------
def require_login(request: Request):
    if "user" not in request.session:
        return RedirectResponse("/login", status_code=302)

# -------------------------
# DASHBOARD
# -------------------------
@app.get("/")
def dashboard(
    request: Request,
    view: str = Query(default="all"),
    page: int = Query(default=1, ge=1),
    page_size: int = 10
):
    auth = require_login(request)
    if auth:
        return auth

    db = SessionLocal()

    # Global counts
    total_count = db.query(Metric).count()
    anomalies = db.query(Metric).filter(Metric.anomaly == -1).count()

    # Base query (filterable)
    base_query = db.query(Metric)
    if view == "anomalies":
        base_query = base_query.filter(Metric.anomaly == -1)

    filtered_count = base_query.count()
    total_pages = math.ceil(filtered_count / page_size)

    # Pagination
    metrics = (
        base_query
        .order_by(Metric.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    db.close()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "metrics": metrics,
            "total_count": total_count,
            "anomalies": anomalies,
            "view": view,
            "page": page,
            "total_pages": total_pages,
            "page_size": page_size
        }
    )


# -------------------------
# ML DETECTION
# -------------------------
@app.get("/detect")
def detect(request: Request):
    auth = require_login(request)
    if auth:
        return auth

    db = SessionLocal()
    metrics = db.query(Metric).all()

    preds, severity = run_anomaly_detection(metrics)
    for i, m in enumerate(metrics):
        m.anomaly = int(preds[i])
        m.score = float(severity[i])

    db.commit()
    db.close()

    return RedirectResponse("/", status_code=302)
