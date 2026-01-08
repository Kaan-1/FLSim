import asyncio
import run_experiment
from fl_simulator.common import CSAlgo
from dataset.common import DatasetType
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import plot.plotter as plt
import config

async def run_all_exp():
    exp_data_types = list(DatasetType)
    exp_CS_algos = list(CSAlgo)
    exp_reps = list(range(config.TOTAL_REPS))
    
    for rep in exp_reps:
        print("\n==================================================================================================")
        print(f"======================================== REPETITION {rep} ============================================")
        print("==================================================================================================")
        tasks = [
            run_experiment.run_exp(dataset_type=dt, CS_algo=algo, rep=rep,
                                   resp_var=config.RESP_VAR,
                                   avg_download_time=config.AVG_DOWNLOAD_TIME,
                                   avg_computation_time=config.AVG_COMPUTATION_TIME,
                                   avg_upload_time=config.AVG_UPLOAD_TIME,
                                   cln_init_dataset_size=config.CLN_INIT_DATASET_SIZE,
                                   avg_data_update=config.AVG_DATA_UPDATE,
                                   learning_rate=config.LEARNING_RATE,
                                   no_of_rounds=config.NO_OF_ROUNDS,
                                   no_of_picked_cln=config.NO_OF_PICKED_CLN,
                                   threshold=config.THRESHOLD,
                                   download_time_weight=config.DOWNLOAD_TIME_WEIGHT,
                                   computation_time_weight=config.COMPUTATION_TIME_WEIGHT,
                                   upload_time_weight=config.UPLOAD_TIME_WEIGHT,
                                   data_size_weight=config.DATA_SIZE_WEIGHT,
                                   sample_freshness_weight=config.SAMPLE_FRESHNESS_WEIGHT,
                                   loss_magnitude_weight=config.LOSS_MAGNITUDE_WEIGHT)
                for dt in exp_data_types
                for algo in exp_CS_algos
        ]
        await asyncio.gather(*tasks)
        print(f"Repetition {rep} has finished")
    
    plt.plot_graphs()


if __name__ == "__main__":
    asyncio.run(run_all_exp())