from abc import ABC
from abc import abstractmethod

import pandas as pd


class QueryStrategy(ABC):
    def __init__(self, model_instance, unlabeled_file, query_params):
        """
        TODO
        """
        self.model_instance = model_instance
        self.unlabeled_file = unlabeled_file
        self.query_set_size = query_params.QUERY_SET_SIZE

    @abstractmethod
    def create_queryset(self, features):
        pass


class Random_1(QueryStrategy):
    def create_queryset(self, features):
        """
        TODO
        """

        result = self.model_instance.predict_classes(features)

        unlabeled_data = pd.read_csv(self.unlabeled_file)
        queryset = unlabeled_data.sample(self.query_set_size)
        queryset = pd.concat([queryset, unlabeled_data[result.astype(bool)]])

        return queryset


class Random_2(QueryStrategy):
    def create_queryset(self, features):
        """
        TODO
        """
        pass
