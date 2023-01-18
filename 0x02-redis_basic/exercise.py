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
