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
from abc import ABC, abstractmethod
from data.common import DatasetType
from data.data_generator import DataGenerator
import config


class Client(ABC):

    # The attributes of clients get updated every round
    def __init__(self, dataset_type: DatasetType, name):
        self.name = name
        self.download_time = None
        self.upload_time = None
        self.computation_time = None
        self.dataset = []

        # initialize the fields of the client
        self.update_datas(0, dataset_type, name)


    # for debugging purposes
    # only shows client name when using pprint
    def __repr__(self):
        return self.name


    async def get_updates(self, global_model_slope, global_model_constant, threshold = None):

        # imitate downloading the global model
        if config.REALISM: await asyncio.sleep(self.download_time)

        # imitate computing the local update
        if threshold != None:   # special case for threshold based CS
            if threshold < self.computation_time:
                if config.REALISM: await asyncio.sleep(threshold)
            else:
                if config.REALISM: await asyncio.sleep(self.computation_time)
        else:
            if config.REALISM: await asyncio.sleep(self.computation_time)
        
        updates = self.calculate_updates(global_model_slope, global_model_constant, threshold)

        # imitate uploading the calculated local update
        if config.REALISM: await asyncio.sleep(self.upload_time)

        return updates
    
    
    @abstractmethod
    def calculate_updates(self, global_model_slope, global_model_constant, threshold = None):
        pass


    # updates download_time, upload_time, computation_time and dataset of clients
    def update_datas(self, training_round, dataset_type, client_name):
        self.download_time = DataGenerator.current_datas[dataset_type][f'round_{training_round}']['download_times'][client_name]
        self.computation_time = DataGenerator.current_datas[dataset_type][f'round_{training_round}']['computation_times'][client_name]
        self.upload_time = DataGenerator.current_datas[dataset_type][f'round_{training_round}']['upload_times'][client_name]
        self.dataset = DataGenerator.current_datas[dataset_type][f'round_{training_round}']['datasets'][client_name]