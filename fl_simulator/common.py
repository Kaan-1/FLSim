from enum import Enum
from typing import NamedTuple, Type

from .client_selection_algorithms.server import Server
from .client_selection_algorithms.all_based.all_based_server import AllBasedServer
from .client_selection_algorithms.loss_value_based.loss_value_based_server import LossValueBasedServer
from .client_selection_algorithms.threshold_based.threshold_based_server import ThresholdBasedServer
from .client_selection_algorithms.reputation_time_based.reputation_time_based_server import ReputationTimeBasedServer
from .client_selection_algorithms.multi_criteria_based.multi_criteria_based_server import MultiCriteriaBasedServer
from .client_selection_algorithms.random_based.random_based_server import RandomBasedServer
from .client_selection_algorithms.reputation_update_based.reputation_update_based_server import ReputationUpdateBasedServer

from .client_selection_algorithms.client import Client
from .client_selection_algorithms.all_based.all_based_client import AllBasedClient
from .client_selection_algorithms.loss_value_based.loss_value_based_client import LossValueBasedClient
from .client_selection_algorithms.threshold_based.threshold_based_client import ThresholdBasedClient
from .client_selection_algorithms.reputation_time_based.reputation_time_based_client import ReputationTimeBasedClient
from .client_selection_algorithms.multi_criteria_based.multi_criteria_based_client import MultiCriteriaBasedClient
from .client_selection_algorithms.random_based.random_based_client import RandomBasedClient
from .client_selection_algorithms.reputation_update_based.reputation_update_based_client import ReputationUpdateBasedClient



class Entity(NamedTuple):
    server: Type[Server]
    client: Type[Client]



class CSAlgo(Enum):
    LOSS = Entity(LossValueBasedServer, LossValueBasedClient)
    THRESHOLD = Entity(ThresholdBasedServer, ThresholdBasedClient)
    REPUTATION_TIME = Entity(ReputationTimeBasedServer, ReputationTimeBasedClient)
    MULTI = Entity(MultiCriteriaBasedServer, MultiCriteriaBasedClient)
    RANDOM = Entity(RandomBasedServer, RandomBasedClient)
    ALL = Entity(AllBasedServer, AllBasedClient)
    REPUTATION_UPDATE = Entity(ReputationUpdateBasedServer, ReputationUpdateBasedClient)
