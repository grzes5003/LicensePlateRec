from dataclasses import dataclass


@dataclass
class LicensePlate:
    plate_value: str
    confidence: float
    coordinates: dict
    process_time: float