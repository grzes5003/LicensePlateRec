from dataclasses import dataclass, field


@dataclass(order=True)
class LicensePlate:
    id_: int
    number_: str = field(compare=False, default='')
    x_: int = field(compare=False, default=0)
    y_: int = field(compare=False, default=0)
    h_: int = field(compare=False, default=0)
    w_: int = field(compare=False, default=0)
