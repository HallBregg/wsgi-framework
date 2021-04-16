from api import API


app = API()


class ReverseMiddleware:
    def __init__(self, app):
        self.wrapped_app = app

    def __call__(self, environ, start_response, *args, **kwargs):
        wrapped_app_response = self.wrapped_app(environ, start_response)
        middleware_response = [data[::-1] for data in wrapped_app_response]
        return middleware_response


@app.route('/hello/{name}')
def hello(request, response, name):
    response.text = f'Hello {name}'


@app.route('/home')
def home(request, response):
    response.text = 'Hello from HOME page'


@app.route('/about')
def about(request, response):
    response.text = 'Hello from ABOUT page'


@app.route('/book')
class BooksView:
    def get(self, request, response):
        response.text = 'Books GET'

    def post(self, request, response):
        response.text = 'Books POST'
