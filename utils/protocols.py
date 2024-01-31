from typing import Protocol
from dataclasses import dataclass


@dataclass
class NavalObject(Protocol):
    def render_json(self) -> str:
        raise NotImplementedError()

    @classmethod
    def load_from_json_str(cls, json_string: str) -> "NavalObject":
        raise NotImplementedError()
