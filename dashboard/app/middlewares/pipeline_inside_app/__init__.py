from flask import Flask, request

def configure_middlewares(app: Flask):
    @app.before_request
    def authentication():
        print("1")
    @app.before_request
    def authorization():
        print("2")