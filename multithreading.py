
import threading
import time

def process_order(order_id):
    print(f"Processing Order {order_id}")
    time.sleep(3)
    print(f"Order {order_id} completed")

start = time.perf_counter()

threads = []

for i in range(1, 5):
    t = threading.Thread(
        target=process_order,
        args=(i,)
    )

    threads.append(t)
    t.start()

for t in threads:
    t.join()

end = time.perf_counter()

print(f"Total time: {end - start:.2f} seconds")
