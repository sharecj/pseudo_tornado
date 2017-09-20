from selectors import DefaultSelector
from framework import Client, Application, Future

selector = DefaultSelector()

def view(future):
    client = Client(selector)
    url = 'http://www.xuetangx.com/courses'

    body = yield client.get(url, future)
    print('first request done')
    #print(body)

    yield client.get(url, future)
    print('second request done')

    yield client.get(url, future)
    print('third request done')

future = Future()
gen = view(future)
future.gen = gen

next(gen)

app = Application(selector)
app.ioloop()

