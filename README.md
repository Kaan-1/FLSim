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

In this simulation, each client has different download time, computation time and upload time, resulting in different repsonse times. Variance of these values must be picked from the CLI.

There are several pretuned experiment datasets for a user to utilize. The datasets are still generated during runtime, but these options effect the parameters of the dataset being generated. Types of datasets, with their explanations, and instructions on how to run an experiment is given below.

- **homo_low_dev**: Syntetic datasets of the clients all follow the same normal distribution, and they all have low individual deviation
- **homo_high_dev**: Syntetic datasets of the clients all follow the same normal distribution, but with deviation high individual deviation
- **semi_homo_low_dev**: Syntetic datasets of clients follow different normal distributions. In particular, some have positively skewed data, and some have negatively skewed data, and some are between. But they all follow low individual deviations, and they average to the true line.
- **semi_homo_high_dev**: Syntetic datasets of clients follow different normal distributions. In particular, some have positively skewed data, and some have negatively skewed data, and some are between. They all follow low individual deviations, but they average to the true line.
- **hetero_low_dev**: Syntetic datasets of clients follow different normal distributions. In particular, some are positively skewed, and some are on the true line. But they follow low individual deviations.
- **hetero_low_dev**: Syntetic datasets of clients follow different normal distributions. In particular, some are positively skewed, and some are on the true line. They follow high individual deviations.

To run an experiment, execute the following command in the FLSim/ directory:

```shell
python run_experiment.py [response_variances] [experiment_type] [client_selection_algorithm]
```

**Valid response_variances values**: low, medium, high

**Valid experiment_type values**: homo_low_dev, homo_high_dev, semi_homo_low_dev, semi_homo_high_dev, hetero_low_dev, hetero_low_dev

**Valid client_selection_algorithm values**: loss, threshold, reputation, multi

**WARNING**: Picking high response_variances and non-homo experiment_type may result in inconsistent experiment result, as clients are attended response times randomly.

## TO DO

**Simulation Framework** ✅

**Client Selection Algorithms**

- Loss Based ✅
- Threshold Based
- Reputation Based
- Multi-criteria Based

**Datasets**

- homo_low_dev ✅
- homo_high_dev ✅
- semi_homo_low_dev ✅
- semi_homo_high_dev ✅
- hetero_low_dev ✅
- hetero_low_dev ✅

**CLI Usability** ✅

**Logging**

**UI**
