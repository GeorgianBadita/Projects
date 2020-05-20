from typing import List
import os

import redis

HOST = os.environ.get('AB_HOST', 'localhost')
PORT = int(os.environ.get('AB_PORT', 6379))
DB = int(os.environ.get('AB_DB', 0))

CONN = None


class StoreError(redis.exceptions.RedisError):
    pass


def get():
    global CONN
    if not CONN:
        CONN = redis.Redis(host=HOST, port=PORT, db=DB)
    return CONN


def incr(key: str):
    try:
        return get().incr(key)
    except redis.exceptions.RedisError as e:
        raise StoreError(e, advise())


def mget(keys: List[str]):
    try:
        return get().mget(keys)
    except redis.exceptions.RedisError as e:
        raise StoreError(e, advise())


def advise():
    return 'Please configure & run redis: make redis_install redis_start'
