import redis.asyncio as redis

from config import Config

JTI_EXPIRY = 3600

jti_blocklist = redis.Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=0  # Uses the default Redis database
)


async def add_jti_to_blocklist(jti: str) -> None:
    """ Adds a JTI to the Redis blocklist with an expiration time. """
    await jti_blocklist.set(name=jti, value="", ex=JTI_EXPIRY)


async def jti_in_blocklist(jti: str) -> bool:
    """ Checks if a JTI exists in the Redis blocklist. """
    result = await jti_blocklist.get(jti)
    return result is not None  # If Redis returns None, JTI is not blocked