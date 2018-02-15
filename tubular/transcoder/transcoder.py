import os
import time

def transcode(conn, url='', delay=1):
    x = 0
    print(f'start transcoding {url}')
    while x < 10:
        conn.send(f'[{os.getpid()}] {x}')
        time.sleep(delay)
        x+=1
    conn.send('Done')
