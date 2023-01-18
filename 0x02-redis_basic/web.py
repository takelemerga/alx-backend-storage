#!/usr/bin/env python3
"""module"""
import redis
import requests
from functools import wraps
from typing import Callable


r = redis.Redis()


def cacher(method: Callable) -> Callable:
    """Caches the output of fetched data.
    """
    @wraps(method)
    def wrapper(url) -> str:
        """caching the output.
        """
        r.incr(f"count:{url}")
        fetched = r.get(f"fetched:{url}")
        if fetched:
            return fetched.decode('utf-8')
        fetched = method(url)
        r.set(f'count:{url}', 0)
        r.setex(f'fetched:{url}', 10, fetched)
        return fetched
    return wrapper


@cacher
def get_page(url: str) -> str:
    """Returns the content of a URL after caching the request's response
    """
    return requests.get(url).text
