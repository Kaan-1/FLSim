# This experiment performs FL on homogenous clients
# The line we want to reach is 2x+5
import data_generator.data_from_line as dfl
import data_generator.csv_to_list as ctl
import fl_simulator.server as sv
import fl_simulator.client as cl
import asyncio
import numpy as np
import pprint

async def main():

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
    resp_var = 0.01


    # average download time of clients
    avg_download_time = 0.01


    # average computation time of clients
    avg_computation_time = 0.04


    # average upload time of clients
    avg_upload_time = 0.02


    # Learning rate of the ML algorithm
    learning_rate = 0.1


    # no of rounds to train the model
    no_of_rounds = 10


    # number of clients to be picked each round
    # Redundant for some of the CS algorihms, such as threshold based CS
    # Total number of clients is 15
    no_of_cln = 10


    # Time limit that clients are allowed to compute their updates in
    # Only used in threshold based client selection
    # Have to make it None otherwise, because of the current implementation
    threshold = 0.04
    if exp_CS_algo != "threshold":
        threshold = None



    #######################################################################
    ####################### VARIABLE SPOT END #############################
    #######################################################################

    print(f"Running {exp_type} experiment with client selection algorithm: {exp_CS_algo}")

    # randomly generate data for clients, and then create the clients
    print("Creating clients.")
    clients = []

    # randomly generate response times based on the user response_variance picking
    down_times = []
    comp_times = []
    up_times = []
    for i in range(15):
        # WARNING: If you want to run the experiment fastly, paste the following
            # down_val = abs(np.random.normal(loc=0.001, scale=resp_var*0))
            # comp_val = abs(np.random.normal(loc=0.004, scale=resp_var*0))
            # up_val = abs(np.random.normal(loc=0.002, scale=resp_var*0))
        # If you want to run the experiment normaly, paste the following
            # down_val = abs(np.random.normal(loc=1, scale=resp_var))
            # comp_val = abs(np.random.normal(loc=4, scale=resp_var))
            # up_val = abs(np.random.normal(loc=2, scale=resp_var))
        down_val = abs(np.random.normal(loc=avg_download_time, scale=resp_var))
        comp_val = abs(np.random.normal(loc=avg_computation_time, scale=resp_var))
        up_val = abs(np.random.normal(loc=avg_upload_time, scale=resp_var))
        down_times.append(down_val)
        comp_times.append(comp_val)
        up_times.append(up_val)


    def homo(dev):
        for i in range(15):
            client_name = f"client_{i}"
            dfl.generate_client_data(2, 5, 10, 0, 10, dev, client_name)
            clients.append(cl.Client(name=client_name, download_time=down_times[i], 
                                        computation_time=comp_times[i], upload_time=up_times[i], 
                                        CS_algo = exp_CS_algo, dataset=ctl.csv_to_list(client_name)))
            
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
            dfl.generate_client_data(slope, constant, 10, 0, 10, dev, client_name)
            clients.append(cl.Client(name=client_name, download_time=down_times[i], 
                                        computation_time=comp_times[i], upload_time=up_times[i], 
                                        CS_algo = exp_CS_algo, dataset=ctl.csv_to_list(client_name)))
            
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
            dfl.generate_client_data(slope, constant, 10, 0, 10, dev, client_name)
            clients.append(cl.Client(name=client_name, download_time=down_times[i], 
                                        computation_time=comp_times[i], upload_time=up_times[i], 
                                        CS_algo = exp_CS_algo, dataset=ctl.csv_to_list(client_name)))

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
    server = sv.Server(exp_CS_algo, learning_rate, no_of_clients=no_of_cln, threshold=threshold)

    # add the clients to the server
    for client in clients:
        server.add_client(client, 10)

    # train the model
    await server.train_model(no_of_rounds)
    
    # print model results
    print("Calculated global model slope is: ", server.slope)
    print("Calculated global model constant is: ", server.constant)
    
    pass

if __name__ == "__main__":
    asyncio.run(main())