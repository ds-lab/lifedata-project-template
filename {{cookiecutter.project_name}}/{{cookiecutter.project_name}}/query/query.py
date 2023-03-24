# %%
from pathlib import Path

import pandas as pd
import numpy as np
import params
from {{cookiecutter.project_name}}.model_training import model_factory
from {{cookiecutter.project_name}}.query.query_strategy_factory import QueryStrategyFactory
from {{cookiecutter.project_name}}.query.qs_base import QueryData
from {{cookiecutter.project_name}}.util import data_input


# %%
def get_data_for_queryset_creation(unlabeled_file: Path, preprocess_folder: Path) -> QueryData:
    """
    TODO
    """
    features = data_input.get_features(unlabeled_file, preprocess_folder)
    sample_ids = data_input.get_sample_ids(unlabeled_file)

    query_data = QueryData(sample_ids, features)

    return query_data


# %%
def save_queryset(queryset: pd.DataFrame, queryset_file: Path) -> None:
    """
    TODO
    """
    queryset.to_csv(queryset_file, index=False)


# %%
if __name__ == "__main__":
    # %%
    preprocess_folder = params.absolute_path(params.PREPROCESS.FOLDER)
    unlabeled_file = params.absolute_path(params.EXTERNAL_DATA.UNLABELED_FILE)
    model_training = params.MODEL_TRAINING
    query_params = params.QUERY
    queryset_folder = params.absolute_path(params.QUERY.FOLDER)
    queryset_folder.mkdir(exist_ok=True)
    queryset_file = params.absolute_path(params.QUERY.QUERY_SET_FILE)

    # %%
    model_instance = model_factory.instantiate_model(model_training)
    model_instance.read_model()

    # %%
    query_strategy_instance = QueryStrategyFactory().initialize(model_instance)

    # %%
    X = get_data_for_queryset_creation(unlabeled_file, preprocess_folder)

    # %%
    # reduce queryset size for last iteration
    query_params.QUERY_SET_SIZE = min(query_params.QUERY_SET_SIZE, len(X))

    # %%
    queryset = query_strategy_instance.assess_query(
            X, query_params.QUERY_SET_SIZE
    )


    # %%
    save_queryset(queryset, queryset_file)
