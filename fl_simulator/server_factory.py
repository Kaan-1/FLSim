from .client_selection_algorithms.server import Server
from .common import CSAlgo

def create_server(cs_algo: CSAlgo, learning_rate: float, no_of_picked_clients=None, threshold=None, logger=None, dataset_type=None, m_score_weights = None) -> Server:
    return cs_algo.value.server(cs_algo.name, learning_rate, no_of_picked_clients, threshold, logger, dataset_type, m_score_weights)