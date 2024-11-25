from enum import Enum


class GenericModificationTypes(Enum):
    DATETIME_TO_STRING = (
        "isinstance(value, datetime)",
        lambda x: x.isoformat(),
        "from datetime import datetime",
    )
    STRIP_WHITESPACE = ("isinstance(value, str)", lambda x: x.strip())
    TO_UPPERCASE = ("isinstance(value, str)", lambda x: x.upper())
    TO_LOWERCASE = ("isinstance(value, str)", lambda x: x.lower())
    ROUND_FLOAT = ("isinstance(value, float)", lambda x: round(x, 2))

