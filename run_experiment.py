# run_experiment.py

import random
import numpy
import fl_simulator.server as sv
import fl_simulator.client as cl
import asyncio
import logger

def set_seed(seed=2):
    random.seed(seed)
    numpy.random.seed(seed)

async def run_simulation_async(exp_type, exp_CS_algo, no_of_cln=10, no_of_rounds=10):
    set_seed(2)
    logger.reset_logs()

    # Fixed constants (can be added as parameters later if needed)
    resp_var = 0.1
    avg_download_time = 0.1
    avg_computation_time = 0.4
    avg_upload_time = 0.2
    avg_data_update = 2
    learning_rate = 0.5

    threshold = 0.4 if exp_CS_algo == "threshold" else None

    logger.log("PICKED VARIABLES FOR THE EXPERIMENT")
    logger.log(f"Dataset type: {exp_type}")
    logger.log(f"Client selection algorithm: {exp_CS_algo}")
    logger.log(f"Number of picked clients per round: {no_of_cln}")
    logger.log(f"Response time threshold: {threshold}\n")

    print(f"Running {exp_type} experiment with client selection algorithm: {exp_CS_algo}")

    clients = []
    avg_resp_vals = (resp_var, avg_download_time, avg_computation_time, avg_upload_time)

    def homo(dev):
        for i in range(15):
            avg_dataset_vals = (avg_data_update, 2, 5, 0, 10, dev)
            clients.append(cl.Client(f"client_{i}", exp_CS_algo, 10, avg_resp_vals, avg_dataset_vals))

    def semi_homo(dev):
        for i in range(15):
            slope, constant = (2, 6) if i < 3 else (3, 5) if i < 6 else (2, 5) if i < 9 else (2, 4) if i < 12 else (1, 5)
            avg_dataset_vals = (avg_data_update, slope, constant, 0, 10, dev)
            clients.append(cl.Client(f"client_{i}", exp_CS_algo, 10, avg_resp_vals, avg_dataset_vals))

    def hetero(dev):
        for i in range(15):
            slope, constant = (2, 7) if i < 5 else (4, 5) if i < 10 else (2, 5)
            avg_dataset_vals = (avg_data_update, slope, constant, 0, 10, dev)
            clients.append(cl.Client(f"client_{i}", exp_CS_algo, 10, avg_resp_vals, avg_dataset_vals))

    if exp_type == "homo_low_dev":
        homo(1)
    elif exp_type == "homo_high_dev":
        homo(5)
    elif exp_type == "semi_homo_low_dev":
        semi_homo(1)
    elif exp_type == "semi_homo_high_dev":
        semi_homo(5)
    elif exp_type == "hetero_low_dev":
        hetero(1)
    elif exp_type == "hetero_high_dev":
        hetero(5)
    else:
        raise KeyError("Invalid experiment type.")

    server = sv.Server(exp_CS_algo, learning_rate, no_of_clients=no_of_cln, threshold=threshold)

    for client in clients:
        server.add_client(client, 10)

    await server.train_model(no_of_rounds)

    # Return results
    return {
        "global_slope": server.slope,
        "global_constant": server.constant,
        "logs": logger.get_logs()
    }

def run_simulation(dataset_type, selection_algo, num_clients=10, rounds=10):
    return asyncio.run(run_simulation_async(dataset_type, selection_algo, num_clients, rounds))

