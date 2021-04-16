import inspect
from typing import Iterable, Optional

from parse import parse
from webob import Request, Response


class API:
    def __init__(self):
        self.routes = {}

    def __call__(self, environ: dict, start_response: callable) -> Response:
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)

    def handle_request(self, request: Request) -> Response:
        response = Response()  # Response class is also a WSGI application
        handler, kwargs = self.find_handler(request.path)
        if handler:
            if inspect.isclass(handler):
                handler = getattr(handler(), request.method.lower(), None)
                if not handler:
                    raise AssertionError('Method not allowed: ', request.method)
            handler(request, response, **kwargs)
        else:
            self.not_found(request, response)
        return response

    def find_handler(self, request_path: str) -> Optional[tuple[callable, dict]]:
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result:
                return handler, parse_result.named
        return None, None

    def route(self, path: str) -> callable:
        assert path not in self.routes, f'{path} already exists in a router.'
        def wrapper(handler: callable) -> callable:
            self.routes[path] = handler
            return handler
        return wrapper

    def not_found(self, request: Request, response: Response):
        response.status_code = 404
        response.text = '404 Not found.'


# Basic WSGI application
def application(environ: dict, start_response: callable) -> Iterable[str]:
    response_body = [f'{key}: {value}' for key, value in sorted(environ.items())]
    response_body = '\n'.join(response_body)
    status = '200 OK'
    response_headers = [
        ('Content-Type', 'text/html'),
        ('Content-Length', str(len(response_body))),
    ]
    start_response(status, response_headers)
    return [response_body.encode('utf-8')]  # change to binary
