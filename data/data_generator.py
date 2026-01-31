from .common import DatasetType
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
import numpy as np
import json
import shutil

class DataGenerator:
    
    current_datas: dict[DatasetType, dict] = {}
    current_randomized_resp_vals = {}

    def __init__(self):
        datas_dir = os.path.join(os.path.dirname(__file__), "datas")
        if os.path.exists(datas_dir):
            shutil.rmtree(datas_dir)
        pass


    def generate_datas(self, rep: int):

        np.random.seed(config.SEED * (rep+1))

        self.reset_instance()

        for dataset_type in DatasetType:
            cln_datas = DataGenerator.current_datas[dataset_type]
            for round_no in range(config.NO_OF_ROUNDS):
                cln_datas[f'round_{round_no}'] = {}
                cln_datas[f'round_{round_no}']['datasets'] = {}
                cln_datas[f'round_{round_no}']['download_times'] = {}
                cln_datas[f'round_{round_no}']['computation_times'] = {}
                cln_datas[f'round_{round_no}']['upload_times'] = {}
                cln_datas[f'round_{round_no}']['response_times'] = {}

                for client_no in range(config.NO_OF_CLN):
                    new_dataset = None
                    if (round_no == 0):
                        new_dataset = self.generate_dataset(
                            round_no,
                            cln_datas['all_avg_dataset_vals'][f'client_{client_no}'],
                            dataset = []
                        )
                    else:
                        new_dataset = self.generate_dataset(
                            round_no,
                            cln_datas['all_avg_dataset_vals'][f'client_{client_no}'],
                            cln_datas[f'round_{round_no-1}']['datasets'][f'client_{client_no}'])
                    cln_datas[f'round_{round_no}']['datasets'][f'client_{client_no}'] = new_dataset

        # set the response values of every DatasetType experiments the same
        for client_no in range(config.NO_OF_CLN):
            new_atts = self.get_modified_avg_resp_vals(DataGenerator.current_randomized_resp_vals[f'client_{client_no}'])
            for round_no in range(config.NO_OF_ROUNDS):
                for dataset_type in DatasetType:
                    cln_datas = DataGenerator.current_datas[dataset_type]
                    cln_datas[f'round_{round_no}']['download_times'][f'client_{client_no}'] = new_atts[1]
                    cln_datas[f'round_{round_no}']['computation_times'][f'client_{client_no}'] = new_atts[2]
                    cln_datas[f'round_{round_no}']['upload_times'][f'client_{client_no}'] = new_atts[3]
                    cln_datas[f'round_{round_no}']['response_times'][f'client_{client_no}'] = \
                        new_atts[1] + new_atts[2] + new_atts[3]
                    
        self.save_datas(rep)


    def reset_instance(self):
        DataGenerator.current_datas = {}
        DataGenerator.current_randomized_resp_vals = {}
        for dataset_type in DatasetType:
            DataGenerator.current_datas[dataset_type] = {}
        self.generate_init_avg_atts()
        self.generate_init_avg_datasets()

    def generate_init_avg_atts(self):
        for cln_no in range(config.NO_OF_CLN):
            randomized_resp_vals = self.get_modified_avg_resp_vals((
                config.RESP_VAR,
                config.AVG_DOWNLOAD_TIME,
                config.AVG_COMPUTATION_TIME,
                config.AVG_UPLOAD_TIME))
            DataGenerator.current_randomized_resp_vals[f'client_{cln_no}'] = randomized_resp_vals

    def generate_init_avg_datasets(self):

        def homo(dev):
            return (2, 5, dev)
        
        def semi_homo(dev, cln_no):
            group_size = config.NO_OF_CLN // 5
            slope = None
            constant = None
            if cln_no < group_size:                              # positively skewed clients
                slope = 2
                constant = 7
            elif group_size <= cln_no < 2 * group_size:          # high slope clients
                slope = 3
                constant = 5
            elif 2 * group_size <= cln_no < 3 * group_size:      # normal clients
                slope = 2
                constant = 5
            elif 3 * group_size <= cln_no < 4 * group_size:      # negatively skewed clients
                slope = 2
                constant = 3
            else:                                           # low slope clients
                slope = 1
                constant = 5
            return (slope, constant, dev)
        
        def hetero(dev, cln_no):
            group_size = config.NO_OF_CLN // 3
            slope = None
            constant = None
            if cln_no < group_size:                              # positively skewed clients
                slope = 2
                constant = 7
            elif group_size <= cln_no < 2 * group_size:          # high slope clients
                slope = 4
                constant = 5
            else:                                           # normal clients
                slope = 2
                constant = 5
            return (slope, constant, dev)

        for dataset_type in DatasetType:
            DataGenerator.current_datas[dataset_type]['all_avg_dataset_vals'] = {}
            for cln_no in range(config.NO_OF_CLN):
                avg_dataset_vals = None
                if (dataset_type == DatasetType.HOMO_LOW_DEV):
                    avg_dataset_vals = homo(0.2)
                elif (dataset_type == DatasetType.HOMO_HIGH_DEV):
                    avg_dataset_vals = homo(1)
                elif (dataset_type == DatasetType.SEMI_HOMO_LOW_DEV):
                    avg_dataset_vals = semi_homo(0.2, cln_no)
                elif (dataset_type == DatasetType.SEMI_HOMO_HIGH_DEV):
                    avg_dataset_vals = semi_homo(1, cln_no)
                elif (dataset_type == DatasetType.HETERO_LOW_DEV):
                    avg_dataset_vals = hetero(0.2, cln_no)
                elif (dataset_type == DatasetType.HETERO_HIGH_DEV):
                    avg_dataset_vals = hetero(1, cln_no)
                else:
                    raise Exception(f"Unknown DatasetType: {dataset_type.name}")
                DataGenerator.current_datas[dataset_type]['all_avg_dataset_vals'][f'client_{cln_no}'] = avg_dataset_vals


    
                    

    def save_datas(self, rep: int):
        results_dir = os.path.join(os.path.dirname(__file__), "datas")
        os.makedirs(results_dir, exist_ok=True)
        file_path = os.path.join(results_dir, f"rep_{rep}.json")

        # Convert enum keys to strings for JSON serialization
        # Put randomized_resp_vals first
        serializable_data = {'randomized_resp_vals': DataGenerator.current_randomized_resp_vals}
        for dataset_type, data in DataGenerator.current_datas.items():
            serializable_data[dataset_type.name] = data

        with open(file_path, 'w') as file:
            json.dump(serializable_data, file, indent=4)


    def generate_dataset(self, round_no, avg_data_vals, dataset):
        new_dataset = dataset.copy()
        if (round_no == 0):
            self.add_to_dataset(config.CLN_INIT_DATASET_SIZE, new_dataset, 0, avg_data_vals)
        else:
            no_of_entry_changes = int(round(np.random.normal(loc=0, scale=config.AVG_DATA_UPDATE)))
            if no_of_entry_changes > 0:
                self.add_to_dataset(no_of_entry_changes, new_dataset, round_no, avg_data_vals)
            elif no_of_entry_changes < 0:
                # don't completely wipe out the dataset
                if len(new_dataset) > 3:
                    self.remove_from_dataset(min(abs(no_of_entry_changes), (len(new_dataset)-3)), new_dataset)
        return new_dataset


    # we add the training round as a time stamp to the samples added to the datasets
    # this way, we can measure the sample freshness of clients
    def add_to_dataset(self, num_of_points, dataset, training_round, avg_data_vals):
        x_vals = np.random.uniform(0, 10, num_of_points)
        for x_val in x_vals:
            y_val = (avg_data_vals[0] * x_val) + avg_data_vals[1]
            error = np.random.normal(loc=0, scale = avg_data_vals[2])
            dataset.append([x_val, y_val+error, training_round])


    # removes no_of_ent_to_remove oldest elements from the dataset
    def remove_from_dataset(self, no_of_ent_to_remove, dataset):
        dataset.sort(key=lambda x: x[2])
        for i in range(no_of_ent_to_remove):
            dataset.pop(0)


    # gets a tuple of size 4
    # randomizes the elements with the indeces 1, 2, 3 wrt to 0
    def get_modified_avg_resp_vals(self, avg_resp_val):
        avg_down_time = abs(np.random.normal(loc=avg_resp_val[1], scale = avg_resp_val[0]))
        avg_comp_time = abs(np.random.normal(loc=avg_resp_val[2], scale = avg_resp_val[0]))
        avg_up_time = abs(np.random.normal(loc=avg_resp_val[3], scale = avg_resp_val[0]))
        return (avg_resp_val[0], avg_down_time, avg_comp_time, avg_up_time)
    

if __name__ == "__main__":
    data_gen = DataGenerator()
    data_gen.generate_datas(0)