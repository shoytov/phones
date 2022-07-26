from typing import Optional

from fastapi_cache import FastAPICache
from starlette.requests import Request
from starlette.responses import Response


def key_builder(
    func,
    namespace: Optional[str] = "",
    request: Optional[Request] = None,
    response: Optional[Response] = None,
    *args,
    **kwargs,
) -> str:
    prefix = FastAPICache.get_prefix()
    cache_key = f"{prefix}:{namespace}:{func.__module__}:{func.__name__}:{args}:{kwargs}"

    return cache_key
