from dataclasses import dataclass, field
import json


@dataclass(repr=True, order=True)
class Frame:
    id_: int
    time_stamp_: float = field(compare=False, default=0.0)
    img_: [] = field(compare=False, default=None, repr=False)
