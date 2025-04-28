# This experiment performs FL on 15 clients
# The picked ML model is 2D linear regression
# The line we want to reach is 2x+5

# SET THE SEED OF THE EXPERIMENT HERE
seed = 2

import random
import numpy
random.seed(seed)
numpy.random.seed(seed)

import fl_simulator.server as sv
import fl_simulator.client as cl
import asyncio
import pprint
import logger

async def main():

    # reset the logs to get ready to log new stuff :)
    logger.reset_logs()

    #######################################################################
    ####################### VARIABLE SPOT START ###########################
    #######################################################################



    # experiment seed
    seed = 2

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


    # type of CS algorithm to be tested in the simulation
    # possible values include
        # loss
        # threshold
        # reputation
        # multi
    exp_CS_algo = "multi"


    # variance of response times that the clients will have
    # Recommended values
        # low: 0.25
        # mid: 1
        # high: 5
    resp_var = 0.1


    # average download time of clients
    avg_download_time = 0.1


    # average computation time of clients
    avg_computation_time = 0.4


    # average upload time of clients
    avg_upload_time = 0.2


    # average number of entries to be deleted/added per round for clients
    avg_data_update = 2


    # Learning rate of the ML algorithm
    learning_rate = 0.5


    # no of rounds to train the model
    no_of_rounds = 10


    # number of clients to be picked each round
    # Redundant for some of the CS algorihms, such as threshold based CS
    # Total number of clients is 15
    no_of_cln = 10


    # Time limit that clients are allowed to compute their updates in
    # Only used in threshold based client selection
    # Have to make it None otherwise, because of the current implementation
    threshold = 0.4
    if exp_CS_algo != "threshold":
        threshold = None



    #######################################################################
    ####################### VARIABLE SPOT END #############################
    #######################################################################

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
    logger.add_entry_to_dict("no_of_picked_clients_per_round", no_of_cln, ["params"])
    logger.add_entry_to_dict("response_time_threshold", threshold, ["params"])

    print(f"Running {exp_type} experiment with client selection algorithm: {exp_CS_algo}")

    # randomly generate data for clients, and then create the clients
    print("Creating clients")
    clients = []

    # will be used to generate the response times of the clients
    avg_resp_vals = (resp_var, avg_download_time, avg_computation_time, avg_upload_time)


    def homo(dev):
        avg_dataset_vals = (avg_data_update, 2, 5, 0, 10, dev)
        for i in range(15):
            client_name = f"client_{i}"
            clients.append(cl.Client(client_name, exp_CS_algo, 10, avg_resp_vals, avg_dataset_vals))
            
    def semi_homo(dev):
        for i in range(15):
            slope = None
            constant = None
            if i<3:             # positively skewed clients
                slope = 2
                constant = 6
            elif 3 <= i < 6:    # high slope clients
                slope = 3
                constant = 5
            elif 6 <= i < 9:    # normal clients
                slope = 2
                constant = 5
            elif 9 <= i < 12:   # negatively skewed clients
                slope = 2
                constant = 4
            else:               # low slope clients
                slope = 1
                constant = 5
            client_name = f"client_{i}"
            avg_dataset_vals = (avg_data_update, slope, constant, 0, 10, dev)
            clients.append(cl.Client(client_name, exp_CS_algo, 10, avg_resp_vals, avg_dataset_vals))
            
    def hetero(dev):
        for i in range(15):
            slope = None
            constant = None
            if i<5:                 # positively skewed clients
                slope = 2
                constant = 7
            elif 5 <= i < 10:       # high slope clients
                slope = 4
                constant = 5
            else:                   # normal clients
                slope = 2
                constant = 5
            client_name = f"client_{i}"
            avg_dataset_vals = (avg_data_update, slope, constant, 0, 10, dev)
            clients.append(cl.Client(client_name, exp_CS_algo, 10, avg_resp_vals, avg_dataset_vals))

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
    
    # create the server
    print("Creating the server")
    server = sv.Server(exp_CS_algo, learning_rate, no_of_clients=no_of_cln, threshold=threshold)

    # add the clients to the server
    print("Adding the clients to the server")
    for client in clients:
        server.add_client(client, 10)

    # train the model
    print(f"Training the model for {no_of_rounds} rounds with learning rate {learning_rate}\n")
    await server.train_model(no_of_rounds)
    logger.save_logs()

    # print model results
    print("Calculated global model slope is: ", server.slope)
    print("Calculated global model constant is: ", server.constant)



if __name__ == "__main__":
    asyncio.run(main())