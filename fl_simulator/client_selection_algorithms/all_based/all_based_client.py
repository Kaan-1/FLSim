import numpy as np
from ..client import Client

class AllBasedClient(Client):
    def calculate_updates(self, global_model_slope, global_model_constant, threshold = None):
        x = np.array([point[0] for point in self.dataset])
        y = np.array([point[1] for point in self.dataset])
    
        x_mean = np.mean(x)
        y_mean = np.mean(y)
    
        numerator = np.sum((x - x_mean) * (y - y_mean))
        denominator = np.sum((x - x_mean) ** 2)
    
        MIN_DENOMINATOR = 1e-3
    
        if denominator < MIN_DENOMINATOR or numerator == 0:
            print("Problem A")
            print(f"denominator: {denominator}")
            print(f"numerator: {numerator}")
            client_slope = MIN_DENOMINATOR
        else:
            client_slope = float(numerator) / float(denominator)
    
        client_constant = y_mean - client_slope * x_mean
    
        slope_update = client_slope - global_model_slope
        constant_update = client_constant - global_model_constant
    
        if abs(slope_update) > 10:
            print("Problem B")
            print(f"slope_update: {slope_update}")
            slope_update = MIN_DENOMINATOR
        if abs(constant_update) > 10:
            print("Problem C")
            print(f"constant_update: {constant_update}")
            constant_update = MIN_DENOMINATOR
    
        return (slope_update, constant_update)