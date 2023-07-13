from mongoengine import connect, disconnect

class Mongo(object):
    def __init__(self, uri):
        self.uri = uri

    def connect(self,
                connect_timout=None,
                server_selection_timeout=None):

        params = dict(
            host=self.uri
        )
        if connect_timout:
            params['connectTimeoutMS'] = connect_timout
        if server_selection_timeout:
            params['serverSelectionTimeoutMS'] = server_selection_timeout

        connect(**params)

    def disconnect(self):
        disconnect()
