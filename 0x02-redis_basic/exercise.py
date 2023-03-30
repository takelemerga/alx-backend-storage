#!/usr/bin/env python3
"""
python module interact with redis server
"""
from uuid import uuid4
import redis
from functools import wraps
from typing import Any, Callable, Union


def count_calls(method: Callable) -> Callable:
    """count number of times cache methods called"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """invokes func"""
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Tracks the call details of a method in a Cache class"""
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def invoker(self, *args, **kwargs):
        """ invoker """
        self._redis.rpush(inputs, str(args))
        value = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(outputs, str(value))
        return value

    return invoker


def replay(method: Callable) -> None:
    """
    Replays the history of a function
    """
    name = method.__qualname__
    store = redis.Redis()
    calls_count = store.get(name).decode("utf-8")
    print("{} was called {} times:".format(name, calls_count))
    inputs = store.lrange(name + ":inputs", 0, -1)
    outputs = store.lrange(name + ":outputs", 0, -1)
    for i, o in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(name, i.decode('utf-8'),
                                     o.decode('utf-8')))


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """generate random key and return it"""
        r_key = str(uuid4())
        self._redis.set(r_key, data)
        return r_key

    def get(
            self,
            key: str,
            fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        """Retrieves a value from a Redis data storage.
        """
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

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
