from dataclasses import dataclass
import json


@dataclass(repr=True, order=True)
class Frame:
    value: int

