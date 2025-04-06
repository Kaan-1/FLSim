# implements the get_updates() method of the client wrt to the multi criteria based algorithm
import numpy as np

def get_updates(client, global_model_slope, global_model_constant):
    # Extract x and y from the dataset tuples
    x = np.array([point[0] for point in client.dataset])
    y = np.array([point[1] for point in client.dataset])
    
    # Calculate means
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    
    # Calculate slope using the formula
    numerator = np.sum((x - x_mean) * (y - y_mean))
    denominator = np.sum((x - x_mean) ** 2)
    
    # Handle the case where denominator is zero (all x values are the same)
    if denominator == 0:
        client_slope = 0
    else:
        client_slope = numerator / denominator
    
    # Calculate intercept using the formula
    client_constant = y_mean - client_slope * x_mean
    
    # Calculate updates as difference from global model
    slope_update = client_slope - global_model_slope
    constant_update = client_constant - global_model_constant

    return (slope_update, constant_update)