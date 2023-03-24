# %%
from pathlib import Path
from typing import Tuple

import numpy as np
import params
import yaml
from {{cookiecutter.project_name}}.model_training import model_factory
from {{cookiecutter.project_name}}.util import data_input
from sklearn.metrics import classification_report


# %%
def get_data_for_evaluation(
    test_split_file: Path, preprocess_folder: Path
) -> Tuple[np.ndarray, np.ndarray]:
    """
    TODO
    """

    X = data_input.get_features(test_split_file, preprocess_folder)
    y = data_input.get_labels(test_split_file)

    return X, y


# %%
def evaluate_results(model_instance, X_test, y_true):
    """
    TODO
    """
    y_pred = model_instance.predict_classes(X_test)

    report = classification_report(y_true, y_pred, output_dict=True)

    return report


# %%
def save_evaluation_results(evaluation_output: list, evaluation_file: Path) -> None:
    """
    TODO
    """
    with open(evaluation_file, "w") as f:
        yaml.dump(evaluation_output, f)


# %%
if __name__ == "__main__":
    # %%

    test_split_file = params.absolute_path(params.TRAIN_TEST.TEST_SPLIT_FILE)
    preprocessed_folder = params.absolute_path(params.PREPROCESS.FOLDER)
    model_training = params.MODEL_TRAINING
    evaluation_file = params.absolute_path(params.EVALUATION.METRICS_FILE)
    evaluation_folder = params.absolute_path(params.EVALUATION.FOLDER)

    evaluation_folder.mkdir(exist_ok=True)

    # %%
    model_instance = model_factory.instantiate_model(model_training)
    model = model_instance.read_model()

    # %%
    X_test, y_test = get_data_for_evaluation(test_split_file, preprocessed_folder)

    # %%
    # TODO: Use features and labes from returned dataframe
    evaluation_output = evaluate_results(model_instance, X_test, y_test)

    # %%
    save_evaluation_results(evaluation_output, evaluation_file)

# %%
