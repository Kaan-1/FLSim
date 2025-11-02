from .client_selection_algorithms.client import Client
from .common import CSAlgo

def create_client(cs_algo: CSAlgo, name, init_dataset_size, avg_resp_vals, avg_data_vals) -> Client:
    return cs_algo.value.client(name, init_dataset_size, avg_resp_vals, avg_data_vals)