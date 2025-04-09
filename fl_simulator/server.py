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
import pprint
from .client_selection_algorithms.loss_value_based import loss_value_based_server as CS_loss
from .client_selection_algorithms.threshold_based import threshold_based_server as CS_threshold
from .client_selection_algorithms.reputation_based import reputation_based_server as CS_reputation
from .client_selection_algorithms.multi_criteria_based import multi_criteria_based_server as CS_multi_criteria

# import the logger from one directory above
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import logger

class Server:

    # float slope: slope of the aggregated line model (a of ax+b)
    # float constant: constant of the aggreagated line model (b of ax+b)
    # Dict(Client->int) clients: a dictionary of clients together with their weights
    # int no_of_clients: number of clients to be picked in each iteration 
    def __init__(self, CS_algo: str, learning_rate: float, no_of_clients=None, threshold=None):
        self.CS_algo = CS_algo
        self.learning_rate = learning_rate
        self.no_of_clients = no_of_clients
        self.threshold = threshold
        self.client_scores = {}

    def init_model_weights(self):
        self.slope = np.random.normal(0, 0.01)
        self.constant = np.random.normal(0, 0.01)

    async def train_model(self, no_of_rounds):
        print("Initializing global model weights\n")
        self.init_model_weights()
        client_updates = None

        # log the state at the start
        logger.log("START")
        self.log_state()

        for i in range(no_of_rounds):
            print(f"Training round: {i+1}")

            # tells the clients to update their attributes at the start of each round
            # in the real life setting, the server is not responsible for this
            # done this way to simulate real life
            self.update_client_attributes()

            print("Updating client scores")
            self.update_client_scores(client_updates)

            print("Requesting local updates from clients")
            client_updates = await self.request_updates()

            print("Aggregating the updates\n")
            self.aggregate_updates(client_updates)

            logger.log(f"ROUND {i+1} END")
            self.log_state(client_updates)        # log the state of clients and server at the end of each round

    def add_client(self, client_obj, init_weigth):
        self.client_scores[client_obj] = init_weigth

    def remove_client(self, client_name):
        for client in self.client_scores.keys():
            if client.name == client_name:
                del self.client_scores[client]
                break

    # sends current model parameters to clients, waits for their response
    # int s: no of clients to be picked
    async def request_updates(self):
        client_updates = {}
        if self.CS_algo == "loss":
            client_updates = await CS_loss.request_updates(self)
        elif self.CS_algo == "threshold":
            client_updates = await CS_threshold.request_updates(self)
        elif self.CS_algo == "reputation":
            client_updates = await CS_reputation.request_updates(self)
        else:   # self.CS_algo == "multi"
            client_updates = await CS_multi_criteria.request_updates(self)
        return client_updates


    # updates the weights of the clients (0=not picked, 1=fully picked)
    def update_client_scores(self, client_updates):
        if self.CS_algo == "loss":
            CS_loss.update_client_scores(self, client_updates)
        elif self.CS_algo == "threshold":
            CS_threshold.update_client_scores(self, client_updates)
        elif self.CS_algo == "reputation":
            CS_reputation.update_client_scores(self, client_updates)
        else:   # self.CS_algo == "multi"
            CS_multi_criteria.update_client_scores(self,client_updates)

    def aggregate_updates(self, client_updates):
        # Extract all slope and constant updates from client_updates
        slope_updates = []
        constant_updates = []
        
        if len(client_updates) == 0:
            return

        for client, updates in client_updates.items():
            slope_update, constant_update, *rest = updates  # Third element is loss, which we don't need here
            slope_updates.append(slope_update)
            constant_updates.append(constant_update)
        
        # Calculate the average updates
        avg_slope_update = sum(slope_updates) / len(slope_updates)
        avg_constant_update = sum(constant_updates) / len(constant_updates)
        
        # Apply the updates with learning rate
        self.slope += self.learning_rate * avg_slope_update
        self.constant += self.learning_rate * avg_constant_update


    def update_client_attributes(self):
        for client in list(self.client_scores.keys()):
            client.update_atts()

    
    # client updates are used to get the picked clients of the round
    def log_state(self, client_updates = None):
        if client_updates != None:
            logger.log("\nClient Updates")
            for client, update in client_updates.items():
                logger.log(f"{client.name} update: {update[0]:.3f}, {update[1]:.3f}")
        
        logger.log("\nClient Scores")
        for client, score in self.client_scores.items():
            logger.log(f"{client.name} score: {score}")

        logger.log("\nClient Datasets")
        for client in self.client_scores.keys():
            logger.log(f"{client.name} dataset: {client.dataset}")
        
        logger.log("\nClient Response Times")
        logger.log("Results are given in the format: download_time + computation_time + upload_time = response time")
        for client in self.client_scores.keys():
            logger.log(f"{client.name} response time: {client.download_time:.3f} + {client.computation_time:.3f} + {client.upload_time:.3f} = {(client.download_time+client.computation_time+client.upload_time):.3f}")

        logger.log("\nGlobal Model")
        logger.log(f"Slope: {self.slope}")
        logger.log(f"Constant: {self.constant}")

        logger.log("\n\n\n\n\n")