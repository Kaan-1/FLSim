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
import numpy as np
import random
from .client_selection_algorithms.loss_value_based import loss_value_based_client as CS_loss
from .client_selection_algorithms.threshold_based import threshold_based_client as CS_threshold
from .client_selection_algorithms.reputation_based import reputation_based_client as CS_reputation
from .client_selection_algorithms.multi_criteria_based import multi_criteria_based_client as CS_multi_criteria

class Client:

    # The attributes of clients get updated every round
    def __init__(self, name, CS_algo, init_dataset_size, avg_resp_vals, avg_data_vals):
        self.name = name
        self.download_time = None
        self.upload_time = None
        self.computation_time = None
        self.CS_algo = CS_algo
        self.dataset = []

        # tuple avg_resp_vals: contains the average values of the fields corresponding to responding
        # needed since client response values get updated every round
        # avg_att_vals[0] -> average response deviation
        # avg_att_vals[1] -> average download time
        # avg_att_vals[2] -> average computation time
        # avg_att_vals[3] -> average upload time
        # using avg_resp_vals, create the average response values for this client
        # this way, each client will have different average response values, centered around avg_resp_vals
        # needed for healthy results in the reputation based CS
        self.avg_resp_vals = self.get_modified_avg_resp_vals(avg_resp_vals)

        # avg_data_vals[0] -> average dataset increase/decrease per round
        # avg_data_vals[1] -> average slope
        # avg_data_vals[2] -> average constant
        # avg_data_vals[3] -> interval start
        # avg_data_vals[4] -> interval end
        # avg_data_vals[5] -> average error
        self.avg_data_vals = avg_data_vals

        # intialize the dataset
        self.add_to_dataset(init_dataset_size, 0)

        # initialize the fields of the client
        self.update_atts(False)


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


    # updates download_time, upload_time, computation_time and dataset of clients
    def update_atts(self, training_round, change_dataset = True):
        self.download_time = abs(np.random.normal(loc=self.avg_resp_vals[1], 
                                                        scale=self.avg_resp_vals[0]))
        self.computation_time = abs(np.random.normal(loc=self.avg_resp_vals[2], 
                                                        scale=self.avg_resp_vals[0]))
        self.upload_time = abs(np.random.normal(loc=self.avg_resp_vals[3], 
                                                        scale=self.avg_resp_vals[0]))
        if change_dataset:
            no_of_entry_changes = int(round(np.random.normal(loc=0, scale=self.avg_data_vals[0])))
            if no_of_entry_changes > 0:
                self.add_to_dataset(no_of_entry_changes, training_round)
            elif no_of_entry_changes < 0:
                if abs(no_of_entry_changes) < len(self.dataset):     # don't compeletely wipe out the dataset
                    self.remove_from_dataset(abs(no_of_entry_changes))


    # we add the training round as a time stamp to the samples added to the datasets
    # this way, we can measure the sample freshness of clients
    def add_to_dataset(self, num_of_points, training_round):
        interval_len = self.avg_data_vals[4] - self.avg_data_vals[3]
        step_size = interval_len / num_of_points
        step = 0
        for i in range(num_of_points):
            step += step_size
            y_val = (self.avg_data_vals[1] * step) + self.avg_data_vals[2]
            error = np.random.normal(loc=0, scale = self.avg_data_vals[5])
            self.dataset.append([step, y_val+error, training_round])


    def remove_from_dataset(self, no_of_ent_to_remove):
        indices_to_remove = random.sample(range(len(self.dataset)), no_of_ent_to_remove)
        for i in sorted(indices_to_remove, reverse=True):
            self.dataset.pop(i)


    # gets a tuple of size 4
    # randomizes the elements with the indeces 1, 2, 3 wrt to 0
    def get_modified_avg_resp_vals(self, avg_resp_val):
        avg_down_time = np.random.normal(loc=avg_resp_val[1], scale = avg_resp_val[0])
        avg_comp_time = np.random.normal(loc=avg_resp_val[2], scale = avg_resp_val[0])
        avg_up_time = np.random.normal(loc=avg_resp_val[3], scale = avg_resp_val[0])
        return (avg_resp_val[0], avg_down_time, avg_comp_time, avg_up_time)