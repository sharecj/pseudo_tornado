from selectors import DefaultSelector
from framework import Client, Application, Future
from functools import wraps

selector = DefaultSelector()

def coroutine(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        future = Future()
        gen = func()
        future.gen = gen

        gen.send(future)

    return wrapper

@coroutine
def view():
    future = yield

    client = Client(selector)
    url = 'http://www.xuetangx.com/courses'

    body = yield client.get(url, future)
    print('first request done')
    print(body)

    yield client.get(url, future)
    print('second request done')

    yield client.get(url, future)
    print('third request done')

view()

app = Application(selector)
app.ioloop()

