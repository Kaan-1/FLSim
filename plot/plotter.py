import os
import json
import numpy as np
import matplotlib.pyplot as plt

def plot_graphs():

    exp_data_types = ["homo_low_dev", "homo_high_dev",
                        "semi_homo_low_dev", "semi_homo_high_dev",
                        "hetero_low_dev", "hetero_high_dev"]

    validation_dataset = create_val_dataset()

    # create a directory for storing the plots in, if it doesn't exist
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    # get the experiment results, names
    current_dir = os.path.dirname(__file__)
    results_dir = os.path.abspath(os.path.join(current_dir, '..', 'logger', 'results'))
    json_files = [f_name for f_name in os.listdir(results_dir) if f_name.endswith('.json')]

    # turn the json files into a list of dictionaries
    dict_list = []
    for file_name in json_files:
        file_path = os.path.join(results_dir, file_name)
        with open(file_path, 'r') as f:
            data = json.load(f)
            dict_list.append(data)

    # go through the dict list, get the MSRE plots
    for data_type in exp_data_types:
        x_vals = get_x_vals(dict_list[0])
        for result_dict in dict_list:
            if result_dict["params"]["dataset_type"] == data_type:
                y_vals = get_y_vals(result_dict, validation_dataset)
                plt.plot(x_vals, y_vals, label=result_dict["params"]["cs_algo"])
        plt.title(f"Error rates on {data_type}")
        plt.xlabel("Rounds")
        plt.ylabel("MRSE")
        plt.legend()
        filepath = os.path.join(output_dir, f"{data_type}_error.png")
        plt.savefig(filepath)
        plt.close()



# creates and returns a syntetic validation dataset, consisting of points around the 2x+5 line
def create_val_dataset():
    dataset = []
    x_vals = np.random.uniform(0, 10, 100)
    for x_val in x_vals:
        y_val = (2 * x_val) + 5
        error = np.random.normal(loc=0, scale = 0.01)
        dataset.append([x_val, y_val+error])
    return dataset



def get_x_vals(result_dict):
    no_of_rounds = len(result_dict["results"]) - 1      # discard the init round
    return range(1, no_of_rounds+1)



def get_y_vals(result_dict, validation_dataset):

    # get all the global models
    global_models = []
    for round_name, stats in result_dict["results"].items():
        if round_name != "init":
            global_model = result_dict["results"][round_name]["global_model"]
            global_models.append(global_model)
    
    # find out the MRSE for each one of them
    y_vals = []
    for global_model in global_models:
        rmse = calculate_rmse(validation_dataset, global_model["slope"], global_model["constant"])
        y_vals.append(rmse)

    return y_vals



# calculates the RMSE of validation set with respect to the line y=slope*x + constant
def calculate_rmse(validation_dataset, slope, constant):

    x_values = np.array([x for x,y in validation_dataset])
    y_values = np.array([y for x,y in validation_dataset])
    y_pred = slope * x_values + constant

    squared_errors = (y_values-y_pred) ** 2
    mse = np.mean(squared_errors)
    rmse = np.sqrt(mse)

    return rmse