# %%
from pathlib import Path
from typing import Tuple

import numpy as np
import params
from {{cookiecutter.project_name}}.model_training import model_factory
from {{cookiecutter.project_name}}.util import data_input


# %%
def get_data_for_training(
    train_split_file: Path, preprocess_folder: Path
) -> Tuple[np.ndarray, np.ndarray]:
    """
    TODO
    """

    X = data_input.get_features(train_split_file, preprocess_folder)
    y = data_input.get_labels(train_split_file)

    return X, y


# %%
if __name__ == "__main__":

    # %%
    train_split_file = params.absolute_path(params.TRAIN_TEST.TRAIN_SPLIT_FILE)
    preprocess_folder = params.absolute_path(params.PREPROCESS.FOLDER)
    model_training = params.MODEL_TRAINING
    model_training_folder = params.absolute_path(params.MODEL_TRAINING.FOLDER)
    model_training_folder.mkdir(exist_ok=True, parents=True)

    # %%
    model_instance = model_factory.instantiate_model(model_training)
    model_instance.define_model()

    # %%
    X, y = get_data_for_training(train_split_file, preprocess_folder)

    # %%
    model_instance.fit_model(X, y)

    # %%
    model_instance.save_model()
