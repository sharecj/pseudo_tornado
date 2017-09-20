from tornado import gen
import tornado.ioloop
from tornado.httpclient import AsyncHTTPClient

@gen.coroutine
def view():
    url = 'http://www.xuetangx.com/courses'

    client = AsyncHTTPClient()
    response = yield client.fetch(url)
    print('first request done')

    client = AsyncHTTPClient()
    response = yield client.fetch(url)
    print('second request done')

view()
view()

tornado.ioloop.IOLoop.current().start()

