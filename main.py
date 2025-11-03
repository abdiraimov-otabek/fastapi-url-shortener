from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import URL
from utils import generate_short_code

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="URL Shortener",
    description="A simple URL shortener service",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "URL Shortener",
            "description": "Operations related to URL shortening and redirection",
        }
    ],
)


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


# Create short URL
@app.post("/shorten/", tags=["URL Shortener"])
def create_short_url(url: URLCreate, db: Session = Depends(get_db)):
    code = generate_short_code()
    db_url = URL(original_url=url.original_url, short_code=code)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return {"short_url": f"http://localhost:8000/{code}"}


# Redirect
@app.get("/{code}", tags=["URL Shortener"])
def redirect_url(code: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.short_code == code).first()
    if url:
        url.clicks += 1
        db.commit()
        return RedirectResponse(url.original_url)
    raise HTTPException(status_code=404, detail="URL not found")


# Optional: List all URLs (for testing)
@app.get("/urls/", tags=["URL Shortener"])
def list_urls(db: Session = Depends(get_db)):
    urls = db.query(URL).all()
    return [
        {"original": u.original_url, "short": u.short_code, "clicks": u.clicks}
        for u in urls
    ]
