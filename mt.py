
# import requests
# import time

# urls = [
#     "https://httpbin.org/delay/2",
#     "https://httpbin.org/delay/2",
#     "https://httpbin.org/delay/2"
# ]

# def fetch_api(url):
#     response = requests.get(url, timeout=10)
#     print("Status:", response.status_code)

# start = time.perf_counter()

# for url in urls:
#     fetch_api(url)

# print("Total:", round(time.perf_counter() - start, 2))


import requests
import time
from concurrent.futures import ThreadPoolExecutor

urls = [
    "https://httpbin.org/delay/2",
    "https://httpbin.org/delay/2",
    "https://httpbin.org/delay/2"
]

def fetch_api(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.status_code

start = time.perf_counter()

with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(fetch_api, urls))

print("Results:", results)
print("Total:", round(time.perf_counter() - start, 2))
