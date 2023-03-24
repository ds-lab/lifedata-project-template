from abc import ABC
from abc import abstractmethod

import pandas as pd


class SemiSupervisedStrategy(ABC):
    def __init__(self, model_instance, unlabeled_file, semi_supervised_params):
        """
        TODO
        """
        self.model_instance = model_instance
        self.unlabeled_file = unlabeled_file
        self.semi_supervised_params = semi_supervised_params

    @abstractmethod
    def create_pseudolabels(self, features):
        pass


class Random_1(SemiSupervisedStrategy):
    def create_pseudolabels(self, features):
        """
        TODO
        """
        self.model_instance.read_model()

        result = self.model_instance.predict_classes(features)

        unlabeled_data = pd.read_csv(self.unlabeled_file)
        pseudo_label_set = unlabeled_data.sample(3)
        pseudo_label_set = pd.concat(
            [pseudo_label_set, unlabeled_data[result.astype(bool)]]
        )

        return pseudo_label_set


class Random_2(SemiSupervisedStrategy):
    def create_pseudolabels(self, features):
        """
        TODO
        """
        pass
