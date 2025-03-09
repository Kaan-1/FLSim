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

class Client:

    def __init__(self, download_time_mean, download time_dev,
                    upload_time_mean, upload_time_dev,
                    computation_time_mean, computation_time_dev,
                    dataset_size_mean, dataset_size_dev,
                    local_dataset_slope_mean, local_dataset_slope_dev,
                    local_dataset_constant_mean, local_dataset_constant_dev):
        self.download_time_mean = download_time_mean
        self.download_time_dev = download_time_dev
        self.upload_time_mean = upload_time_mean
        self.upload_time_dev = upload_time_dev
        self.computation_time_mean = computation_time_mean
        self.computation_time_dev = computation_time_dev
        self.dataset_size_mean = dataset_size_mean
        self.dataset_size_dev = dataset_size_dev
        self.local_dataset_slope_mean = local_dataset_slope_mean
        self.local_dataset_slope_dev = local_dataset_slope_dev
        self.local_dataset_constant_mean = local_dataset_constant_mean
        self.local_dataset_constant_dev = local_dataset_constant_dev
        self.dataset = []

    async def get_updates(self)
        # update dataset
        # TO DO: Client selection algoritmasına göre update etmesi lazım. Loss based ve threshold based'in client kodları farklı çünkü.
