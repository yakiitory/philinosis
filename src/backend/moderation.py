import re
from .lists import FILIPINO_SWEAR_WORDS

patterns = []
for word in FILIPINO_SWEAR_WORDS:
    escaped = re.escape(word)
    escaped = escaped.replace(r"\ ", r"[\s-]+")
    patterns.append(escaped)

PROFANITY_PATTERN = re.compile(
    r"\b(?:"
    + "|".join(patterns)
    + r")\b",
    re.IGNORECASE,
)

def count_profanity(message: str) -> int:
    return len(PROFANITY_PATTERN.findall(message))
