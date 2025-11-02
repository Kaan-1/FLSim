import asyncio
from ..server import Server

class AllBasedServer(Server):
    async def request_updates(self, prev_rounds_updates = None, m_score_weights = None):
        client_updates = {}
        tasks = []
    
        client_list = list(self.client_scores.keys())  #all clients
    
        for client in client_list:
            task = client.get_updates(global_model_slope=self.slope,
                                      global_model_constant=self.constant)
            tasks.append(task)
    
        results = await asyncio.gather(*tasks)
    
        for i, result in enumerate(results):
            client_updates[client_list[i]] = result
    
        return client_updates
    
    def update_client_scores(self, client_updates):
        pass  #no scoring