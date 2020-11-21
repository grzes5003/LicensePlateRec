from dataclasses import dataclass, field


@dataclass(order=True)
class LicensePlate:
    plate_value: str
    confidence: float
    coordinates: dict
    process_time: float