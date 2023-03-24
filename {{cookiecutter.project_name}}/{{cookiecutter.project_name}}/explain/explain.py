# %%
from pathlib import Path
from typing import Any

import params
import yaml
from {{cookiecutter.project_name}}.explain import explain_factory
from {{cookiecutter.project_name}}.model_training import model_factory


# %%
def save_explanation(explain_results: Any, explain_file: Path) -> None:
    """
    TODO
    """
    with open(explain_file, "w") as f:
        yaml.dump({"Explanation": "This is an explanation"}, f)


# %%
if __name__ == "__main__":
    # %%
    explain_file = params.absolute_path(params.EXPLAIN.METRICS_FILE)
    explain_folder = params.absolute_path(params.EXPLAIN.FOLDER)
    explain_folder.mkdir(exist_ok=True)

    model_training = params.MODEL_TRAINING
    train_split_file = params.absolute_path(params.TRAIN_TEST.TRAIN_SPLIT_FILE)
    preprocess_folder = params.absolute_path(params.PREPROCESS.FOLDER)

    # %%
    model_instance = model_factory.instantiate_model(model_training)
    model = model_instance.read_model()

    # %%
    explain_instance = explain_factory.instanciate_explanation()
    explain_results = explain_instance.explain()

    # %%
    save_explanation(explain_results, explain_file)

# %%
