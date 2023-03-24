from pathlib import Path

import params
from {{cookiecutter.project_name}}.model_training import model
from {{cookiecutter.project_name}}.semi_supervised import semi_supervised_strategies


def instantiate_semi_supervised_strategy(
    model_instance: model.Model,
    unlabeled_file: Path,
    semi_supervised_params: params.SEMI_SUPERVISED,
) -> None:
    """
    TODO
    """
    if semi_supervised_params.SEMI_SUPERVISED_METHOD == "random":
        return semi_supervised_strategies.Random_1(
            model_instance, unlabeled_file, semi_supervised_params
        )
    elif semi_supervised_params.SEMI_SUPERVISED_METHOD == "random_2":
        return semi_supervised_strategies.Random_2(
            model_instance, unlabeled_file, semi_supervised_params
        )
    else:
        raise ValueError(
            f"{semi_supervised_params.SEMI_SUPERVISED_METHOD=} is a not implemented or known strategy"
        )
