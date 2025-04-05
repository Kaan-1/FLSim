# implements the request_updates() and update_client_weights() of the server wrt the threshold based algorithm
import asyncio

# int threshold: the time allowed for clients to calculate their updates
async def request_updates(server):
    client_updates = {}
    
    # Create tasks for all clients
    tasks = []
    client_list = list(server.client_weights.keys())
    
    for client in client_list:
        # Assuming client.get_updates() is an async method that needs current model parameters
        task = client.get_updates(global_model_slope=server.slope,
                                    global_model_constant=server.constant,
                                    threshold=server.threshold)
        tasks.append(task)

    # Wait for all updates to complete
    results = await asyncio.gather(*tasks)

    # Map results back to clients
    for i, result in enumerate(results):
        if result != False:     # clients return false if they can't reach the deadline
            client_updates[client_list[i]] = result

    # print selected client names
    selected_client_names = []
    for client in client_updates.keys():
        selected_client_names.append(client.name)
    print("Selected clients are:", selected_client_names)

    return client_updates



def update_client_weights(server, client_updates):
    pass    # client weights are not used or updated in loss based CS