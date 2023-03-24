from abc import ABC
from abc import abstractmethod

import numpy as np
import params
from typing import Any


class Model(ABC):
    def __init__(self, model_training: params.MODEL_TRAINING):
        """
        TODO
        """
        self.model_file = params.absolute_path(model_training.MODEL_FILE)
        self.batch_size = model_training.BATCH_SIZE
        self.epochs = model_training.EPOCHS
        self.learning_rate = model_training.LEARNING_RATE
        self.history_file = params.absolute_path(model_training.HISTORY_FILE)

    @abstractmethod
    def read_model(self) -> None:
        pass

    @abstractmethod
    def define_model(self) -> None:
        pass

    @abstractmethod
    def fit_model(self, features_train: Any, labels_train: Any) -> None:
        pass

    @abstractmethod
    def predict_classes(self, features: Any) -> np.ndarray:
        pass

    @abstractmethod
    def predict_probability(self, X: Any) -> np.ndarray:
        pass

    @abstractmethod
    def save_model(self) -> None:
        pass
