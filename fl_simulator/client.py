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

    def __init__(self, download_time, upload_time, computation_time,
                    dataset_size, local_dataset_slope, local_dataset_constant):
        self.download_time = download_time
        self.upload_time = upload_time
        self.computation_time = computation_time
        self.dataset_size = dataset_size
        self.local_dataset_slope = local_dataset_slope
        self.local_dataset_constant = local_dataset_constant
        self.dataset = []

    async def get_updates(self):
        # update dataset
        # TO DO: Client selection algoritmasına göre update etmesi lazım. Loss based ve threshold based'in client kodları farklı çünkü.
