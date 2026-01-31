# Set the seed for reproducibility
SEED = 2


# When set to true, actually sleeps clients during upload, computation, and download
# Set to false to run the experiment fastly
REALISM = False


# No of times the experiments will be repeated
# We later take the averages of the experiments when creating the plots
TOTAL_REPS = 10


# variance of response times that the clients will have
RESP_VAR = 1


# average download time of clients
AVG_DOWNLOAD_TIME = 1


# average computation time of clients
AVG_COMPUTATION_TIME = 4


# average upload time of clients
AVG_UPLOAD_TIME = 2


# initial dataset size of clients
CLN_INIT_DATASET_SIZE = 100


# average number of entries to be deleted/added per round for clients
AVG_DATA_UPDATE = 10


# Learning rate of the ML algorithm
LEARNING_RATE = 0.1


# no of rounds to train the model
NO_OF_ROUNDS = 50


# total number of clients
NO_OF_CLN = 15


# number of clients to be picked each round
# Redundant for some of the CS algorihms, such as threshold based CS or all based CS
NO_OF_PICKED_CLN = 8


# Time limit that clients are allowed to compute their updates in
# Only used in threshold based client selection
THRESHOLD = AVG_DOWNLOAD_TIME + AVG_COMPUTATION_TIME + AVG_UPLOAD_TIME


# weights of criterias for multi-criteria based CS
DOWNLOAD_TIME_WEIGHT = 0.5
COMPUTATION_TIME_WEIGHT = 0.5
UPLOAD_TIME_WEIGHT = 0.5
DATA_SIZE_WEIGHT = 1
SAMPLE_FRESHNESS_WEIGHT = 1
LOSS_MAGNITUDE_WEIGHT = 5