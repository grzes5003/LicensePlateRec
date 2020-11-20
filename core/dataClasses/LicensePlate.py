from dataclasses import dataclass


@dataclass
class LicensePlate:
    plate_value: str
    confidence: float
    coordinates: dict
    process_time: float

    def __init__(self, plate_value: str, confidence: float, coordinates: dict, process_time: float):
        self.plate_value = plate_value
        self.confidence = confidence
        self.coordinates = coordinates
        self.process_time = process_time