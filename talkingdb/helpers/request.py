from contextvars import ContextVar
from typing import Dict, Any

_request_context: ContextVar[Dict[str, Any]] = ContextVar(
    "request_context",
    default={},
)


def set_request_context(**kwargs):
    ctx = _request_context.get().copy()
    ctx.update(kwargs)
    _request_context.set(ctx)


def get_request_context() -> Dict[str, Any]:
    return _request_context.get()


def clear_request_context():
    _request_context.set({})
