from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ
import socket
import time

selector = DefaultSelector()
n_jobs = 0

class Future:
    def __init__(self):
        self.callback = None

    def resolve(self):
        self.callback()

class Client:
    def __init__(self, gen):
        self.gen = gen
        self.step()

    def step(self):
        try:
            f = next(self.gen)
        except StopIteration:
            return

        f.callback = self.step

def get(path):
    global n_jobs
    n_jobs += 1
    s = socket.socket()
    s.setblocking(False)
    try:
        s.connect(('www.xuetangx.com', 80))
    except BlockingIOError:
        pass

    f = Future()
    selector.register(s.fileno(), EVENT_WRITE, f)
    yield f
    selector.unregister(s.fileno())

    s.send(('GET %s HTTP/1.0\r\n\r\n' % path).encode())
    buf = []

    while True:
        f = Future()
        selector.register(s.fileno(), EVENT_READ, f)
        yield f
        selector.unregister(s.fileno())
        chunk = s.recv(1000)
        if chunk:
            buf.append(chunk)
        else:
            break

    # Finished.
    print((b''.join(buf)).decode().split('\n')[0])
    n_jobs -= 1

start = time.time()
for i in range(10):
    Client(get('http://www.xuetangx.com/courses'))

while n_jobs:
    events = selector.select()
    for key, mask in events:
        future = key.data
        future.resolve()

print('took %.2f seconds' % (time.time() - start))
