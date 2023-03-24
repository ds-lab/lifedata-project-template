from typing import Type
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential

from {{cookiecutter.project_name}}.model_training.modelwrapper_keras import ModelWrapper_Keras
import params


class ExampleModelTF(ModelWrapper_Keras):
    def __init__(self, model_training: Type[params.MODEL_TRAINING]):
        super().__init__(model_training)

    def define_model(self) -> None:
        """
        TODO
        """
        self.model = Sequential()
        self.model.add(Dense(10, input_shape=(4,), activation="relu"))
        self.model.add(Dense(1, activation="sigmoid"))
        self.model.compile(optimizer="adam", loss="binary_crossentropy")

    def fit_model(self, features_train, labels_train):
        """
        TODO
        """
        self.model.fit(features_train, labels_train, epochs=self.epochs, callbacks=self.callbacks)