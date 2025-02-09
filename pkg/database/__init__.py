
class DatabaseConfig:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def get_config(self):
        return {
            "name": self.dbname,
            "user": self.user,
            "password": self.password,
            "host": self.host,
            "port": self.port
        }
    

class ElasticConfig:
    def __init__(self, user, password, host, port):
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def get_config(self):
        return {
            "user": self.user,
            "password": self.password,
            "host": self.host,
            "port": self.port
        }
    