# This experiment performs FL on 15 clients
# The picked ML model is 2D linear regression
# The line we want to reach is 2x+5

# SET THE SEED OF THE EXPERIMENT HERE
seed = 6

import random
import numpy as np
random.seed(seed)
np.random.seed(seed)

# to be able to get to fl_simulator and logger folders
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import fl_simulator.server_factory as sv_factory
import fl_simulator.client_factory as cl_factory
import asyncio
import logger.logger as lg
from fl_simulator.common import CSAlgo
from data.common import DatasetType


async def run_exp(
        dataset_type = DatasetType.HETERO_LOW_DEV,
        CS_algo = CSAlgo.ALL,
        rep = 0,
        learning_rate = 0.1,
        no_of_rounds = 50,
        no_of_cln = 15,
        no_of_picked_cln = 8,
        threshold = 0.04,
        download_time_weight = 1,
        computation_time_weight = 1,
        upload_time_weight = 1,
        data_size_weight = 1,
        sample_freshness_weight = 1,
        loss_magnitude_weight = 10
        ):

    m_score_weights = {
        'download_time': download_time_weight,
        'computation_time': computation_time_weight,
        'upload_time': upload_time_weight,
        'data_size': data_size_weight,
        'sample_freshness': sample_freshness_weight,
        'loss_magnitude': loss_magnitude_weight
    }

    logger = lg.Logger()

    # log the picked variables
    logger.add_entry_to_dict("params", {})
    logger.add_entry_to_dict("dataset_type", dataset_type.name, ["params"])
    logger.add_entry_to_dict("cs_algo", CS_algo.name, ["params"])
    logger.add_entry_to_dict("rep", rep, ["params"])
    logger.add_entry_to_dict("learning_rate", learning_rate, ["params"])
    logger.add_entry_to_dict("no_of_rounds", no_of_rounds, ["params"])
    logger.add_entry_to_dict("no_of_picked_clients_per_round", no_of_picked_cln, ["params"])
    logger.add_entry_to_dict("response_time_threshold", threshold, ["params"])

    print(f"[{dataset_type.name}+{CS_algo.name}]" .ljust(40), "is starting")

    # randomly generate data for clients, and then create the clients
    clients = []

    for i in range(no_of_cln):
            client_name = f"client_{i}"
            clients.append(cl_factory.create_client(dataset_type, CS_algo, client_name))
    
    # create the server
    server = sv_factory.create_server(
        CS_algo,
        learning_rate, 
        no_of_picked_clients=no_of_picked_cln, 
        threshold=threshold, 
        logger=logger, 
        dataset_type=dataset_type, 
        m_score_weights = m_score_weights)

    # add the clients to the server
    for client in clients:
        server.add_client(client, 10)

    # train the model
    await server.train_model(no_of_rounds)
    logger.save_logs(f"{CS_algo.name}_{dataset_type.name}_rep_{rep}")

    # print that the experiment is finished
    print(f"[{dataset_type.name}+{CS_algo.name}]" .ljust(40), "finished")




if __name__ == "__main__":
    asyncio.run(run_exp())