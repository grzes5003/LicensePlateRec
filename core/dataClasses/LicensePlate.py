from dataclasses import dataclass, field


@dataclass(order=True)
class LicensePlate:
    plate_value: str
    confidence: float
    coordinates: dict = field(repr=False)
    process_time: float = field(repr=False)
