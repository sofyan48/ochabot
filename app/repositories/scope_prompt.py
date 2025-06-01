from app.repositories import redis, logger, alchemy
from app.entity.scope_prompt import ScopePrompts
from pkg.database.alchemy import select, desc
from sqlalchemy import func

class ScopePromptRepositories(object):
    def __init__(self):
        self.model = ScopePrompts
        self.table = ScopePrompts.__table__
        self.db = alchemy

    async def upsert(self, scope_prompt: ScopePrompts):
        try:
            entity = {
                "name": scope_prompt.name,
                "created_at": scope_prompt.created_at,
                "updated_at": scope_prompt.updated_at,
            }
            if scope_prompt.id is not None:
                entity["id"] = scope_prompt.id
            
            return await self.db.upsert_without_tx(
                model=self.model, 
                values=entity,
                conflict_key=["id"]
            )
        except Exception as e:
            raise e
        
    async def delete(self, id):
        await self.db.delete_without_tx(table=self.table, where_clause=(ScopePrompts.id==id))
    
    async def get(self, id: int):
        try:
            query = select(self.table).where(ScopePrompts.id == id)
            result = await self.db.fetch(query=query, arguments={})
            return result
        except Exception as e:
            raise e

    async def list(self, page: int = 1, per_page: int = 10):
        try:
            # Hitung offset berdasarkan halaman dan jumlah item per halaman
            offset = (page - 1) * per_page

            # Query dengan limit dan offset untuk pagination
            query = (
                select(self.table)
                .limit(per_page)
                .offset(offset)
                .order_by(desc(ScopePrompts.id))
            )

            # Eksekusi query
            results = await self.db.find(query=query, arguments={})

            # Hitung total data untuk mengetahui jumlah halaman
            total_query = select(func.count(self.table.c.id))
            total_count = await self.db.count(query=total_query)

            # Hitung total halaman
            total_pages = (total_count + per_page - 1) // per_page

            return {
                "data": results,
                "pagination": {
                    "current_page": page,
                    "per_page": per_page,
                    "total_pages": total_pages,
                    "total_items": total_count,
                },
            }
        except Exception as e:
            raise e