import redis

host = '192.168.100.3'
# host = '127.0.0.1'
port = 6379
password = 'passwd'
max_connections = 10
POOL = redis.ConnectionPool(host=host, port=port, password=password, max_connections=max_connections,
                            decode_responses=True)


def get_redis_conn():
    return redis.Redis(connection_pool=POOL)

