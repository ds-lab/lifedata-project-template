from pathlib import Path
from abc import ABCMeta
from abc import abstractmethod
from enum import Enum
from typing import ClassVar

import params
from {{cookiecutter.project_name}}.model_training.model import Model
from {{cookiecutter.project_name}}.query.qs_base import QueryStrategy
from {{cookiecutter.project_name}}.query.qs_random import RandomQuery
from {{cookiecutter.project_name}}.query.qs_uncertainty import Uncertainty
from {{cookiecutter.project_name}}.query.qs_customized import CustomizedQS

class QUERY_STRATEGIES_FACTORIES(Enum):
    RANDOM = "random"
    UNCERTAINTY = "uncertainty"


class QueryStrategyCreator(metaclass=ABCMeta):
    _params: ClassVar = params

    def __init__(self) -> None:
        pass

    @abstractmethod
    def create_query_strategy(self, model_instance: Model) -> QueryStrategy:
        raise NotImplementedError("Must be implemented by the subclass.")



class QueryStrategyFactory:
    def instantiate_query_strategy(
        self, query_strategy: str, model_instance: Model
    ) -> QueryStrategy:
        if query_strategy.lower() == QUERY_STRATEGIES_FACTORIES.RANDOM.value:
            return RandomQSCreator().create_query_strategy(model_instance)
        elif query_strategy.lower() == QUERY_STRATEGIES_FACTORIES.UNCERTAINTY.value:
            return UncertaintyCreator().create_query_strategy(model_instance)
        else:
            raise ValueError(f"{query_strategy} is not implemented or unknown strategy.")

    def initialize(self, model_instance: Model) -> QueryStrategy:
        return CustomQSCreator().create_query_strategy(model_instance)



class RandomQSCreator(QueryStrategyCreator):
    def __init__(self) -> None:
        super().__init__()

    def create_query_strategy(self, model_instance: Model) -> QueryStrategy:
        random_state = self._params.RANDOM_STATE
        random_qs = RandomQuery(random_state)
        return random_qs

class UncertaintyCreator(QueryStrategyCreator):
    def __init__(self) -> None:
        super().__init__()

    def create_query_strategy(self, model_instance: Model) -> QueryStrategy:
        uncertainty = Uncertainty(model_instance)
        return uncertainty

class CustomQSCreator(QueryStrategyCreator):
    def __init__(self) -> None:
        super().__init__()

    def create_query_strategy(self, model_instance: Model) -> QueryStrategy:
        all_qs = []
        all_perc = []
        for query_strategy, perc in zip(
            self._params.QUERY.LIST_QS_STRATEGIES,
            self._params.QUERY.LIST_QS_WEIGHTS,
        ):
            all_perc.append(perc)
            all_qs.append(
                QueryStrategyFactory().instantiate_query_strategy(query_strategy, model_instance)
            )

        custom_qs = CustomizedQS(weights_per_qs=all_perc, array_of_qs=all_qs)
        return custom_qs