import asyncpg as pg
from dataclasses import dataclass, field


class Column:
    def __init__(self, value_type, value=None, length=None, size=None):
        self.type = value_type
        self.value = value
        self.max_length = length
        self.size = size

    def __repr__(self):
        return self.value
