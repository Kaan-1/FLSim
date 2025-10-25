import asyncio

async def request_updates(server):
    client_updates = {}
    tasks = []

    client_list = list(server.client_scores.keys())  #all clients

    for client in client_list:
        task = client.get_updates(global_model_slope=server.slope,
                                  global_model_constant=server.constant)
        tasks.append(task)

    results = await asyncio.gather(*tasks)

    for i, result in enumerate(results):
        client_updates[client_list[i]] = result

    return client_updates

def update_client_scores(server, client_updates):
    pass  #no scoring