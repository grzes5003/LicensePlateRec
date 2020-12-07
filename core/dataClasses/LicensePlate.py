from dataclasses import dataclass, field
from typing import List, Dict


@dataclass(order=True)
class LicensePlate:
    plate_value: str
    confidence: float
    coordinates: List[Dict[str, int]] = field(repr=False)
    process_time: float = field(repr=False)
