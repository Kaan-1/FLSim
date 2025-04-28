# responsible for logging stuff in json format
import os
import json
import copy


file_name = os.path.join(os.path.dirname(__file__), "experiment_trace.json")
logs = {}


def reset_logs():
    with open(file_name, "w") as file:
        file.write("")



def add_entry_to_dict(key, val, entry_path=[]):
    dic = get_nested_object(logs, entry_path)
    dic[key] = copy.deepcopy(val)



def save_logs():
    with open(file_name, 'w') as file:
        json.dump(logs, file, indent=4)



def get_nested_object(dictionary, path):
    result = dictionary
    try:
        for key in path:
            result = result[key]
        return result
    except:
        KeyError(f"couldn't find the nested object located at: {path}")