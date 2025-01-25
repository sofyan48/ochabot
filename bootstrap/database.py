from pkg.database import DatabaseConfig
import os
from pkg.database.alchemy import AlChemy 

def register_alchemy_async():
    config = DatabaseConfig(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )
    return AlChemy(cfgWrite=config).get_engine(
        config=config,
        driver="postgre", 
        debug=False, 
        async_=True
    )

def register_alchemy():
    config = DatabaseConfig(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )
    return AlChemy(cfgWrite=config).get_engine(
        config=config,
        driver=os.getenv("DB_DRIVER", "postgres"), 
        debug=False, 
        async_=False
    )