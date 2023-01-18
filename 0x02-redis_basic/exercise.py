#!/usr/bin/env python3
"""
python module interact with redis server
"""
import uuid
import redis


class Cache:
    def __init__(self):
        self.__redis = redis.Redis()
        self.__redis.flushdb()


    def store(self, data):
        """generate random key and return it"""
        r_key = str(uuid.uuid4())
        self.__redis.set(r_key, data)
        return r_key
