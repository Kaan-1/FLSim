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
from abc import ABC, abstractmethod

class Server(ABC):

    # float slope: slope of the aggregated line model (a of ax+b)
    # float constant: constant of the aggreagated line model (b of ax+b)
    # Dict(Client->int) clients: a dictionary of clients together with their weights
    # int no_of_clients: number of clients to be picked in each iteration 
    def __init__(self, cs_algo_name, learning_rate: float, no_of_picked_clients=None, threshold=None, logger=None, dataset_type=None, m_score_weights = None):
        self.cs_algo_name = cs_algo_name
        self.learning_rate = learning_rate
        self.no_of_picked_clients = no_of_picked_clients
        self.threshold = threshold
        self.client_scores = {}
        self.logger = logger
        self.dataset_type = dataset_type
        self.m_score_weights = m_score_weights
        self.training_round = 0

    def init_model_weights(self):
        self.slope = np.random.normal(0, 0.01)
        self.constant = np.random.normal(0, 0.01)

    async def train_model(self, no_of_rounds):
        self.init_model_weights()
        client_updates = None

        # initialize the log results
        self.logger.add_entry_to_dict("results", {})

        # log the state at the start
        self.log_state("init")

        for i in range(no_of_rounds):
            print(f"[{self.dataset_type.name}+{self.cs_algo_name}]" .ljust(40), f"is on round {i+1}")
            self.training_round = i+1

            self.update_client_scores(client_updates)

            client_updates = await self.request_updates(client_updates, self.m_score_weights)

            self.aggregate_updates(client_updates)

            self.log_state(f"round_{i+1}", client_updates)



    def add_client(self, client_obj, init_weigth):
        self.client_scores[client_obj] = init_weigth



    def remove_client(self, client_name):
        for client in self.client_scores.keys():
            if client.name == client_name:
                del self.client_scores[client]
                break



    # sends current model parameters to clients, waits for their response
    # int s: no of clients to be picked
    @abstractmethod
    async def request_updates(self, prev_rounds_updates = None, m_score_weights = None):
        pass



    # updates the weights of the clients (0=not picked, 1=fully picked)
    @abstractmethod
    def update_client_scores(self, client_updates):
        pass



    def aggregate_updates(self, client_updates):
        # Extract all slope and constant updates from client_updates
        slope_updates = []
        constant_updates = []
        
        if len(client_updates) == 0:
            return

        for _, updates in client_updates.items():
            slope_update, constant_update, *rest = updates  # Third element is loss, which we don't need here
            slope_updates.append(slope_update)
            constant_updates.append(constant_update)
        
        # Calculate the average updates
        avg_slope_update = sum(slope_updates) / len(slope_updates)
        avg_constant_update = sum(constant_updates) / len(constant_updates)
        
        # Apply the updates with learning rate
        self.slope += self.learning_rate * avg_slope_update
        self.constant += self.learning_rate * avg_constant_update


    
    # client updates are used to get the picked clients of the round
    # client_updates defaults to None, to take care of the initialization round, where \
        # clients don't send any data
    # round_name is usually one of init, round_1, round_2 etc...
    # logger.add_entry_to_dict(, , ["results", round_name])
    def log_state(self, round_name, client_updates = None):
        self.logger.add_entry_to_dict(round_name, {}, ["results"])
        self.logger.add_entry_to_dict("updates", {}, ["results", round_name])
        if (client_updates != None):
            for client, update in client_updates.items():
                self.logger.add_entry_to_dict(client.name, update, ["results", round_name, "updates"])
        
        self.logger.add_entry_to_dict("scores", {}, ["results", round_name])
        for client, score in self.client_scores.items():
            self.logger.add_entry_to_dict(client.name, score, ["results", round_name, "scores"])

        self.logger.add_entry_to_dict("global_model", {}, ["results", round_name])
        self.logger.add_entry_to_dict("slope", self.slope, ["results", round_name, "global_model"])
        self.logger.add_entry_to_dict("constant", self.constant, ["results", round_name, "global_model"])