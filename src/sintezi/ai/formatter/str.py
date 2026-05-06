from .base import RequestFormatter


class StrFormatter(RequestFormatter):
    def format(self, content: str) -> str:
        return content
