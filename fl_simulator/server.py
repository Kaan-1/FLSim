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
import client_selection_algorithms.loss_value_based.loss_value_based_server as CS_loss

class Server:

    # float slope: slope of the aggregated line model (a of ax+b)
    # float constant: constant of the aggreagated line model (b of ax+b)
    # Dict(Client->int) clients: a dictionary of clients together with their weights
    def __init__(self, CS_algo):
        self.CL_algo = CS_algo
        self.clients = {}

    def init_model_weights(self):
        self.slope = np.random.normal(0, 0.01)
        self.constant = np.random.normal(0, 0.01)

    async def train_model(self, no_of_rounds):
        self.init_model_weights()
        client_updates = None
        for i in range(no_of_rounds):
            update_client_weights(client_updates)
            client_updates = await self.request_updates()
            aggregate_model_updates(client_updates)

    def add_client(self, client_obj, init_weigth):
        self.clients[client_obj] = init_weigth

    def remove_client(self, client_name):
        for client in self.clients.keys():
            if client.name == client_name:
                del self.clients[client]
                break

    # sends current model parameters to clients, waits for their response
    # int s: no of clients to be picked
    async def request_updates(self, s: int):
        client_updates = {}
        if self.CS_algo == "loss":
            client_updates = await CS_loss.request_updates_loss(self, s)
        elif self.CS_algo == "threshold":
            pass
        elif self.CS_algo == "reputation":
            pass
        else:   # self.CS_algo == "multi"
            pass
        return client_updates


    # updates the weights of the clients (0=not picked, 1=fully picked)
    def update_client_weights(self):
        # TO DO: implement this in client selection algorithms and call it from here
        return 0

    def aggreagate_updates(self):
        # TO DO: We can just take the average of the updates maybe
        return 0

