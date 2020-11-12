from dataclasses import dataclass


@dataclass(repr=True, order=True)
class Frame:
    value: int
