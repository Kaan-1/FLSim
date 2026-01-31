import asyncio
import run_experiment
from fl_simulator.common import CSAlgo
from data.common import DatasetType
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import plot.plotter as plt
import config
import logger.logger as lg
from data.data_generator import DataGenerator

async def run_all_exp():
    exp_data_types = list(DatasetType)
    exp_CS_algos = list(CSAlgo)
    exp_reps = list(range(config.TOTAL_REPS))
    
    lg.Logger.clear_results()
    data_generator = DataGenerator()
    
    for rep in exp_reps:
        print("Generating client datas...")
        data_generator.generate_datas(rep)
        print("Successfully generated datas!")

        print("\n==================================================================================================")
        print(f"======================================== REPETITION {rep} ============================================")
        print("==================================================================================================")
        tasks = [
            run_experiment.run_exp(dataset_type=dt, CS_algo=algo, rep=rep,
                                   learning_rate=config.LEARNING_RATE,
                                   no_of_rounds=config.NO_OF_ROUNDS,
                                   no_of_cln=config.NO_OF_CLN,
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
    
    
    print("Plotting the results. This may take a minute...")
    plt.plot_graphs()
    print("Successfully plotted the results!")
    print("You can find the plots under 'plot/outputs/'")


if __name__ == "__main__":
    asyncio.run(run_all_exp())