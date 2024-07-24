import aioredis
from common.log import LoggingConfig


class AsyncRedisClient:
    def __init__(self, host='localhost', port=6379, db=0, password='yourpassword'):
        self.client = aioredis.Redis(
            host=host,
            port=port,
            db=db,
            password=password
        )
        self.logging_config = LoggingConfig(log_name="AsyncRedisClient")

    async def set_value(self, key, value, ex=None):
        """
        Set the value of a key.

        :param key: The key to set.
        :param value: The value to set.
        :param ex: Expiration time in seconds (optional).
        """
        log = await self.logging_config.get_logger("set_value")
        try:
            await self.client.set(key, value, ex=ex)

            log.info(f"Key '{key}' set to '{value}' with expiration {ex} seconds" if ex else f"Key '{key}' set to '{value}'")
        except aioredis.RedisError as e:
            log.error(f"Error setting key '{key}': {e}")

    async def get_value(self, key):
        """
        Get the value of a key.

        :param key: The key to get.
        :return: The value of the key or None if the key does not exist.
        """
        log = await self.logging_config.get_logger("get_value")
        try:
            value = await self.client.get(key)
            if value is not None:
                return value
            else:
                log.info(f"Key '{key}' does not exist")
                return None
        except aioredis.RedisError as e:
            log.error(f"Error getting key '{key}': {e}")
            return None

    async def delete_key(self, key):
        """
        Delete a key.

        :param key: The key to delete.
        :return: None
        """
        log = await self.logging_config.get_logger("delete_key")
        try:
            result = await self.client.delete(key)
            if result:
                log.info(f"Key '{key}' deleted")
            else:
                log.info(f"Key '{key}' does not exist")
        except aioredis.RedisError as e:
            log.error(f"Error deleting key '{key}': {e}")

    async def exists(self, key):
        """
        Check if a key exists.

        :param key: The key to check.
        :return: True if the key exists, False otherwise.
        """
        log = await self.logging_config.get_logger("exists")
        try:
            return await self.client.exists(key) == 1
        except aioredis.RedisError as e:
            log.error(f"Error checking existence of key '{key}': {e}")
            return False

    async def keys(self, pattern='*'):
        """
        Get all keys matching a pattern.

        :param pattern: The pattern to match keys (default '*').
        :return: A list of keys.
        """
        log = await self.logging_config.get_logger("keys")
        try:
            return await self.client.keys(pattern)
        except aioredis.RedisError as e:
            log.error(f"Error getting keys with pattern '{pattern}': {e}")
            return []

    async def expire(self, key, time):
        """
        Set a key's time to live in seconds.

        :param key: The key to set expiration.
        :param time: Time to live in seconds.
        :return: True if the timeout was set, False if key does not exist or timeout could not be set.
        """
        log = await self.logging_config.get_logger("expire")
        try:
            result = await self.client.expire(key, time)
            if result:
                log.info(f"Expiration for key '{key}' set to {time} seconds")
                return True
            else:
                log.info(f"Failed to set expiration for key '{key}'")
                return False
        except aioredis.RedisError as e:
            log.error(f"Error setting expiration for key '{key}': {e}")
            return False

    async def incr(self, key, amount=1):
        """
        Increment the value of a key by a given amount.

        :param key: The key to increment.
        :param amount: The amount to increment by (default is 1).
        :return: The new value of the key after incrementing.
        """
        log = await self.logging_config.get_logger("expire")
        try:
            new_value = await self.client.incrby(key, amount)
            log.info(f"Key '{key}' incremented by {amount}. New value: {new_value}")
            return new_value
        except aioredis.RedisError as e:
            log.error(f"Error incrementing key '{key}': {e}")
            return None



# Example usage
async def main():
    client = AsyncRedisClient()
    await client.set_value('test', '1')
    value = await client.get_value('test')
    print(f"Value: {value}")
    new_value = await client.incr('test', 5)
    print(f"New Value after increment: {new_value}")
    await client.delete_key('test')

# Run the example
# asyncio.run(main())
