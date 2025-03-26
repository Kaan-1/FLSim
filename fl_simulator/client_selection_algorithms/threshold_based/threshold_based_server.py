# implements the request_updates() and update_client_weights() of the server wrt the threshold based algorithm
import asyncio

async def request_updates_threshold(server):
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
    for i, result in enumerate(results):
        client_updates[client_list[i]] = result

    return client_updates