# Client is able to take in the global model and caldulate the model update wrt to its local dataset
# Clients differ in multiple metrics such as:
    # download time: time it takes to get the global model
    # upload time: time it take to send the model updates calculated locally
    # computation time: time it takes to train the model locally
    # dataset size
    # dataset content
# For almost all of the metrics of the client, I set metric mean and metric deviation as parameters, and plan to take a random from a normal distribution with those values
    #to create a more natural simulation environment. Mantıklı mı emin diilim ama ya
# For every round, the client updates its local dataset diye düşündüm de bilemedim

import asyncio
import time
from .client_selection_algorithms.loss_value_based import loss_value_based_client as CS_loss

class Client:

    def __init__(self, name, download_time, computation_time,
                    upload_time, CS_algo, dataset):
        self.name = name
        self.download_time = download_time
        self.upload_time = upload_time
        self.computation_time = computation_time
        self.CS_algo = CS_algo
        self.dataset = dataset

    async def get_updates(self, global_model_slope, global_model_constant):
        time.sleep(self.download_time)
        time.sleep(self.computation_time)
        updates = None
        if self.CS_algo == "loss":
            updates = CS_loss.get_updates(self, global_model_slope, global_model_constant)
        elif self.CS_algo == "threshold":
            pass    # TO DO
        elif self.CS_algo == "reputation":
            pass    # TO DO
        else:   # self.CS_algo == "multi"
            pass    # TO DO
        time.sleep(self.upload_time)
        return updates
