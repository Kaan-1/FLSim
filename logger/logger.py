import os
import json
import copy

class Logger:
    def __init__(self):
        self.logs = {}

    def add_entry_to_dict(self, key, val, entry_path=[]):
        dic = self.get_nested_object(self.logs, entry_path)
        dic[key] = copy.deepcopy(val)

    def save_logs(self, file_name):
        results_dir = os.path.join(os.path.dirname(__file__), "results")
        os.makedirs(results_dir, exist_ok=True)
        file_path = os.path.join(results_dir, f"{file_name}.json")
        with open(file_path, 'w') as file:
            json.dump(self.logs, file, indent=4)

    def get_nested_object(self, dictionary, path):
        result = dictionary
        try:
            for key in path:
                result = result[key]
            return result
        except Exception:
            raise KeyError(f"couldn't find the nested object located at: {path}")
            
    def get_dict(self):
        return self.logs