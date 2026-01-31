from enum import Enum, auto

class DatasetType(Enum):
    HOMO_LOW_DEV = auto()
    HOMO_HIGH_DEV = auto()
    SEMI_HOMO_LOW_DEV = auto()
    SEMI_HOMO_HIGH_DEV = auto()
    HETERO_LOW_DEV = auto()
    HETERO_HIGH_DEV = auto()