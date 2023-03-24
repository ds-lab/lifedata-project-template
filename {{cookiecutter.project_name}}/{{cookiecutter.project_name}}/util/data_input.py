# %%
from pathlib import Path

import numpy as np
import pandas as pd


# %%
def get_sample_paths(metadata_file: Path, sample_folder: Path) -> pd.DataFrame:
    """
    TODO
    """

    metadata = pd.read_csv(metadata_file)
    metadata["file_path"] = metadata.apply(
        lambda row: sample_folder / (row["sample_id"] + ".csv"), axis=1
    )

    return metadata

# %%
def get_sample_ids(metadata_file: Path) -> np.ndarray:
    metadata = pd.read_csv(metadata_file)
    sample_ids = metadata["sample_id"]

    return sample_ids.to_numpy()

# %%
def get_features(metadata_file: Path, sample_folder: Path) -> np.ndarray:
    """
    TODO
    """

    samples_metadata = get_sample_paths(metadata_file, sample_folder)

    def read_sample(sample_path):
        # Sample is first/only element in csv
        sample_df = pd.read_csv(sample_path).iloc[0]
        return sample_df.values

    samples_metadata["features"] = samples_metadata.apply(
        lambda row: read_sample(row["file_path"]), axis=1
    )

    return np.vstack(samples_metadata["features"])


# %%
def get_labels(metadata_file: Path) -> np.ndarray:
    samples_metadata = pd.read_csv(metadata_file)

    return samples_metadata["label"].to_numpy()


# %%
