from dataclasses import fields, MISSING, is_dataclass
from enum import Enum
from typing import Any, Dict, Type, TypeVar, get_origin, get_args

T = TypeVar("T")


def _is_optional(tp):
    return get_origin(tp) is not None and type(None) in get_args(tp)


def _default_is_none(f):
    if f.default is not MISSING:
        return f.default is None
    if f.default_factory is not MISSING:
        return f.default_factory() is None
    return False


def to_json(obj):
    if is_dataclass(obj):
        result = {}

        for f in fields(obj):
            if not f.init or not f.repr:
                continue

            raw_value = getattr(obj, f.name)

            if (
                raw_value is None
                and _is_optional(f.type)
                and _default_is_none(f)
            ):
                continue

            result[f.name] = to_json(raw_value)

        return result

    if isinstance(obj, Enum):
        return obj.value

    if isinstance(obj, (list, tuple)):
        return [to_json(v) for v in obj]

    if isinstance(obj, dict):
        return {k: to_json(v) for k, v in obj.items()}

    return obj

def from_dict(model: Type[T], data: Dict[str, Any]) -> T:
    if not is_dataclass(model):
        raise TypeError(f"{model} is not a dataclass")

    if not isinstance(data, dict):
        raise TypeError("data must be a dict")

    allowed_keys = {f.name for f in fields(model)}
    filtered = {k: v for k, v in data.items() if k in allowed_keys}

    return model(**filtered)
