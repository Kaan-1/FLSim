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
from .client_selection_algorithms.loss_value_based import loss_value_based_client as CS_loss
from .client_selection_algorithms.threshold_based import threshold_based_client as CS_threshold
from .client_selection_algorithms.reputation_based import reputation_based_client as CS_reputation
from .client_selection_algorithms.multi_criteria_based import multi_criteria_based_client as CS_multi_criteria

class Client:

    def __init__(self, name, download_time, computation_time,
                    upload_time, CS_algo, dataset):
        self.name = name
        self.download_time = download_time
        self.upload_time = upload_time
        self.computation_time = computation_time
        self.CS_algo = CS_algo
        self.dataset = dataset


    # for debugging purposes
    # only shows client name when using pprint
    def __repr__(self):
        return self.name


    async def get_updates(self, global_model_slope, global_model_constant, threshold = None):

        # imitate downloading the global model
        await asyncio.sleep(self.download_time)

        # imitate computing the local update
        if threshold != None:   # special case for threshold based CS
            if threshold < self.computation_time:
                await asyncio.sleep(threshold)
        else:
            await asyncio.sleep(self.computation_time)
        
        updates = None
        if self.CS_algo == "loss":
            updates = CS_loss.get_updates(self, global_model_slope, global_model_constant)
        elif self.CS_algo == "threshold":
            updates = CS_threshold.get_updates(self, global_model_slope, global_model_constant, threshold)
        elif self.CS_algo == "reputation":
            updates = CS_reputation.get_updates(self, global_model_slope, global_model_constant)
        else:   # self.CS_algo == "multi"
            updates = CS_multi_criteria.get_updates(self, global_model_slope, global_model_constant)

        # imitate uploading the calculated local update
        await asyncio.sleep(self.upload_time)

        return updates
