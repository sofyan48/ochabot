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

    async def save(self, prompt: str, is_active=False):
        try: 
            return await self.db.insert_without_tx(self.table, {
                "prompt": prompt,
                "is_active": is_active
            })
        except Exception as e:
            raise e
        
    async def set_prompt_config(self, id_prompt):
        try:
            query = select(self.model).where(self.model.id==id_prompt and self.model.is_active==True)
            data_prompt = await self.db.fetch(query=query, arguments={})
            if data_prompt is None:
                return None
            return await self.redis.set(self.key, data_prompt.get('prompt'))
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
    
    async def delete_prompt(self):
        return await self.redis.delete(self.key)