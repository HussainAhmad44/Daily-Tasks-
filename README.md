# Python Concurrency Lab

A small FastAPI + HTML application comparing sequential, asyncio and multithreaded HTTP requests to JSONPlaceholder.

## Run

```powershell
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Open http://127.0.0.1:8000

The app simulates a 1-second I/O wait per request to illustrate timing. The upstream API requires internet access.
