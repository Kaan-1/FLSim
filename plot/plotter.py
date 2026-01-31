import os
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from fl_simulator.common import CSAlgo
from data.common import DatasetType

def generate_distinct_colors(n):
    """Generate n distinct colors using HSV color space."""
    colors = []
    for i in range(n):
        hue = i / n
        saturation = 0.7
        value = 0.9
        rgb = mcolors.hsv_to_rgb([hue, saturation, value])
        colors.append(rgb)
    return colors

def load_generated_data():
    """Load all pre-generated data files from data/datas directory."""
    current_dir = os.path.dirname(__file__)
    datas_dir = os.path.abspath(os.path.join(current_dir, '..', 'data', 'datas'))
    
    data_files = {}
    if os.path.exists(datas_dir):
        json_files = [f for f in os.listdir(datas_dir) if f.endswith('.json')]
        for file_name in json_files:
            # Extract rep number from filename (e.g., rep_0.json -> 0)
            rep = int(file_name.split('_')[1].split('.')[0])
            file_path = os.path.join(datas_dir, file_name)
            with open(file_path, 'r') as f:
                data_files[rep] = json.load(f)
    
    return data_files

def plot_graphs():

    exp_data_types = list(DatasetType)
    cs_algo_types = list(CSAlgo)

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
    
    # load pre-generated data files
    generated_data = load_generated_data()

    # define the colors of cs algorithms dynamically
    distinct_colors = generate_distinct_colors(len(cs_algo_types))
    cs_algo_colors = {algo.name: distinct_colors[i] for i, algo in enumerate(cs_algo_types)}

    # go through the dict list, get the MSRE plots
    for data_type in exp_data_types:
        x_vals = get_x_vals(dict_list[0])
        results_by_algo_lst = {}
        for algo in list(CSAlgo):
            results_by_algo_lst[algo.name] = {}
        for result_dict in dict_list:
            if result_dict["params"]["dataset_type"] == data_type.name:
                y_vals = get_y_vals(result_dict, validation_dataset)
                algo = result_dict["params"]["cs_algo"]
                rep = result_dict["params"]["rep"]
                results_by_algo_lst[algo][rep] = y_vals
        for algo, rep_dict in results_by_algo_lst.items():
            y_val_sum = np.zeros(len(rep_dict[0]))
            for rep, y_vals in rep_dict.items():
                y_val_sum += np.array(y_vals)
            y_val_avg = y_val_sum / len(rep_dict)
            plt.plot(x_vals, y_val_avg, label=algo, color=cs_algo_colors[algo])
        plt.title(f"Error rates on {data_type.name}")
        plt.xlabel("Rounds")
        plt.ylabel("MRSE")
        plt.legend()
        filepath = os.path.join(output_dir, f"{data_type.name}_error.png")
        plt.savefig(filepath)
        plt.close()

    # go through a subset of dict list, get the time bar graph
    for data_type in exp_data_types:
        x_vals = list(CSAlgo)
        y_vals = []
        for x_val in x_vals:
            total_time = 0
            reps = 0
            for result_dict in dict_list:
                if result_dict["params"]["cs_algo"] == x_val.name and \
                        result_dict["params"]["dataset_type"] == data_type.name:
                    reps += 1
                    rep_num = result_dict["params"]["rep"]
                    dataset_type = result_dict["params"]["dataset_type"]
                    total_time += calculate_total_time(result_dict, x_val, generated_data, rep_num, dataset_type)
            if reps > 0:
                y_vals.append(total_time/reps)
            else:
                y_vals.append(0)
        plt.figure(figsize=(7, 6))
        colors = [cs_algo_colors[algo.name] for algo in x_vals]
        plt.bar([algo.name for algo in x_vals], y_vals, color=colors)
        plt.xticks(rotation=90)
        plt.title(f"Total time of training on {data_type.name}")
        plt.xlabel("CS Algorithms")
        plt.ylabel("Seconds")
        plt.subplots_adjust(bottom=0.3)
        file_path = os.path.join(output_dir, f"{data_type.name}_total_times.png")
        plt.savefig(file_path)
        plt.close()



# time calculation is different for loss vs others
# in loss, the server waits for every client, every round
# others only wait for the picked clients
def calculate_total_time(result_dict, cs_algo, generated_data, rep_num, dataset_type):
    total = 0
    
    # Get the response times from the pre-generated data
    data_for_rep = generated_data.get(rep_num)
    if data_for_rep is None:
        raise ValueError(f"No generated data found for rep {rep_num}")
    
    data_for_dataset = data_for_rep.get(dataset_type)
    if data_for_dataset is None:
        raise ValueError(f"No generated data found for dataset type {dataset_type}")
    
    if cs_algo == CSAlgo.LOSS:
        # get all client's response times
        for round_name, stats in result_dict["results"].items():
            if round_name != "init":
                # Extract round number from round_name (e.g., "round_1" -> 1)
                round_num = int(round_name.split('_')[1]) - 1
                round_key = f'round_{round_num}'
                
                response_times = []
                for client_name in data_for_dataset[round_key]['response_times'].keys():
                    response_times.append(data_for_dataset[round_key]['response_times'][client_name])
                # add the max
                total += max(response_times)
    else:
        for round_name, stats in result_dict["results"].items():
            if round_name != "init":
                # Extract round number from round_name (e.g., "round_1" -> 1)
                round_num = int(round_name.split('_')[1]) - 1
                round_key = f'round_{round_num}'
                
                # get their response times for picked clients only
                response_times = []
                for client_name in result_dict["results"][round_name]["updates"]:
                    response_times.append(data_for_dataset[round_key]['response_times'][client_name])
                # pick the maximum one
                total += max(response_times)
    return total



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
        mrse = calculate_mrse(validation_dataset, global_model["slope"], global_model["constant"])
        y_vals.append(mrse)

    return y_vals



# calculates the MRSE of validation set with respect to the line y=slope*x + constant
def calculate_mrse(validation_dataset, slope, constant):

    x_values = np.array([x for x,y in validation_dataset])
    y_values = np.array([y for x,y in validation_dataset])
    y_pred = slope * x_values + constant

    # Calculate root of each squared error (rather than root of mean)
    root_squared_errors = np.sqrt((y_values-y_pred) ** 2)
    # Take the mean of the root squared errors
    mrse = np.mean(root_squared_errors)

    return mrse