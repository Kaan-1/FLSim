# This experiment performs FL on homogenous clients
# The line we want to reach is 2x+5
import data_generator.data_from_line as dfl
import data_generator.csv_to_list as ctl
import fl_simulator.server as sv
import fl_simulator.client as cl
import asyncio
import numpy as np
import argparse

async def main():

    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Run federated learning experiment')
    parser.add_argument('response_variance', nargs='?', default="low",
                        choices=["low", "medium", "high"],
                        help='Type of experiment to run (homogeneous, heterogeneous, malicious)')
    parser.add_argument('experiment_type', nargs='?', default="homogeneous",
                        choices=["homo_low_dev", "homo_high_dev", "semi_homo_low_dev",
                                    "semi_homo_high_dev", "hetero_low_dev", "hetero_high_dev"],
                        help='Type of experiment to run (homogeneous, heterogeneous, malicious)')
    parser.add_argument('cs_algo', nargs='?', default="loss", 
                        choices=["loss", "threshold", "reputation", "multi"],
                        help='Client selection algorithm (loss, threshold, reputation, multi)')
    args = parser.parse_args()
    
    exp_type = args.experiment_type
    exp_CS_algo = args.cs_algo
    exp_resp_var = args.response_variance
    print(f"Running {exp_type} experiment with client selection algorithm: {exp_CS_algo}")

    # randomly generate data for clients, and then create the clients
    print("Creating clients.")
    clients = []
    if exp_resp_var == "low":
        resp_var = 0.5
    elif exp_resp_var == "medium":
        resp_var = 2
    elif exp_resp_var == "high":
        resp_var = 5

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
        down_val = abs(np.random.normal(loc=0.001, scale=resp_var*0))
        comp_val = abs(np.random.normal(loc=0.004, scale=resp_var))
        up_val = abs(np.random.normal(loc=0.002, scale=resp_var*0))
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
    server = sv.Server(exp_CS_algo, 0.1, no_of_clients=10, threshold=0.04)

    # add the clients to the server
    for client in clients:
        server.add_client(client, 1)

    # train the model
    await server.train_model(100)
    
    # print model results
    print("Calculated global model slope is: ", server.slope)
    print("Calculated global model constant is: ", server.constant)
    
    pass

if __name__ == "__main__":
    asyncio.run(main())