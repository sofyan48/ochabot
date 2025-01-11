from pkg.database import DatabaseConfig
import pymysql
from langchain_community.utilities import SQLDatabase
from sqlalchemy.ext.asyncio import create_async_engine


class MySQL(object):
    def __init__(self, cfgWrite: DatabaseConfig, cfgRead: DatabaseConfig):
       self.cfgWrite = cfgWrite.get_config()
       self.cfgRead = cfgRead.get_config()

    def write_connection(self, auto_commit=True):
        conn = pymysql.connect(
            host=self.cfgWrite.get("host"),
            port=int(self.cfgWrite.get("port")),
            user=self.cfgWrite.get("user"),
            password=self.cfgWrite.get("password"),
            database=self.cfgWrite.get("name")
        )
        conn.autocommit = auto_commit
        return conn

    def read_connection(self):
        conn = pymysql.connect(
            host=self.cfgRead.get("host"),
            port=int(self.cfgRead.get("port")),
            user=self.cfgRead.get("user"),
            password=self.cfgRead.get("password"),
            database=self.cfgRead.get("name")
        )
        return conn