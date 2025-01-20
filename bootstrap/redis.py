import os

def str_conn():
    str_conn = "redis://:{}@{}:{}/{}".format(
        os.getenv("REDIS_PASSWORD"),
        os.getenv("REDIS_HOST"),
        os.getenv("REDIS_PORT"),
        os.getenv("REDIS_DB")
    )
    
    return str_conn
    