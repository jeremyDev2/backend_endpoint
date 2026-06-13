import redis.asyncio as redis
from app.settings import settings

redis_client = redis.from_url(str(settings.redis_dns), decode_responses=True)

_DECREMENT_STOCK_LUA = """
local stock = redis.call('GET', KEYS[1])
if stock == false then
    return -2
end
stock = tonumber(stock)
local qty = tonumber(ARGV[1])
if stock >= qty then
    redis.call('DECRBY', KEYS[1], qty)
    return stock - qty
end
return -1
"""

decrement_stock = redis_client.register_script(_DECREMENT_STOCK_LUA)
