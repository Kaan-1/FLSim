# implements the update_client_weight() and request_updates() methods of the server wrt loss value based algorithm
import asyncio

async def request_updates_loss(server, s: int):
    client_updates = {}
    # Create tasks for all clients
    tasks = []
    client_list = list(server.clients.keys())
    
    for client in client_list:
        # Assuming client.get_updates() is an async method that needs current model parameters
        task = client.get_updates(slope=server.slope, constant=server.constant)
        tasks.append(task)
    
    # Wait for all updates to complete
    results = await asyncio.gather(*tasks)
    
    # Map results back to clients
    all_updates = {}
    for i, result in enumerate(results):
        all_updates[client_list[i]] = result
    
    # Sort clients by loss (assuming result contains loss value)
    # Lower loss is better, so we sort in ascending order
    sorted_clients = sorted(all_updates.keys(), 
                        key=lambda client: all_updates[client].get('loss', float('inf')))
    
    # Select only the top s clients
    selected_clients = sorted_clients[:min(s, len(sorted_clients))]
    
    # Create the final dictionary with only the selected clients
    for client in selected_clients:
        client_updates[client] = all_updates[client]

    return client_updates