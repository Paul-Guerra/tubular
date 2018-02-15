import asyncio
import random
import time
import requests

async def fetch(url):
    try:
        response = requests.get(url, timeout=5)
    except Exception:
        return None
    
    return response

async def crawl(loop, manifest):
    tasks = [loop.create_task(fetch(url)) for url in manifest]
    await asyncio.wait(tasks)
    return [task.result() for task in tasks]
        

def main(manifest):
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(crawl(loop, manifest))
    loop.close()

if __name__ == '__main__':
    start = time.time()
    manifest = [
        'http://paulrguerra.com',
        'http://google.com',
        'http://duckduckgo.com'
    ]
    main(manifest)
    end = time.time()
    print(f'total time {end - start}')