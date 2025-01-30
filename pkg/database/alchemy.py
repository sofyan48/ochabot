from pkg.database import DatabaseConfig
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy import (
    select, 
    insert, 
    delete, 
    update, 
    and_, 
    or_,
    
)

from typing import Optional, List, Dict


class AlChemy:
    _instance = None
    _instance_write = None
    _instance_read = None
    _write_url = None

    def __new__(cls, *args, **kwargs):    
        if cls._instance is None:    
            cls._instance = super(AlChemy, cls).__new__(cls)    
        return cls._instance 

    def connection_setup_sync(self, config: DatabaseConfig, driver: str) -> str:
        connection_str = ""
        cfg = config.get_config()
        if driver == "postgres":
            connection_str = "postgresql://{}:{}@{}:{}/{}".format(
                cfg.get("user"),
                cfg.get("password"),
                cfg.get("host"),
                cfg.get("port"),
                cfg.get("name")
            )
        else:
            connection_str = "mysql://{}:{}@{}:{}/{}".format(
                cfg.get("user"),
                cfg.get("password"),
                cfg.get("host"),
                cfg.get("port"),
                cfg.get("name")
            )
        return connection_str   
    
    def connection_setup(self, config: DatabaseConfig, driver: str) -> str:
        connection_str = ""
        cfg = config.get_config()
        if driver == "postgres":
            connection_str = "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
                cfg.get("user"),
                cfg.get("password"),
                cfg.get("host"),
                cfg.get("port"),
                cfg.get("name")
            )
        else:
            connection_str = "mysql+aiomysql://{}:{}@{}:{}/{}".format(
                cfg.get("user"),
                cfg.get("password"),
                cfg.get("host"),
                cfg.get("port"),
                cfg.get("name")
            )
        return connection_str

    def async_engine(self, config: DatabaseConfig, driver: str = "postgres", debug: bool = False) -> AsyncEngine:
        """Membuat engine asinkron berdasarkan konfigurasi yang diberikan."""
        conn_str = self.connection_setup(config, driver)
        return create_async_engine(
            url=conn_str, 
            isolation_level="AUTOCOMMIT", 
            echo=debug,
            pool_pre_ping=True,
            connect_args={}
        )
    
    @classmethod
    def get_instance(cls, cfgWrite: DatabaseConfig, cfgRead: DatabaseConfig, driver: str = "postgres"):
        """Mengambil instance dari AlChemy untuk operasi baca dan tulis."""
        if cls._instance is None:
            cls._instance = super(AlChemy, cls).__new__(cls)  
        
        # Setup untuk instance tulis
        if cls._instance_write is None:
            cls._instance_write = cls._instance.async_engine(config=cfgWrite, driver=driver)
            cls._write_url = cls._instance.connection_setup(config=cfgWrite, driver=driver)
        
        # Setup untuk instance baca
        if cls._instance_read is None:
            cls._instance_read = cls._instance.async_engine(config=cfgRead, driver=driver)
        
        return cls._instance_write, cls._instance_read
    
    @classmethod
    def async_write(cls) -> AsyncEngine:
        """Mengembalikan engine untuk operasi tulis."""
        return cls._instance_write
    
    @classmethod
    def async_read(cls) -> AsyncEngine:
        """Mengembalikan engine untuk operasi baca."""
        return cls._instance_read

    @classmethod
    def get_write_uri(cls) -> str:
        """Mengembalikan URI untuk koneksi tulis."""
        return cls._write_url
    
    @classmethod
    async def fetch(cls, query: select, arguments: dict = {}) -> Optional[dict]:       
        async with AsyncSession(cls._instance_read) as session:    
            try:    
                result = await session.execute(query, arguments)    
                return result.fetchone()
            except Exception as e:    
                raise e
    
    @classmethod      
    async def find(cls, query: select, arguments: dict = {}) -> List[dict]:  
        async with AsyncSession(cls._instance_read) as session:  
            try:  
                result = await session.execute(query, arguments)  
                rows = result.fetchall()  
                return [dict(row._mapping) for row in rows] if rows else []  
            except Exception as e:  
                raise e
            
    @classmethod
    async def update_without_tx(cls, table, values: Dict, where_clause):
        """Update data tanpa transaksi."""
        async with AsyncSession(cls._instance_write) as session:
            stmt = update(table).where(where_clause).values(values)
            await session.execute(stmt)
            await session.flush()

    @classmethod
    async def update_with_tx(cls, table, values: Dict, where_clause):
        """Update data dengan transaksi."""
        async with AsyncSession(cls._instance_write) as session:
            async with session.begin():
                stmt = update(table).where(where_clause).values(values)
                await session.execute(stmt)

    @classmethod
    async def insert_without_tx(cls, table, values: Dict):
        """Insert data tanpa transaksi."""
        async with AsyncSession(cls._instance_write) as session:
            stmt = insert(table).values(values)
            await session.execute(stmt)
            await session.flush()

    @classmethod
    async def insert_with_tx(cls, table, values: Dict):
        """Insert data dengan transaksi."""
        async with AsyncSession(cls._instance_write) as session:
            async with session.begin():
                stmt = insert(table).values(values)
                await session.execute(stmt)

    @classmethod
    async def delete_with_tx(cls, table, where_clause):
        """Delete data dengan transaksi."""
        async with AsyncSession(cls._instance_write) as session:
            async with session.begin():
                stmt = delete(table).where(where_clause)
                await session.execute(stmt)

    @classmethod
    async def delete_without_tx(cls, table, where_clause):
        """Delete data tanpa transaksi."""
        async with AsyncSession(cls._instance_write) as session:
            stmt = delete(table).where(where_clause)
            await session.execute(stmt)
            await session.flush()
