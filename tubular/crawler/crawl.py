import asyncio
import time
import requests
import config

async def fetch(url):
    try:
        response = requests.get(url, timeout=5)
    except Exception:
        return None

    return {'url': url, 'response': response}

async def fetch_urls(loop, manifest):
    tasks = [loop.create_task(fetch(url)) for url in manifest]
    await asyncio.wait(tasks)
    return [task.result() for task in tasks]

def get(manifest):
    loop = asyncio.get_event_loop()
    responses = loop.run_until_complete(fetch_urls(loop, manifest))
    loop.close()
    return responses

def post_responses(url, responses):
    requests.post(url, data={'responses': responses})
    return

if __name__ == '__main__':
    start = time.time()
    app_config = config.load()
    responses = get(app_config['crawler']['manifest'])
    post_responses(app_config['data_store']['ip'], responses)
    end = time.time()
    print(f'total time {end - start}')
