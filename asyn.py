
import asyncio
import httpx
import time

async def get_user(client, user_id):
    url = f"https://jsonplaceholder.typicode.com/users/{user_id}"

    try:
        print(f"Fetching user {user_id}...")

        response = await client.get(url)
        response.raise_for_status()git 

        user = response.json()

        print(f"User {user_id}: {user['name']}")
        return user

    except httpx.HTTPError as error:
        print(f"Error fetching user {user_id}: {error}")
        return None


async def main():
    start = time.perf_counter()

    async with httpx.AsyncClient(timeout=10.0) as client:
        results = await asyncio.gather(
            get_user(client, 1),
            get_user(client, 2),
            get_user(client, 3),
            get_user(client, 4),
            get_user(client, 5)
        )

    successful = [user for user in results if user is not None]

    print(f"\nSuccessfully fetched: {len(successful)} users")
    print(f"Total time: {time.perf_counter() - start:.2f} seconds")


asyncio.run(main())
