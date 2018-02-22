import asyncio
import time
import requests
import config

async def fetch(url):
    try:
        response = requests.get(url, timeout=5)
    except Exception:
        return None
    
    return response

async def fetch_urls(loop, manifest):
    tasks = [loop.create_task(fetch(url)) for url in manifest]
    await asyncio.wait(tasks)
    return [task.result() for task in tasks]
        

def get(manifest):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_urls(loop, manifest))
    loop.close()

if __name__ == '__main__':
    start = time.time()
    manifest = [
        'http://paulrguerra.com',
        'http://google.com',
        'http://duckduckgo.com'
    ]
    app_config = config.load()
    get(app_config['crawler']['manifest'])
    end = time.time()
    print(f'total time {end - start}')