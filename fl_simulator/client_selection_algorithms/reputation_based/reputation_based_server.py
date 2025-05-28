# implements the request_updates() and update_client_weights() methods of the server wrt the reputation based algorithm
import asyncio
import math

# int threshold: the time allowed for clients to calculate their updates
async def request_updates(server):
    client_updates = {}
    
    # Create tasks for all clients
    tasks = []

    # select the most reputable clients
    # initial value of client scores are 10, they will be picked above 6
    selected_clients = []
    for client, score in server.client_scores.items():
        if score > 6:
            selected_clients.append(client)
    
    for client in selected_clients:
        # Assuming client.get_updates() is an async method that needs current model parameters
        task = client.get_updates(global_model_slope=server.slope,
                                    global_model_constant=server.constant,
                                    threshold=server.threshold)
        tasks.append(task)

    # Wait for all updates to complete
    results = await asyncio.gather(*tasks)

    # Map results back to clients
    for i, result in enumerate(results):
        client_updates[selected_clients[i]] = result

    return client_updates



def update_client_scores(server, client_updates):

    # needed since client_updates is none in the first round and we first update the client scores, then call for local model updates
    if client_updates == None:
        return

    # calculate average client response time and highest deviation from the average
    resp_avg, max_resp_dev = get_resp_time_stats(client_updates)

    # TO DO: calculate average of the client updates and the maximum
    # update_avg, max_update_dev = get_update_stats(client_updates)

    for client, score in server.client_scores.items():

        # if the client falls below the threshold, i.e not being picked, increment it's score
        if score < 7:
            server.client_scores[client] += 1
        elif 7 <= score < 25:
            
            # penalize or reward clients based on avg and max_resp_dev
            diff = resp_avg - client_updates[client][2]
            abs_diff = abs(diff)
            sign = math.copysign(1, diff)
            if 0 <= abs_diff < (max_resp_dev/3):
                server.client_scores[client] += 1 * sign
            elif (max_resp_dev/3) <= abs_diff < ((2*max_resp_dev)/3):
                server.client_scores[client] += 2 * sign
            else:       # ((2*max_resp_dev)/3) <= abs_diff <= max_resp_dev
                server.client_scores[client] += 3 * sign

            # TO DO: calculate the average of the model updates



# returns the average of the response times and the highest deviation from the average
def get_resp_time_stats(client_updates):
    values_list = list(client_updates.values())

    # initialize highest and lowest with the resp time of the first client
    sum=0; highest=values_list[0][2]; lowest=values_list[0][2]

    # find out the initalized values
    for update in values_list:
        resp_time = update[2]
        sum += resp_time
        if resp_time > highest:
            highest = resp_time
        elif resp_time < lowest:
            lowest = resp_time

    # calculate the stats to be returned
    avg = sum / len(client_updates)
    diff_with_highest = abs(avg-highest)
    diff_with_lowest = abs(avg-lowest)
    highest_dev = 0
    if diff_with_highest > diff_with_lowest:
        highest_dev = diff_with_highest
    else:       # diff_with_lowest > diff_with_highest
        highest_dev = diff_with_lowest
    
    return avg, highest_dev


# TO DO: returns the average of the model updates and the highest deviation from the average
def get_update_stats(client_updates):
    pass