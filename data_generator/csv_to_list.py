import csv
import os

def csv_to_list(csv_name):
    file_path = os.path.join('syntetic_data', csv_name)
    result = []
    
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if len(row) == 2:
                result.append((float(row[0]), float(row[1])))
    
    return result