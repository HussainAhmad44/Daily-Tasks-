import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

app = FastAPI(title="Python Concurrency Demo")
BASE_URL = "https://jsonplaceholder.typicode.com/users"
USER_IDS = range(1, 6)
DEMO_DELAY = 1  # Simulated I/O wait to make timing differences visible.


def get_user_sync(user_id: int) -> dict:
    time.sleep(DEMO_DELAY)
    with httpx.Client(timeout=15) as client:
        response = client.get(f"{BASE_URL}/{user_id}")
        response.raise_for_status()
        return response.json()


async def get_user_async(client: httpx.AsyncClient, user_id: int) -> dict:
    await asyncio.sleep(DEMO_DELAY)
    response = await client.get(f"{BASE_URL}/{user_id}")
    response.raise_for_status()
    return response.json()


@app.get("/")
def home():
    return FileResponse(Path(__file__).with_name("index.html"))


@app.get("/api/{mode}")
async def compare(mode: str):
    if mode not in {"sequential", "async", "threads"}:
        raise HTTPException(status_code=404, detail="Unknown mode")

    start = time.perf_counter()
    try:
        if mode == "sequential":
            # Run blocking work in a worker so the FastAPI event loop isn't blocked.
            def sequential_fetch():
                return [get_user_sync(user_id) for user_id in USER_IDS]
            users = await asyncio.to_thread(sequential_fetch)
        elif mode == "async":
            async with httpx.AsyncClient(timeout=15) as client:
                users = await asyncio.gather(
                    *(get_user_async(client, user_id) for user_id in USER_IDS)
                )
        else:
            # ThreadPoolExecutor uses threads for blocking HTTP calls.
            def threaded_fetch():
                with ThreadPoolExecutor(max_workers=5) as pool:
                    return list(pool.map(get_user_sync, USER_IDS))
            users = await asyncio.to_thread(threaded_fetch)
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Upstream API request failed: {type(exc).__name__}") from exc

    return {
        "mode": mode,
        "seconds": round(time.perf_counter() - start, 3),
        "users": [{"id": u["id"], "name": u["name"], "email": u["email"]} for u in users],
    }
