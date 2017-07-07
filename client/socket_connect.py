import socket
import time
import os

import urllib
import urllib.request


def invoke_sock(q):
    time.sleep(1)
    url = "http://www.jdmy.me/danmu_get"
    while True:
        data = urllib.request.urlopen(url).read()
        if data != b'no':
            print(data.decode('utf-8'))
            q.put(data.decode('utf-8'))
        time.sleep(3)
