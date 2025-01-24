from pkg.database import DatabaseConfig
import os
    

def register_alchemy_async():
    from pkg.database.alchemy import AlChemy
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
    from pkg.database.alchemy import AlChemy
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
        async_=False
    )