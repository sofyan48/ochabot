import psycopg2
from pkg.database import DatabaseConfig

class Postgree(object):
    def __init__(self, cfgWrite: DatabaseConfig, cfgRead: DatabaseConfig):
        self.cfgWrite = cfgWrite.get_config()
        self.cfgRead = cfgRead.get_config()


    def write_connection(self, auto_commit=True):
        conn = psycopg2.connect(
            dbname=self.cfgWrite.get("name"), 
            user=self.cfgWrite.get("user"), 
            password=self.cfgWrite.get("password"), 
            host=self.cfgWrite.get("host"), 
            port=self.cfgWrite.get("port")
        )
        conn.autocommit = auto_commit
        return conn

    def read_connection(self):
        conn = psycopg2.connect(
            dbname=self.cfgRead.get("name"), 
            user=self.cfgRead.get("user"), 
            password=self.cfgRead.get("password"), 
            host=self.cfgRead.get("host"), 
            port=self.cfgRead.get("port")
        )
        return conn
    


