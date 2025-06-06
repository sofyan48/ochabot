from pkg.database import DatabaseConfig
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy import (
    select,  
    delete, 
    update,
    or_,
    and_,
    desc,
    asc
)
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List, Dict
from pkg.logger.query import logger


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
        conn_str = self.connection_setup(config, driver)
        try:
            return create_async_engine(
                url=conn_str, 
                isolation_level="AUTOCOMMIT", 
                echo=debug,
                pool_pre_ping=True,
                connect_args={}
            )
        except Exception as e:
            logger.error(e)
            raise e
    
    @classmethod
    def get_instance(cls, cfgWrite: DatabaseConfig, cfgRead: DatabaseConfig, driver: str = "postgres"):
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
        return cls._instance_write
    
    @classmethod
    def async_read(cls) -> AsyncEngine:
        return cls._instance_read

    @classmethod
    def get_write_uri(cls) -> str:
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
    async def upsert_with_tx(cls, model, values: Dict, conflict_key):
        """Upsert data dengan transaksi."""
        async with AsyncSession(cls._instance_write) as session:
            async with session.begin():  # Memulai transaksi
                try:
                    stmt = insert(model).values(values)
                    # Create update_dict using the correct method
                    update_structured = {}
                    for c in model.__table__.columns:
                        if c.name in values:  # Check if the column is in values
                            update_structured[c.name] = values[c.name]

                    # Ensure the conflict_key is valid
                    for i in conflict_key:
                        if i not in model.__table__.columns:
                            raise ValueError(f"Conflict key '{conflict_key}' is not a valid column.")
                    
                    stmt = stmt.on_conflict_do_update(
                        index_elements=conflict_key,
                        set_=update_structured
                    )
                    result = await session.execute(stmt)
                    return result.inserted_primary_key[0]
                except SQLAlchemyError as e:
                    await session.rollback()  # Rollback jika terjadi kesalahan
                    raise e  # Lempar kembali kesalahan

    @classmethod
    async def upsert_without_tx(cls, model, values: Dict, conflict_key):
        """Upsert data tanpa transaksi."""
        async with AsyncSession(cls._instance_write) as session:
            try:
                stmt = insert(model).values(values)

                # Create update_dict using the correct method
                update_structured = {}
                for c in model.__table__.columns:
                    if c.name in values:  # Check if the column is in values
                        update_structured[c.name] = values[c.name]

                # Ensure the conflict_key is valid
                for i in conflict_key:
                    if i not in model.__table__.columns:
                        raise ValueError(f"Conflict key '{conflict_key}' is not a valid column.")
                stmt = stmt.on_conflict_do_update(
                    index_elements=conflict_key,
                    set_=update_structured
                )

                result = await session.execute(stmt)
                await session.commit()  # Commit perubahan
                return result.inserted_primary_key[0]
            except SQLAlchemyError as e:
                await session.rollback()  # Rollback jika terjadi kesalahan
                raise e  # Lempar kembali kesalahan
    

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
            result = await session.execute(stmt)
            await session.flush()
            return result.inserted_primary_key[0]
           

    @classmethod
    async def insert_with_tx(cls, table, values: Dict):
        """Insert data dengan transaksi."""
        async with AsyncSession(cls._instance_write) as session:
            async with session.begin():
                stmt = insert(table).values(values)
                result = await session.execute(stmt)
                return result.inserted_primary_key[0]

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

    @classmethod
    async def count(cls, query) -> int:
        """Hitung jumlah baris dalam tabel."""
        async with AsyncSession(cls._instance_read) as session:
            try:
                result = await session.execute(query)
                return result.scalar()  # Mengembalikan jumlah baris
            except Exception as e:
                logger.error("Error counting rows", {"error": str(e)})
                raise e
    
    @classmethod
    async def execute_query(cls, query, arguments: dict = {}, use_transaction: bool = False):
        async with AsyncSession(cls._instance_read) as session:
            try:
                if use_transaction:
                    async with session.begin():
                        result = await session.execute(query, arguments)
                else:
                    result = await session.execute(query, arguments)
                    await session.flush()
                return result
            except SQLAlchemyError as e:
                if use_transaction:
                    await session.rollback()  # Rollback jika terjadi kesalahan
                logger.error("Error executing query", {"error": str(e)})
                raise e
