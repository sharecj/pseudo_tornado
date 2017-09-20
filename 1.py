import socket
import time

def get(path):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('www.xuetangx.com', 80))
    s.send(('GET %s HTTP/1.0\r\n\r\n' % path))

    buf = []
    while True:
        chunk = s.recv(1000)
        if not chunk:
            break
        buf.append(chunk)

    s.close()
    print((b''.join(buf)).split('\n')[0])

start = time.time()
for i in range(10):
    get('http://www.xuetangx.com/courses')

print('took %.2f seconds' % (time.time() - start))
