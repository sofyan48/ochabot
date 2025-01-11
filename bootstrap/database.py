from pkg.database.postgre import Postgree
from pkg.database.mysql import MySQL
from pkg.database.alchemy import AlChemy
from pkg.database import DatabaseConfig
from pkg.database.builder import Builder
import os


def register_postgree() -> Builder:
    write_config = DatabaseConfig(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )

    read_config = DatabaseConfig(
        dbname=os.getenv("DB_NAME_READ"),
        user=os.getenv("DB_USER_READ"),
        password=os.getenv("DB_PASSWORD_READ"),
        host=os.getenv("DB_HOST_READ"),
        port=os.getenv("DB_PORT_READ"),
    )

    conn = Postgree(writeConfig, read_config)
    read = conn.read_connection()
    write = conn.write_connection()
    return Builder(
        client_write=write,
        client_read=read
    )

def register_mysql(app):
    write_config = DatabaseConfig(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )

    read_config = DatabaseConfig(
        dbname=os.getenv("DB_NAME_READ"),
        user=os.getenv("DB_USER_READ"),
        password=os.getenv("DB_PASSWORD_READ"),
        host=os.getenv("DB_HOST_READ"),
        port=os.getenv("DB_PORT_READ"),
    )

    client = MySQL(cfgWrite=write_config, cfgRead=read_config)
    read = client.read_connection()
    write = client.write_connection()
    return Builder(client_write=write, client_read=read)

def register_alchemy_async():
    config = DatabaseConfig(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )
    return AlChemy(cfgWrite=config).async_engine("mysql")
    


