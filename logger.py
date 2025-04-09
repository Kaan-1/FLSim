# responsible for logging stuff

import os

file_name = os.path.join(os.path.dirname(__file__), "experiment_trace.txt")

def reset_logs():
    with open(file_name, "w") as file:
        file.write("")

def log(log_str: str):
    with open(file_name, "a") as file:
        file.write(log_str + "\n")