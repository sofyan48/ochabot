
from pkg.database import DatabaseConfig
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import create_engine


class AlChemy(object):
    def __init__(self, cfgWrite: DatabaseConfig):
       self.cfgWrite = cfgWrite.get_config()

    def connection_setup(self, driver="postgre"):
        connection_str = ""
        if(driver == "postgre"):
            connection_str = "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
                self.cfgWrite.get("user"),
                self.cfgWrite.get("password"),
                self.cfgWrite.get("host"),
                self.cfgWrite.get("port"),
                self.cfgWrite.get("name")
            )
        else:
            connection_str = "mysql+aiomysql://{}:{}@{}:{}/{}".format(
                self.cfgWrite.get("user"),
                self.cfgWrite.get("password"),
                self.cfgWrite.get("host"),
                self.cfgWrite.get("port"),
                self.cfgWrite.get("name")
            )
        return connection_str
    
    def async_engine(self, driver="postgre", debug=False):
        conn_str = self.connection_setup(driver=driver)
        conn = create_async_engine(
            url=conn_str, 
            isolation_level="AUTOCOMMIT", 
            echo=debug,
            pool_pre_ping=True
        )
        return conn
    
    def engine(self, driver="postgre", debug=False):
        conn_str = self.connection_setup(driver=driver)
        return create_engine(url=conn_str, 
                            isolation_level="AUTOCOMMIT", echo=debug)
         