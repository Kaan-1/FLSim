# This experiment performs FL on homogenous clients
import data_generator.data_from_line as dfl
import data_generator.csv_to_list as ctl
import fl_simulator.server as sv
import fl_simulator.client as cl

def main():

    exp_CS_algo = "loss"    # possible values are loss, threshold, reputation, multi

    # randomly generate data for clients, and then create the clients
    print("Creating clients.")
    clients = []
    for i in range(1, 16):
        client_name = f"client_{i}"
        dfl.generate_client_data(2, 5, 10, 0, 10, 1, client_name)
        clients.append(cl.Client(name=client_name, download_time=1, 
                                    computation_time=2, upload_time=1, 
                                    CS_algo = exp_CS_algo, dataset=ctl.csv_to_list(client_name)))
    
    # create the server
    server = sv.Server(exp_CS_algo, 0.01)

    # add the clients to the server
    for client in clients:
        server.add_client(client, 1)

    # train the model
    server.train_model(100)
    
    # print model results
    print("Calculated global model slope is: ", server.slope)
    print("Calculated global model constant is: ", server.constant)
    
    pass

if __name__ == "__main__":
    main()