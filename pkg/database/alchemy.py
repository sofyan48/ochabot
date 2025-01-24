from pkg.database import DatabaseConfig  
from sqlalchemy.ext.asyncio import create_async_engine  
from sqlalchemy import create_engine  
  
class AlChemy(object):  
    _instance = None  
    _sync_engine = None  
    _async_engine = None  
  
    def __new__(cls, cfgWrite: DatabaseConfig):  
        if cls._instance is None:  
            cls._instance = super(AlChemy, cls).__new__(cls)  
            cls._instance.cfgWrite = cfgWrite.get_config()  
        return cls._instance  
  
    def connection_setup(self, driver="postgre"):  
        connection_str = ""  
        if driver == "postgre":  
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
        if self._async_engine is None:  
            self._async_engine = create_async_engine(  
                url=conn_str,   
                isolation_level="AUTOCOMMIT",   
                echo=debug,  
                pool_pre_ping=True  
            )  
        return self._async_engine  
      
    def engine(self, driver="postgre", debug=False):  
        conn_str = self.connection_setup(driver=driver)  
        if self._sync_engine is None:  
            self._sync_engine = create_engine(  
                url=conn_str,   
                isolation_level="AUTOCOMMIT",   
                echo=debug  
            )  
        return self._sync_engine  
  
    @classmethod  
    def get_instance(cls, cfgWrite: DatabaseConfig):  
        if cls._instance is None:  
            cls._instance = cls(cfgWrite)  
        return cls._instance  
  
    @classmethod  
    def get_engine(cls, cfgWrite: DatabaseConfig, driver="postgre", debug=False, async_=False):  
        instance = cls.get_instance(cfgWrite)  
        if async_:  
            return instance.async_engine(driver=driver, debug=debug)  
        else:  
            return instance.engine(driver=driver, debug=debug)  
