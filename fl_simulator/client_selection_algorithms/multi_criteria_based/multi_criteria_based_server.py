# implements the request_updates() and update_client_weights() methods of the server wrt multi criteria based algorithm
import asyncio
import math

async def request_updates(server):
    client_updates = {}
    
    # Create tasks for all clients
    tasks = []
    client_list = list(server.client_scores.keys())
    selected_clients = []

    # calculate M scores of clients, pick the top server.no_of_clients one
    client_to_score = {}
    stats = get_stats(client_list)
    for client in client_list:
        client_to_score[client] = calc_m_score(client, stats, server.training_round)
    sorted_clients = sorted(client_to_score.keys(), key=lambda client: client_to_score[client])
    selected_clients = sorted_clients[:min(server.no_of_clients, len(sorted_clients))]
    
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
def calc_m_score(client, stats, training_round):
    down_score = client.download_time / stats[0]
    comp_score = client.computation_time / stats[1]
    up_score = client.upload_time / stats[2]
    data_score = len(client.dataset) / stats[3]
    sample_freshness_score = calc_sample_freshness_score(client.dataset, training_round)
    score = down_score + comp_score + up_score + data_score + sample_freshness_score
    return score



# returns the average values of factors to be used as criterias
def get_stats(client_list):
    avg_down_time = sum(client.download_time for client in client_list) / len(client_list)
    avg_comp_time = sum(client.computation_time for client in client_list) / len(client_list)
    avg_up_time = sum(client.upload_time for client in client_list) / len(client_list)
    avg_dataset_size = sum(len(client.dataset) for client in client_list) / len(client_list)
    return (avg_down_time, avg_comp_time, avg_up_time, avg_dataset_size)


def calc_sample_freshness_score(dataset, training_round):
    sample_freshness = 0
    for data in dataset:
        oldness = training_round - data[2]      # data[2] is the round that the data was added
        freshness_score = math.exp(-oldness)
        sample_freshness += freshness_score
    return sample_freshness