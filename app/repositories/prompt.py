from app.repositories import redis, logger, alchemy
from app.entity.prompt import Prompt
from pkg.database.alchemy import select

class PromptRepositories(object):
    def __init__(self):
        self.redis = redis
        self.model = Prompt
        self.table = Prompt.__table__
        self.db = alchemy
        self.key = "config:prompt"

    async def save(self, prompt: str, is_default=False):
        try: 
            return await self.db.insert_without_tx(self.table, {
                "prompt": prompt,
                "is_default": is_default
            })
        except Exception as e:
            raise e
        
    async def set_prompt_config(self, id_prompt):
        try:
            query = select(self.table).where(Prompt.id==id_prompt)
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

            return await self.redis.set(self.key, data_prompt.prompt)
        except Exception as e:
            raise e
        
    async def list(self):
        try:
            query = select(self.table).limit(10)
            return await self.db.find(query=query, arguments={})   
        except Exception as e:
            raise e
        
    async def get_prompt(self):
        try:
            prompt = await self.redis.get(self.key)
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

    async def delete_prompt_config(self):
        return await self.redis.delete(self.key)