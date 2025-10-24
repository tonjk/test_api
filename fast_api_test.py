import httpx
import asyncio
import time

async def send_request(client: httpx.AsyncClient, url: str) -> None:
    start_time = time.time()
    response = await client.get(url, timeout=6)
    end_time = time. time ()
    print(f"Response: {response.json()}, Time Taken: {end_time - start_time:.2f} seconds")

async def main():
    url = "http://127.0.0.1:8080/ping"
    async with httpx.AsyncClient() as client:
        tasks = [send_request(client, url) for _ in range(10)]
        start_time = time.time()
        await asyncio.gather(*tasks)
        end_time = time.time()
    print (f"\nTotal Time Taken for 10 Requests: {end_time - start_time: 2f} seconds")

if __name__== "__main__":
    asyncio.run(main())