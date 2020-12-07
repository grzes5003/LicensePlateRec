from dataclasses import dataclass, field
from core.dataClasses.LicensePlate import LicensePlate
from typing import List, Optional


@dataclass(repr=True, order=True)
class Frame:
    id_: int
    time_stamp_: float = field(compare=False, default=0.0)
    img_: [] = field(compare=False, default=None, repr=False)
    license_plates_: Optional[List[LicensePlate]] = field(compare=False, default_factory=lambda: [])
    is_analysed_: bool = field(compare=False, default=False)
    fps_: float = field(compare=False, default=0)
