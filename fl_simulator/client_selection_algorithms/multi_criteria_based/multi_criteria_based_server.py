# implements the request_updates() and update_client_weights() methods of the server wrt multi criteria based algorithm
import asyncio
import math

async def request_updates(server, prev_rounds_updates):
    client_updates = {}
    
    # Create tasks for all clients
    tasks = []
    client_list = list(server.client_scores.keys())
    selected_clients = []

    # calculate M scores of clients, pick the top server.no_of_clients one
    client_to_score = {}
    stats = get_stats(client_list, prev_rounds_updates, server.training_round)
    for client in client_list:
        client_to_score[client] = calc_m_score(client, stats, server.training_round, prev_rounds_updates)
    sorted_clients = sorted(client_to_score.keys(), key=lambda client: client_to_score[client], reverse=True)
    selected_clients = sorted_clients[:min(server.no_of_picked_clients, len(sorted_clients))]
    
    # request updates from clients
    for client in selected_clients:
        # Assuming client.get_updates() is an async method that needs current model parameters
        task = client.get_updates(global_model_slope=server.slope,
                                    global_model_constant=server.constant)
        tasks.append(task)
    
    # Wait for all updates to complete
    results = await asyncio.gather(*tasks)
    
    # Map results back to clients
    client_updates = {}
    for i, result in enumerate(results):
        client_updates[selected_clients[i]] = result

    return client_updates



def update_client_scores(server, client_updates):
    pass    # client scores are not used or updated in multi-criteria based CS



# calculates the score of client using multiple criterias
# Criterias: downloading time, training time, uploading time, dataset size, sample freshness
def calc_m_score(client, stats, training_round, prev_rounds_updates):
    down_score = stats[0] / client.download_time
    comp_score = stats[1] / client.computation_time
    up_score = stats[2] / client.upload_time
    data_score = len(client.dataset) / stats[3]
    sample_freshness_score = calc_sample_freshness_score(client.dataset, training_round) / stats[4]

    # Include loss value as a criteria, default to 0.5 if client not picked in prev round
    loss_score = 0.5
    if prev_rounds_updates and client in prev_rounds_updates:
        # Higher loss means the client has more room for improvement
        # We normalize loss by the average loss value
        if stats[4] > 0:  # Prevent division by zero
            loss_score = prev_rounds_updates[client][2] / stats[5]

    score = down_score + comp_score + up_score + data_score + sample_freshness_score + loss_score
    return score



# returns the maximum values of factors to be used for normalization
def get_stats(client_list, prev_rounds_updates, training_round):
    min_down_time = min(client.download_time for client in client_list)
    min_comp_time = min(client.computation_time for client in client_list)
    min_up_time = min(client.upload_time for client in client_list) 
    max_dataset_size = max(len(client.dataset) for client in client_list)
    max_freshness = max(calc_sample_freshness_score(client.dataset, training_round) for client in client_list)

    # calculate the maximum loss
    max_loss = 0
    if prev_rounds_updates:
        losses = [prev_rounds_updates[client][2] for client in client_list if client in prev_rounds_updates]
        if losses:  # Check if list is not empty
            max_loss = max(losses)
    
    return (min_down_time, min_comp_time, min_up_time, max_dataset_size, max_freshness, max_loss)


def calc_sample_freshness_score(dataset, training_round):
    sample_freshness = 0
    for data in dataset:
        oldness = training_round - data[2]      # data[2] is the round that the data was added
        freshness_score = math.exp(-oldness)
        sample_freshness += freshness_score
    return sample_freshness