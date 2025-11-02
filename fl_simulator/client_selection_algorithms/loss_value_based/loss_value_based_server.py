# implements the update_client_weight() and request_updates() methods of the server wrt loss value based algorithm
import asyncio
from ..server import Server

class LossValueBasedServer(Server):
    async def request_updates(self, prev_rounds_updates = None, m_score_weights = None):
        client_updates = {}
        
        # Create tasks for all clients
        tasks = []
        client_list = list(self.client_scores.keys())
        
        for client in client_list:
            # Assuming client.get_updates() is an async method that needs current model parameters
            task = client.get_updates(global_model_slope=self.slope,
                                        global_model_constant=self.constant)
            tasks.append(task)
        
        # Wait for all updates to complete
        results = await asyncio.gather(*tasks)
        
        # Map results back to clients
        all_updates = {}
        for i, result in enumerate(results):
            all_updates[client_list[i]] = result
        
        # Sort clients by loss (assuming result contains loss value)
        # Higher loss is better, so we sort in ascending order
        sorted_clients = sorted(all_updates.keys(), 
                            key=lambda client: all_updates[client][2], reverse=True)  # third att of result is loss
        
        # Select only the top server.no_of_clients clients
        selected_clients = sorted_clients[:min(self.no_of_picked_clients, len(sorted_clients))]
        
        # Create the final dictionary with only the selected clients
        for client in selected_clients:
            client_updates[client] = all_updates[client]

        return client_updates

    def update_client_scores(self, client_updates):
        pass    # client scores are not used or updated in loss based CS
