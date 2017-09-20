from selectors import DefaultSelector
from framework import Client, Application

selector = DefaultSelector()

def view():
    client = Client(selector)
    url = 'http://www.xuetangx.com/courses'
    client.get(url)
    print('first request done')

    client = Client(selector)
    url = 'http://www.xuetangx.com/courses'
    client.get(url)
    print('second request done')


view()
view()

app = Application(selector)
app.ioloop()

