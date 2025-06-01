from app.repositories import redis, logger, alchemy
from app.entity.prompt import Prompt
from pkg.database.alchemy import select, desc
from sqlalchemy import func

class PromptRepositories(object):
    def __init__(self):
        self.redis = redis
        self.model = Prompt
        self.table = Prompt.__table__
        self.db = alchemy
        self.key = "config:prompt"

    async def upsert(self, prompt: Prompt):
        try:
            entity = {
                "prompt": prompt.prompt,
                "scope_id": prompt.scope_id,
                "is_default": prompt.is_default,
                "created_at": prompt.created_at
            }
            if prompt.id is not None:
                entity["id"] = prompt.id
                entity["updated_at"] = prompt.updated_at
                

            id = await self.db.upsert_without_tx(
                model=self.model,
                values=entity,
                conflict_key=["id"]
            )
            
            entity["id"] = id
            key = self.key+":"+str(prompt.scope_id)
            if prompt.is_default:
                self.redis.set(key, entity)
            return id
        except Exception as e:
            raise e
        
    async def set_prompt_config(self, id_prompt, scope_id):
        try:
            query = select(self.table).where(Prompt.id==id_prompt and Prompt.scope_id==scope_id)
            data_prompt = await self.db.fetch(query=query, arguments={})
            if data_prompt is None:
                return None
            await self.db.update_without_tx(
                table=self.table, 
                values={
                    "is_default": True
                },
                where_clause=(self.model.id==id_prompt)
            )
            key = self.key+":"+str(data_prompt.scope_id)
            return await self.redis.set(key, data_prompt.prompt)
        except Exception as e:
            raise e
        
    async def get_prompt_config(self):
        try:
            query = select(self.table).where(Prompt.is_default==True)
            data_prompt = await self.db.fetch(query=query, arguments={})
            if data_prompt is None:
                return None
            return data_prompt
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
                .order_by(desc(Prompt.id))
            )

            # Eksekusi query untuk mendapatkan data
            results = await self.db.find(query=query, arguments={})

            # Hitung total data untuk mengetahui jumlah halaman
            total_query = select(func.count(self.table.c.id))  # Menggunakan func.count
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
        
    async def get_prompt(self, scope_id=None):
        try:
            key = self.key+":"+str(scope_id)
            prompt = await self.redis.get(key)
            if prompt is None:
                prompt = ""
            return prompt
        except Exception as e:
            logger.error("Error getting prompt", {
                "error": str(e),
            })
            raise e
        
    async def delete(self, id):
        await self.db.delete_without_tx(table=self.table, where_clause=(Prompt.id==id))

    async def delete_prompt_config(self, scope_id):
        key = self.key+":"+str(scope_id)
        return await self.redis.delete(key)