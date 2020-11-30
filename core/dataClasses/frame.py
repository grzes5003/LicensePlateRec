from dataclasses import dataclass, field
from core.dataClasses.LicensePlate import LicensePlate
from typing import List


@dataclass(repr=True, order=True)
class Frame:
    id_: int
    time_stamp_: float = field(compare=False, default=0.0, repr=False)
    img_: [] = field(compare=False, default=None, repr=False)
    license_plates_: List[LicensePlate] = field(compare=False, default_factory=lambda: [])
