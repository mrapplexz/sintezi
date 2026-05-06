from enum import StrEnum


class ResponseFormatCapability(StrEnum):
    json = "json"
    json_schema = "json_schema"
    ebnf = "ebnf"
