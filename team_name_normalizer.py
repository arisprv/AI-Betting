import re
from typing import Optional

_STRIP_TOKENS = re.compile(r'\b(FC|AFC|SC|CF|AC|AS|RC|SD|RCD|UD|CD|Athletic|Club|de|la|le|les|el)\b', re.IGNORECASE)
_WHITESPACE = re.compile(r'\s+')


def normalize(name: str) -> str:
    if not isinstance(name, str):
        return ""
    cleaned = _STRIP_TOKENS.sub(" ", name)
    return _WHITESPACE.sub(" ", cleaned).strip().lower()


def names_match(a: str, b: str) -> bool:
    return normalize(a) == normalize(b)


def find_best_match(target: str, candidates: list[str]) -> Optional[str]:
    target_norm = normalize(target)
    for candidate in candidates:
        if normalize(candidate) == target_norm:
            return candidate
    for candidate in candidates:
        if normalize(candidate) in target_norm or target_norm in normalize(candidate):
            return candidate
    return None