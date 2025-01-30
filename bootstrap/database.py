from pkg.database import DatabaseConfig
from pkg.database import alchemy
import os
    

def register_alchemy_async():
    driver = os.environ.get("DB_DRIVER", "mysql")
    configWrite = DatabaseConfig(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )

    configRead = DatabaseConfig(
        dbname=os.getenv("DB_NAME_READ"),
        user=os.getenv("DB_USER_READ"),
        password=os.getenv("DB_PASSWORD_READ"),
        host=os.getenv("DB_HOST_READ"),
        port=os.getenv("DB_PORT_READ"),
    )
    
    return alchemy.AlChemy.get_instance(
        cfgWrite=configWrite,
        cfgRead=configRead,
        driver=driver
    )

