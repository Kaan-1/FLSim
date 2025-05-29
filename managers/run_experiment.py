# This experiment performs FL on 15 clients
# The picked ML model is 2D linear regression
# The line we want to reach is 2x+5

# SET THE SEED OF THE EXPERIMENT HERE
seed = 6

import random
import numpy
random.seed(seed)
numpy.random.seed(seed)

# to be able to get to fl_simulator and logger folders
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import fl_simulator.server as sv
import fl_simulator.client as cl
import asyncio
import logger.logger as lg

async def run_exp(experiment_type=None, experiment_CS_algo=None, total_number_of_clients=None, repeat=10):

    #######################################################################
    ####################### VARIABLE SPOT START ###########################
    #######################################################################


    # type of dataset to be used for clients
    # detalied information about the datasets can be found in the readme
    # possible values include: 
        # homo_low_dev 
        # homo_high_dev 
        # semi_homo_low_dev
        # semi_homo_high_dev 
        # hetero_low_dev
        # hetero_high_dev
    exp_type = "homo_low_dev"
    if experiment_type != None:
        exp_type = experiment_type


    # type of CS algorithm to be tested in the simulation
    # possible values include
        # loss
        # threshold
        # reputation
        # multi
    exp_CS_algo = "threshold"
    if experiment_CS_algo != None:
        exp_CS_algo = experiment_CS_algo


    # variance of response times that the clients will have
    # Recommended values
        # low: 0.25
        # mid: 1
        # high: 5
    resp_var = 0.01


    # average download time of clients
    avg_download_time = 0.01


    # average computation time of clients
    avg_computation_time = 0.04


    # average upload time of clients
    avg_upload_time = 0.02


    # initial dataset size of clients
    cln_init_dataset_size = 100


    # average number of entries to be deleted/added per round for clients
    avg_data_update = 10


    # Learning rate of the ML algorithm
    learning_rate = 0.05


    # no of rounds to train the model
    no_of_rounds = 100


    # number of clients to be picked each round
    # Redundant for some of the CS algorihms, such as threshold based CS
    # Total number of clients is 15
    no_of_picked_cln = total_number_of_clients//2


    # Time limit that clients are allowed to compute their updates in
    # Only used in threshold based client selection
    # Have to make it None otherwise, because of the current implementation
    threshold = 0.04
    if exp_CS_algo != "threshold":
        threshold = None



    # weights of criterias for multi-criteria based CS
    download_time_weight = 1
    computation_time_weight = 1
    upload_time_weight = 1
    data_size_weight = 1
    sample_freshness_weight = 1
    loss_magnitude_weight = 10
    m_score_weights = {
        'download_time': download_time_weight,
        'computation_time': computation_time_weight,
        'upload_time': upload_time_weight,
        'data_size': data_size_weight,
        'sample_freshness': sample_freshness_weight,
        'loss_magnitude': loss_magnitude_weight
    }


    #######################################################################
    ####################### VARIABLE SPOT END #############################
    #######################################################################
    aggregated_results = []
    for run in range(repeat):
        logger = lg.Logger()
    
        # log the picked variables
        logger.add_entry_to_dict("params", {})
        logger.add_entry_to_dict("dataset_type", exp_type, ["params"])
        logger.add_entry_to_dict("cs_algo", exp_CS_algo, ["params"])
        logger.add_entry_to_dict("response_variance", resp_var, ["params"])
        logger.add_entry_to_dict("avg_download_time", avg_download_time, ["params"])
        logger.add_entry_to_dict("avg_computation_time", avg_computation_time, ["params"])
        logger.add_entry_to_dict("avg_upload_time", avg_upload_time, ["params"])
        logger.add_entry_to_dict("avg_client_data_update_per_round", avg_data_update, ["params"])
        logger.add_entry_to_dict("learning_rate", learning_rate, ["params"])
        logger.add_entry_to_dict("no_of_rounds", no_of_rounds, ["params"])
        logger.add_entry_to_dict("no_of_picked_clients_per_round", no_of_picked_cln, ["params"])
        logger.add_entry_to_dict("response_time_threshold", threshold, ["params"])
        logger.add_entry_to_dict("total_number_of_clients", total_number_of_clients, ["params"])
    
        print(f"[{exp_type}+{exp_CS_algo}]" .ljust(32), "is starting")
    
        # randomly generate data for clients, and then create the clients
        clients = []
    
        # will be used to generate the response times of the clients
        avg_resp_vals = (resp_var, avg_download_time, avg_computation_time, avg_upload_time)
    
    
        def homo(dev):
            avg_dataset_vals = (avg_data_update, 2, 5, 0, 10, dev)
            for i in range(total_number_of_clients):
                client_name = f"client_{i}"
                clients.append(cl.Client(client_name, exp_CS_algo, cln_init_dataset_size, avg_resp_vals, avg_dataset_vals))
                
        def semi_homo(dev):
            for i in range(total_number_of_clients):
                ratio = i / total_number_of_clients
                slope = None
                constant = None
                
                if ratio<0.2:             # positively skewed clients
                    slope = 2
                    constant = 6
                elif 0.2 <= ratio < 0.4:    # high slope clients
                    slope = 3
                    constant = 5
                elif 0.4 <= ratio < 0.6:    # normal clients
                    slope = 2
                    constant = 5
                elif 0.6 <= ratio < 0.8:   # negatively skewed clients
                    slope = 2
                    constant = 4
                else:               # low slope clients
                    slope = 1
                    constant = 5
                client_name = f"client_{i}"
                avg_dataset_vals = (avg_data_update, slope, constant, 0, 10, dev)
                clients.append(cl.Client(client_name, exp_CS_algo, cln_init_dataset_size, avg_resp_vals, avg_dataset_vals))
        
        def hetero(dev):
            for i in range(total_number_of_clients):
                ratio = i / total_number_of_clients
                slope = None
                constant = None
                if ratio<(1/3):                 # positively skewed clients
                    slope = 2
                    constant = 7
                elif (1/3) <= ratio < (2/3):       # high slope clients
                    slope = 4
                    constant = 5
                else:                   # normal clients
                    slope = 2
                    constant = 5
                client_name = f"client_{i}"
                avg_dataset_vals = (avg_data_update, slope, constant, 0, 10, dev)
                clients.append(cl.Client(client_name, exp_CS_algo, cln_init_dataset_size, avg_resp_vals, avg_dataset_vals))
    
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
            raise KeyError(f"Invalid experiment type {exp_type}")
        
        # create the server
        server = sv.Server(exp_CS_algo, learning_rate, no_of_picked_clients=no_of_picked_cln, threshold=threshold, 
                            logger=logger, dataset_type=exp_type, m_score_weights = m_score_weights)
    
        # add the clients to the server
        for client in clients:
            server.add_client(client, 10)
    
        # train the model
        await server.train_model(no_of_rounds)
        logger.save_logs(f"{exp_CS_algo}_{exp_type}_run{run+1}")
    
        # print that the experiment is finished
        print(f"[{exp_type}+{exp_CS_algo}]" .ljust(32), "finished")
        
    ##JSON result as dict
    aggregated_results.append(logger.get_dict())


if __name__ == "__main__":
    asyncio.run(run_exp())