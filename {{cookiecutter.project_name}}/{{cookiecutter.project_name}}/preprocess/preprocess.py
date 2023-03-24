# %%
from pathlib import Path

import numpy as np
import pandas as pd
import params
from {{cookiecutter.project_name}}.util import data_input


# %%
def get_features_to_preprocess(labeled_file: Path, raw_data_folder: Path) -> pd.DataFrame:
    """
    TODO
    """

    samples_to_preprocess_metadata = data_input.get_sample_paths(labeled_file, raw_data_folder)

    return samples_to_preprocess_metadata


# %%
def preprocess_sample(
    example_raw_data: pd.DataFrame, preprocess_params: params.PREPROCESS
) -> np.ndarray:
    """
    TODO
    """

    def multipy_sample(
        example_raw_data: pd.DataFrame, multiplication_factor: float
    ) -> pd.DataFrame:
        """
        TODO
        """
        return example_raw_data * multiplication_factor

    def add_to_sample(example_raw_data: pd.DataFrame, addition_factor: float) -> pd.DataFrame:
        """
        TODO
        """
        return example_raw_data + addition_factor

    multiplication_factor = preprocess_params.MULTIPLICATION_FACTOR
    addition_factor = preprocess_params.ADDITION_FACTOR
    example_data = multipy_sample(example_raw_data, multiplication_factor)
    example_data = add_to_sample(example_data, addition_factor)

    return example_data


# %%
def save_preprocessed_sample(
    preprocessed_data: pd.DataFrame, filename: str, preprocess_folder: Path
) -> None:
    """
    TODO
    """

    preprocessed_data.to_csv(preprocess_folder / (filename + ".csv"), index=False)


# %%
if __name__ == "__main__":

    # %%
    raw_data_folder = params.absolute_path(params.RAW_DATA.FOLDER)
    labeled_file = params.absolute_path(params.EXTERNAL_DATA.LABELED_FILE)
    unlabeled_file = params.absolute_path(params.EXTERNAL_DATA.UNLABELED_FILE)
    preprocess_folder = params.absolute_path(params.PREPROCESS.FOLDER)
    preprocess_folder.mkdir(exist_ok=True, parents=True)

    preprocess_params = params.PREPROCESS

    # %%
    labeled_samples_to_preprocess = get_features_to_preprocess(labeled_file, raw_data_folder)
    unlabeled_samples_to_preprocess = get_features_to_preprocess(unlabeled_file, raw_data_folder)
    samples_to_preprocess = pd.concat([labeled_samples_to_preprocess, unlabeled_samples_to_preprocess])

    # %%
    def apply_preprocess(sample_path: Path, preprocess_params: params.PREPROCESS) -> None:
        raw_data = pd.read_csv(sample_path)
        preprocessed_data = preprocess_sample(raw_data, preprocess_params)
        save_preprocessed_sample(
            preprocessed_data, sample_path.stem, params.absolute_path(preprocess_params.FOLDER)
        )

    # %%
    samples_to_preprocess.apply(
        lambda row: apply_preprocess(row["file_path"], preprocess_params), axis=1
    )

# %%
