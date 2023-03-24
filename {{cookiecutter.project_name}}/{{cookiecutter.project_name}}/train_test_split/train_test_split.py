# %%
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import params
from sklearn.model_selection import train_test_split


# %%
@dataclass
class TrainTestSplit:
    train_data: pd.DataFrame
    test_data: pd.DataFrame


# %%
def get_labeled_samples(labeled_file: Path) -> pd.DataFrame:
    """
    TODO
    """
    return pd.read_csv(labeled_file)


# %%
def split_samples(sample_data: pd.DataFrame, train_test_size: float) -> TrainTestSplit:
    """
    TODO
    """
    train_data, test_data = train_test_split(
        sample_data, test_size=train_test_size, random_state=42
    )

    return TrainTestSplit(train_data=train_data, test_data=test_data)


# %%
def save_train_test_split(
    train_test_split: TrainTestSplit, train_split_file: Path
) -> None:
    """
    TODO
    """
    train_test_split.train_data.to_csv(train_split_file, index=False)
    train_test_split.test_data.to_csv(test_split_file, index=False)


# %%
if __name__ == "__main__":

    # %%
    labeled_file = params.absolute_path(params.EXTERNAL_DATA.LABELED_FILE)
    train_test_split_folder = params.absolute_path(params.TRAIN_TEST.FOLDER)
    train_test_split_folder.mkdir(exist_ok=True)
    test_split_file = params.absolute_path(params.TRAIN_TEST.TEST_SPLIT_FILE)
    train_split_file = params.absolute_path(params.TRAIN_TEST.TRAIN_SPLIT_FILE)

    train_test_size = params.TRAIN_TEST.TEST_SIZE

    # %%
    sample_data = get_labeled_samples(labeled_file)

    # %%
    train_test_splited = split_samples(sample_data, train_test_size)

    # %%
    save_train_test_split(train_test_splited, train_split_file)

# %%
