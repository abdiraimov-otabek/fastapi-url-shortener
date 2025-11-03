

# FastAPI URL Shortener

A simple URL shortener built with **FastAPI** and **SQLite**.
Shorten long URLs and redirect users to the original URL. Includes click tracking.

---

## **Features**

* Create short URLs
* Redirect short URLs to the original URL
* Track number of clicks per short URL
* Easy to extend and deploy

---

## **Tech Stack**

* FastAPI
* SQLAlchemy (ORM)
* SQLite (database)
* **UV** (server with pyproject.toml)

---

## **Project Structure**

```
url_shortener/
├─ main.py         # FastAPI app with endpoints
├─ models.py       # SQLAlchemy models
├─ database.py     # Database setup
├─ utils.py        # Helper functions (short code generator)
├─ pyproject.toml  # UV project config & dependencies
```

---

## **Installation**

1. Clone the repo:

```bash
git clone <repo-url>
cd url_shortener
```

2. Ensure you have Python ≥ 3.11 installed.

3. Install dependencies via **UV** (using `pyproject.toml`):

```bash
uv install
```

4. Run the server:

```bash
uv run main:app --reload
```

Server will run at `http://localhost:8000`

---

## **API Endpoints**

### **Create Short URL**

```
POST /shorten/
Content-Type: application/json
Body:
{
  "original_url": "https://example.com"
}
Response:
{
  "short_url": "http://localhost:8000/a1b2C3"
}
```

### **Redirect Short URL**

```
GET /{short_code}
Example: http://localhost:8000/a1b2C3
Redirects to the original URL.
```

### **List All URLs (Optional)**

```
GET /urls/
Response:
[
  {
    "original": "https://example.com",
    "short": "a1b2C3",
    "clicks": 5
  }
]
```

---

## **Future Improvements**

* Custom short codes
* Expiration dates for URLs
* Frontend dashboard for analytics
* User authentication & personal links

---

