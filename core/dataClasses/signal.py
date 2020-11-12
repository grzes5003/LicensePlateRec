from enum import Enum


class Signal(Enum):
    IMG_PROCESSING_FINISHED = 1
    MAN_SUBMITTING_FINISHED = 2
    MAN_STOPPED = 3
    MAN_RUNNING = 4
