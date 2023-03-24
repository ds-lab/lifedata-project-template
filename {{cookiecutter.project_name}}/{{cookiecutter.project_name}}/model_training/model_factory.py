import importlib
import os
import pathlib
from typing import Type

from loguru import logger


import params
from {{cookiecutter.project_name}}.model_training import model


def instantiate_model(model_training_params: Type[params.MODEL_TRAINING]) -> model.Model:
    """
    TODO
    """
    base_path = pathlib.Path(__file__).parent.resolve().as_posix() + "/model_implementations"
    possible_frameworks = ["tf", "torch"]

    architecture = model_training_params.MODEL_ARCHITECTURE
    model_path = ""
    found_paths = set([])
    for framework in possible_frameworks:
        if os.path.isfile(base_path + "/" + framework + "/" + architecture + ".py"):
            model_path = (
                "{{cookiecutter.project_name}}.model_training.model_implementations" + "." + framework + "." + architecture
            )
            found_paths.add(model_path)

    if len(found_paths) > 1:
        logger.warning(f"Found multiple equally named model architectures.\n{found_paths}")

    if model_path == "":
        raise ValueError(
            f"{model_training_params.MODEL_ARCHITECTURE=} is an unknown or non-implemented architecture."
        )

    python_file = importlib.import_module(model_path)
    try:
        model_class = getattr(python_file, architecture)
        return model_class(model_training_params)
    except AttributeError:
        raise SystemError(
            architecture
            + " has not been implemented properly. Please reference other existing models"
        )

