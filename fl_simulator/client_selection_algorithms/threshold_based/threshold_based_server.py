# implements the request_updates() and update_client_weights() of the server wrt the threshold based algorithm
import asyncio
from ..server import Server

class ThresholdBasedServer(Server):
    # int threshold: the time allowed for clients to calculate their updates
    async def request_updates(self, prev_rounds_updates = None, m_score_weights = None):
        client_updates = {}
        
        # Create tasks for all clients
        tasks = []
        client_list = list(self.client_scores.keys())
        
        for client in client_list:
            # Assuming client.get_updates() is an async method that needs current model parameters
            task = client.get_updates(global_model_slope=self.slope,
                                        global_model_constant=self.constant,
                                        threshold=self.threshold)
            tasks.append(task)

        # Wait for all updates to complete
        results = await asyncio.gather(*tasks)

        # Map results back to clients
        for i, result in enumerate(results):
            if result != False:     # clients return false if they can't reach the deadline
                client_updates[client_list[i]] = result

        return client_updates

    def update_client_scores(self, client_updates):
        pass    # client scores are not used or updated in threshold based CS
