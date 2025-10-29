import asyncio
import run_experiment
from fl_simulator.common import CSAlgo
from dataset_generator.common import DatasetType
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import plot.plotter as plt


async def run_all_exp():

    exp_data_types = list(DatasetType)
    exp_CS_algos = list(CSAlgo)
    exp_reps = list(range(1))
    
    """
    for rep in exp_reps:
        print("\n==================================================================================================")
        print(f"======================================== REPETITION {rep} ============================================")
        print("==================================================================================================")
        tasks = [
            run_experiment.run_exp(dataset_type=dt, CS_algo=algo, rep=rep)
                for dt in exp_data_types
                for algo in exp_CS_algos
        ]
        await asyncio.gather(*tasks)
        print(f"Repetition {rep} has finished")
    """
    plt.plot_graphs()


if __name__ == "__main__":
    asyncio.run(run_all_exp())