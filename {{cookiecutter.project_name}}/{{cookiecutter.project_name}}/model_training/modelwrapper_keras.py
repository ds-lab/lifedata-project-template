from typing import Any
from typing import Type
import tensorflow.keras as K
import numpy as np

from {{cookiecutter.project_name}}.model_training.model import Model
import params


def get_callback(history_file):
    """
    TODO
    """
    return K.callbacks.CSVLogger(history_file, append=True, separator=";")


class ModelWrapper_Keras(Model):
    def __init__(self, model_training: Type[params.MODEL_TRAINING]):
        super().__init__(model_training)
        
        self.model = K.Model()
        self.callbacks = get_callback(self.history_file)

    def read_model(self):
        """
        TODO
        """
        self.model = K.models.load_model(self.model_file)

    def save_model(self) -> None:
        """
        TODO
        """
        self.model.save(self.model_file)

    def predict_probability(self, X: Any) -> np.ndarray:
        """
        TODO
        """
        return self.model.predict(X)
    
    def predict_classes(self, features: Any) ->np.ndarray:
        """
        TODO
        """
        return np.argmax(self.model.predict(features), axis=-1)
    


