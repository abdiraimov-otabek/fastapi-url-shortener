from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine, Base
from models import URL
from utils import generate_short_code

Base.metadata.create_all(bind=engine)
app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Pydantic model
class URLCreate(BaseModel):
    original_url: str


# Frontend page
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/dashboard/")
def dashboard(request: Request, db: Session = Depends(get_db)):
    urls = db.query(URL).all()
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "urls": urls}
    )


# Create short URL
@app.post("/shorten/")
def create_short_url(url: URLCreate, db: Session = Depends(get_db)):
    code = generate_short_code()
    db_url = URL(original_url=url.original_url, short_code=code)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return {"short_url": f"http://localhost:8000/{code}"}


# Redirect short URL
@app.get("/{code}")
def redirect_url(code: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.short_code == code).first()
    if url:
        url.clicks += 1
        db.commit()
        return RedirectResponse(url.original_url)
    raise HTTPException(status_code=404, detail="URL not found")
