# No of times the experiments will be repeated
# We later take the averages of the experiments when creating the plots
TOTAL_REPS = 3


# variance of response times that the clients will have
# Recommended values
# low: 0.25
# mid: 1
# high: 5
RESP_VAR = 0.01


# average download time of clients
AVG_DOWNLOAD_TIME = 0.01


# average computation time of clients
AVG_COMPUTATION_TIME = 0.04


# average upload time of clients
AVG_UPLOAD_TIME = 0.02


# initial dataset size of clients
CLN_INIT_DATASET_SIZE = 100


# average number of entries to be deleted/added per round for clients
AVG_DATA_UPDATE = 10


# Learning rate of the ML algorithm
LEARNING_RATE = 0.1


# no of rounds to train the model
NO_OF_ROUNDS = 50


# number of clients to be picked each round
# Redundant for some of the CS algorihms, such as threshold based CS
# Total number of clients is 15
NO_OF_PICKED_CLN = 8


# Time limit that clients are allowed to compute their updates in
# Only used in threshold based client selection
THRESHOLD = 0.04


# weights of criterias for multi-criteria based CS
DOWNLOAD_TIME_WEIGHT = 1
COMPUTATION_TIME_WEIGHT = 1
UPLOAD_TIME_WEIGHT = 1
DATA_SIZE_WEIGHT = 1
SAMPLE_FRESHNESS_WEIGHT = 1
LOSS_MAGNITUDE_WEIGHT = 10