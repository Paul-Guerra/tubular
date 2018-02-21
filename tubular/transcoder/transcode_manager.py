'''Responsible for coordinating transcode child processes'''
import os
from multiprocessing import Process, Pipe
from http.server import HTTPServer, BaseHTTPRequestHandler
from .transcoder import transcode

workers = []

def is_available():
    '''Returns Boolean if the node can handle additional jobs'''
    if is_connected() and capacity(workers) > 0:
        pass

def is_connected():
    '''Reports if this node has the needed network access to complete the job'''
    return True

def capacity(workers):
    '''Reports capacity to take on more work.'''
    cores = os.cpu_count() or 1
    return cores - len(workers)

def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    # https://gist.github.com/bradmontgomery/2219997
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == '__main__':
    p_conn, c_conn  = Pipe()
    t = Process(target=transcode, args=(c_conn, 'some URL'))
    t.start()

    t2 = Process(target=transcode, args=(c_conn, 'foobar', 3))
    t2.start()
    working = True
    while working:
        if p_conn.poll():
            response = p_conn.recv()
            if response == 'Done':
                working = False
            print(response)
    print('All done!')
