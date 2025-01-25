from app.repositories import redis, logger


class Prompt(object):
    def __init__(self):
        self.redis = redis
        self.key = "config:prompt"

    async def save_prompt(self, prompt):
        return await self.redis.set(self.key, prompt)

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