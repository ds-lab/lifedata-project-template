# %%
from pathlib import Path

import pandas as pd
import params
from {{cookiecutter.project_name}}.model_training import model_factory
from {{cookiecutter.project_name}}.semi_supervised import semi_supervised_factory
from {{cookiecutter.project_name}}.util import data_input


# %%
def get_data_for_semi_supervised_learning(
    unlabeled_file: Path, preprocess_folder: Path
) -> pd.DataFrame:

    """
    TODO
    """
    return data_input.get_features(unlabeled_file, preprocess_folder)


def save_pseudolabels(pseudolabels: pd.DataFrame, pseudolabels_file: Path) -> None:
    """
    TODO
    """

    pseudolabels.to_csv(pseudolabels_file, index=False)


# %%
if __name__ == "__main__":
    # %%
    preprocess_folder = params.absolute_path(params.PREPROCESS.FOLDER)
    unlabeled_file = params.absolute_path(params.EXTERNAL_DATA.UNLABELED_FILE)
    pseudolabels_file = params.absolute_path(params.SEMI_SUPERVISED.PSEUDOLABEL_SET_FILE)
    pseudolabels_folder = params.absolute_path(params.SEMI_SUPERVISED.FOLDER)
    pseudolabels_folder.mkdir(exist_ok=True)
    semi_supervised_params = params.SEMI_SUPERVISED
    model_training = params.MODEL_TRAINING

    # %%
    model_instance = model_factory.instantiate_model(model_training)

    # %%
    semi_supervised_instance = semi_supervised_factory.instantiate_semi_supervised_strategy(
        model_instance, unlabeled_file, semi_supervised_params
    )

    # %%
    X = get_data_for_semi_supervised_learning(unlabeled_file, preprocess_folder)

    # %%
    pseudolabels = semi_supervised_instance.create_pseudolabels(X)

    # %%
    save_pseudolabels(pseudolabels, pseudolabels_file)

# %%
