#!/usr/bin/env python3
"""
python module interact with redis server
"""
from uuid import uuid4
import redis


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data):
        """generate random key and return it"""
        r_key = str(uuid4())
        self._redis.set(r_key, data)
        return r_key

    def get_str(self, key: str) -> str:
        """convert to string data type"""
        value = self._redis.get(key)
        return value.decode('utf-8')

    def get_int(self, key: str) -> int:
        """convert to int data type"""
        value = self._redis.get(key)
        try:
            value = int(value.decode('utf-8'))
        except Exception:
            value = 0
        return value
