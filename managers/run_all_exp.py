import asyncio
import run_experiment
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import plot.plotter as plt


async def run_all_exp():

    exp_data_types = ["homo_low_dev", "homo_high_dev",
                        "semi_homo_low_dev", "semi_homo_high_dev",
                        "hetero_low_dev", "hetero_high_dev"]
    exp_CS_algos = ["loss", "threshold", "reputation", "multi", "random","all"]

    tasks = [
        run_experiment.run_exp(experiment_type=dt, experiment_CS_algo=algo, total_number_of_clients=100)
            for dt in exp_data_types
            for algo in exp_CS_algos
    ]
    await asyncio.gather(*tasks)

    plt.plot_graphs()


if __name__ == "__main__":
    asyncio.run(run_all_exp())