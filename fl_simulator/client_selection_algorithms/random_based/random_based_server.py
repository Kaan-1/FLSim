# picks server.no_of_clients different clients and collects their updates
import asyncio
import random
from ..server import Server

class RandomBasedServer(Server):
    async def request_updates(self, prev_rounds_updates = None, m_score_weights = None):
        client_updates = {}
        
        # Create tasks for all clients
        tasks = []
        client_list = list(self.client_scores.keys())
        random_clients = random.sample(client_list, self.no_of_picked_clients)
        
        for client in random_clients:
            # Assuming client.get_updates() is an async method that needs current model parameters
            task = client.get_updates(global_model_slope=self.slope,
                                        global_model_constant=self.constant)
            tasks.append(task)
        
        # Wait for all updates to complete
        results = await asyncio.gather(*tasks)
        
        # Map results back to clients
        client_updates = {}
        for i, result in enumerate(results):
            client_updates[random_clients[i]] = result

        return client_updates

    def update_client_scores(self, client_updates):
        pass    # client scores are not used or updated in random based CS
