# implements the get_updates() method of the client wrt to the multi criteria based algorithm
import numpy as np
from ..client import Client

class MultiCriteriaBasedClient(Client):
    def calculate_updates(self, global_model_slope, global_model_constant, threshold = None):
        # Extract x and y from the dataset tuples
        x = np.array([point[0] for point in self.dataset])
        y = np.array([point[1] for point in self.dataset])
        
        # Calculate means
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        
        # Calculate slope using the formula
        numerator = np.sum((x - x_mean) * (y - y_mean))
        denominator = np.sum((x - x_mean) ** 2)
        
        MIN_DENOMINATOR = 1e-3

        # Handle the case where denominator is zero (all x values are the same)
        if denominator < MIN_DENOMINATOR or numerator == 0:
            print("Problem A")
            print(f"denominator: {denominator}")
            print(f"numerator: {numerator}")
        client_slope = float(numerator) / float(denominator)
        
        # Calculate intercept using the formula
        client_constant = y_mean - client_slope * x_mean
        
        # Calculate updates as difference from global model
        slope_update = client_slope - global_model_slope
        constant_update = client_constant - global_model_constant

        # Calculate predictions using the global model
        y_pred_global = global_model_slope * x + global_model_constant
        
        # Calculate Mean Squared Residual Error (MSRE)
        loss_value = np.mean((y - y_pred_global) ** 2)

        # outlier detection
        if abs(slope_update) > 10:
            print("Problem B")
            print(f"slope_update: {slope_update}")

        if abs(constant_update) > 10:
            print("Problem C")
            print(f"constant_update: {constant_update}")

        return (slope_update, constant_update, loss_value)
