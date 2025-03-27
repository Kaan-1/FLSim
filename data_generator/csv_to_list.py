import csv
import os

def csv_to_list(csv_name):

    # Get the directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Define the path to the syntetic_data directory relative to this script
    syntetic_data_dir = os.path.join(current_dir, "syntetic_data")

    file_path = os.path.join(syntetic_data_dir, f"{csv_name}.csv")
    result = []
    
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if len(row) == 2:
                result.append((float(row[0]), float(row[1])))
    
    return result