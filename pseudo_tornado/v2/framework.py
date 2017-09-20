import time
import socket
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ

class Future:
    def __init__(self):
        self.callback = None

    def resolve(self):
        self.callback()

class Client:
    def __init__(self, selector):
        self.selector = selector

    def _get(self, url):
        s = socket.socket()
        s.setblocking(False)
        try:
            s.connect(('www.xuetangx.com', 80))
        except BlockingIOError:
            pass

        f = Future()
        self.selector.register(s.fileno(), EVENT_WRITE, f)
        yield f
        self.selector.unregister(s.fileno())

        s.send(('GET %s HTTP/1.0\r\n\r\n' % url).encode())
        buf = []

        while True:
            f = Future()
            self.selector.register(s.fileno(), EVENT_READ, f)
            yield f
            self.selector.unregister(s.fileno())
            chunk = s.recv(1000)
            if chunk:
                buf.append(chunk)
            else:
                raise StopIteration(buf)

    def step(self):
        try:
            f = next(self.gen)
        except StopIteration as e:
            try:
                self.caller_future.gen.send(e)
            except:
                return e
        else:
            f.callback = self.step

    def get(self, url, future):
        self.gen = self._get(url)
        self.caller_future = future
        self.step()

class Application:

    def __init__(self, selector):
        self.selector = selector

    def ioloop(self):
        while True:
            events = self.selector.select()
            for key, mask in events:
                future = key.data
                future.resolve()

