from flask import request, Response
from app.authorization import guardian
from vakt import Inquiry
def authorize(policy=""):
    def get_func_param(func):
        def wrapper(*args, **kwargs):
            # impelement authorize this
            is_authorized = False
            if "user" in request:
                is_authorized = True
            if is_authorized:
                return func(*args, **kwargs)
            else:
                return Response(response="Unauthorized", status=401)
        return wrapper
    return get_func_param

def abac_authorize(policy=""):
    def get_func_param(func):
        def wrapper(*args, **kwargs):
            # impelement authorize this
            is_authorized = False
            if "user" in request:
                is_authorized = True
            
            user = request["user"]
            
            inquiry = Inquiry(action=user["action"],
                                resource=user["resource"],
                                subject=user["subject"],
                                context=user["context"])
            is_authorized = guardian.check(inquiry)
            if is_authorized:
                return func(*args, **kwargs)
            else:
                return Response(response="Unauthorized", status=401)
        return wrapper
    return get_func_param
            