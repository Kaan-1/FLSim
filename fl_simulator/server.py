# defines the server object

# keeps model weights
# can initialize the model weights
# keeps a list of the clients, together with their weights, can add or remove clients from the list
    # I think we shoudl keep weights because it also includes the binary case using weights 0 and 1 (picking or not picking a client)
# can send the weights to clients
# can wait for the updates from the clients
# has its own test data set, under the syntetic_data folder
# upon receiving the updates, can send them to the client selection algorithms, to update the weights of the clients
# also, upon receiving the updates, can aggregate them with respect to client's weights

import numpy as np
import asyncio

class Server:

    # float slope: slope of the aggregated line model (a of ax+b)
    # float constant: constant of the aggreagated line model (b of ax+b)
    # Dict(Client->int) clients: a dictionary of clients together with their weights
    def __init__(self, slope, constant):
        self.slope = slope
        self.constant = constant
        self.clients = {}

    def train_model(self, no_of_rounds):
        init_model_weights()
        model_updates = None
        for i in range(no_of_rounds):
            update_client_weights(model_updates)
            model_updates = request_updates()
            aggregate_model_updates(model_updates)

    def init_model_weights(self):
        self.slope = np.random.normal(0, 0.01)
        self.constant = np.random.normal(0, 0.01)

    def add_client(self, client_obj, init_weigth):
        self.clients[client_obj] = init_weight

    def remove_client(self, client_name):
        for client in self.clients.keys():
            if client.name == client_name:
                del self.clients[client]
                break

    # sends current model parameters to clients, waits for their response
    def request_updates(self):
        # TO DO: implement this in client selection algorithms and call it from here
        return 0

    # updates the weights of the clients (0=not picked, 1=fully picked)
    def update_client_weights(self):
        # TO DO: implement this in client selection algorithms and call it from here
        return 0

    def aggreagate_updates(self):
        # TO DO: We can just take the average of the updates maybe
        return 0

