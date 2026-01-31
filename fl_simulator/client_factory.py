from .client_selection_algorithms.client import Client
from .common import CSAlgo
from data.common import DatasetType

def create_client(dataset_type: DatasetType, cs_algo: CSAlgo, name) -> Client:
    return cs_algo.value.client(dataset_type, name)