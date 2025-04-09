# FLSim

A tool for simulation and analysis of top FL client selection algorithms.

**WARNING**: This project is in working progress. Public contributions will not be merged since this is a school project, sadly :( You can check out the TO DO list at the bottom to track the current status of the project.

## Simulation Logic

This simulation tries to derive a 2D line using federated learning on 15 clients. We assume that we have are trying to reach a "true" line, and create different syntetic datasets for clients, where some follow this "true" line, and some don't. Clients all have different download, compute and upload time. The following client selection algorithms can be selected in the simulation:

- Loss based client selection
- Threshold based client selection
- Reputation based client selection
- Multi-criteria based client selection

## Experiments

Before running the experiment, you should go into the run_experiment.py file in the root directory, and modify the variables according to your needs. Values that can be modified can be found between "VARIABLE SPOT START" and "VARIABLE SPOT END". The explanation of the possible values for the exp_type variable is given below, since it is not clear from the get go.

There are several pretuned experiment datasets for a user to utilize. The datasets are still generated during runtime, but these options effect the parameters of the dataset being generated. Types of datasets, with their explanations, and instructions on how to run an experiment is given below.

- **homo_low_dev**: Syntetic datasets of the clients all follow the same normal distribution, and they all have low individual deviation
- **homo_high_dev**: Syntetic datasets of the clients all follow the same normal distribution, but with deviation high individual deviation
- **semi_homo_low_dev**: Syntetic datasets of clients follow different normal distributions. In particular, some have positively skewed data, and some have negatively skewed data, and some are between. But they all follow low individual deviations, and they average to the true line.
- **semi_homo_high_dev**: Syntetic datasets of clients follow different normal distributions. In particular, some have positively skewed data, and some have negatively skewed data, and some are between. They all follow high individual deviations, but they average to the true line.
- **hetero_low_dev**: Syntetic datasets of clients follow different normal distributions. In particular, some are positively skewed, and some are on the true line. But they follow low individual deviations.
- **hetero_low_dev**: Syntetic datasets of clients follow different normal distributions. In particular, some are positively skewed, and some are on the true line. They follow high individual deviations.

To run an experiment, simply execute the following command in the FLSim/ directory after modifying the variables:

```shell
python run_experiment.py
```

**WARNING**: Picking high resp_var and non-homo experiment_type may result in inconsistent experiment result, as clients are attended response times randomly.

## TO DO

**Simulation Framework** ✅

**Client Selection Algorithms**✅

- Loss Based ✅
- Threshold Based✅
- Reputation Based✅
- Multi-criteria Based✅

**Datasets**✅

- homo_low_dev ✅
- homo_high_dev ✅
- semi_homo_low_dev ✅
- semi_homo_high_dev ✅
- hetero_low_dev ✅
- hetero_low_dev ✅

**Logging** ✅

**Simulation-time client attribute updates** ✅

**Global seed for randomization**

**Add requirements file**

**UI**


## UPDATE NOTES

CLI usability was implemented, but later reverted because of the difficulty of usability caused by the high number of variables that can be modified.