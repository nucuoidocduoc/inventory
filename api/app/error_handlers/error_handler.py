from flask import Flask
def handle_bad_request(e):
    return 'bad request!', 400

def handle_server_error(e):
    return 'server error!', 500

def handle_general_error(e):
    return 'general error!'

def error_hander_register(app: Flask):
    app.register_error_handler(400, handle_bad_request)
    app.register_error_handler(500, handle_server_error)
    app.register_error_handler(Exception, handle_general_error)