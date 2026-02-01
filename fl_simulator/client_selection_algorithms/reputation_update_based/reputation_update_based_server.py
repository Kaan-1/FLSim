# implements the request_updates() and update_client_weights() methods of the server wrt the reputation based algorithm
import asyncio
from ..server import Server

class ReputationUpdateBasedServer(Server):
    # int threshold: the time allowed for clients to calculate their updates
    async def request_updates(self, prev_rounds_updates = None, m_score_weights = None):
        client_updates = {}

        # Create tasks for all clients
        tasks = []

        # select the most reputable clients
        # initial value of client scores are 10, they will be picked above 7
        selected_clients = []
        for client, score in self.client_scores.items():
            if score > 7:
                selected_clients.append(client)

        for client in selected_clients:
            # Assuming client.get_updates() is an async method that needs current model parameters
            task = client.get_updates(global_model_slope=self.slope,
                                      global_model_constant=self.constant,
                                      threshold=self.threshold)
            tasks.append(task)

        # Wait for all updates to complete
        results = await asyncio.gather(*tasks)

        # Map results back to clients
        for i, result in enumerate(results):
            client_updates[selected_clients[i]] = result

        return client_updates

    def update_client_scores(self, client_updates):

        # needed since client_updates is none in the first round and we first update the client scores, then call for local model updates
        if client_updates is None:
            return

        # calculate average client response time and highest deviation from the average
        avg_slope_update, max_slope_update, avg_cons_update, max_cons_update = self.get_update_stats(client_updates)

        for client, score in self.client_scores.items():

            # if the client falls below the threshold, i.e not being picked, increment it's score
            if score <= 7:
                self.client_scores[client] += 0.5
            elif 7 < score < 25:
                slope_diff_normalized = abs(client_updates[client][0] - avg_slope_update) / max_slope_update
                cons_diff_normalized = abs(client_updates[client][1] - avg_cons_update) / max_cons_update
                
                # update score wrt slope difference from the average
                if 0 <= slope_diff_normalized <= 1/3 or max_slope_update < 0.5:
                    self.client_scores[client] += 1
                elif 2/3 <= slope_diff_normalized <= 1:
                    self.client_scores[client] -= 1

                # update score wrt slope difference from the average
                if 0 <= cons_diff_normalized <= 1/3 or max_cons_update < 1:
                    self.client_scores[client] += 1
                elif 2/3 <= cons_diff_normalized <= 1:
                    self.client_scores[client] -= 1

    def get_update_stats(self, client_updates):
        """
        Calculates the average and maximum deviation from the average for both slope and constant updates.
        Args:
            client_updates (dict): {client_id: (slope_update, constant_update), ...}
        Returns:
            avg_slope_update (float)
            max_slope_update (float)
            avg_cons_update (float)
            max_cons_update (float)
        """

        slope_updates = [update[0] for update in client_updates.values()]
        cons_updates = [update[1] for update in client_updates.values()]

        avg_slope_update = sum(slope_updates) / len(slope_updates)
        avg_cons_update = sum(cons_updates) / len(cons_updates)

        max_slope_update = max(abs(s - avg_slope_update) for s in slope_updates)
        max_cons_update = max(abs(c - avg_cons_update) for c in cons_updates)

        return avg_slope_update, max_slope_update, avg_cons_update, max_cons_update
