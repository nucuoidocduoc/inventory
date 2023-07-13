from werkzeug.wrappers import Request
from flask import Flask
class Middleware:

    def __init__(self, app: Flask):
        self.app = app

    def __call__(self, environ, start_response):
        # not Flask request - from werkzeug.wrappers import Request
        request = Request(environ)
        print('path: %s, url: %s' % (request.path, request.url))
        # just do here everything what you need
        return self.app(environ, start_response)