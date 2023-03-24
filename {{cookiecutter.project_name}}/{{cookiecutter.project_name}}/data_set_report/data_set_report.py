# %%
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import params


# %%
@dataclass
class AnalysisResults:
    """
    TODO
    """

    number_files: int
    sample_mean: pd.Series


# %%
def read_raw_samples(raw_folder: Path) -> pd.DataFrame:
    """
    TODO
    """
    example_raw_data = [
        pd.read_csv(file).rename(index=lambda x: file)
        for file in list(raw_folder.glob("*"))
    ]
    return pd.concat(example_raw_data)


# %%
def analyse(raw_folder: Path, raw_data_dataframe: pd.DataFrame) -> AnalysisResults:
    """
    TODO
    """

    number_files = sum(1 for x in raw_folder.parent.glob("**/*") if x.is_file())

    sample_mean = raw_data_dataframe.mean(axis=1)

    return AnalysisResults(number_files=number_files, sample_mean=sample_mean)


# %%
def save_analysis_results(
    analysis_report_file: Path, analysis_results: AnalysisResults
) -> None:
    """
    TODO
    """
    with open(analysis_report_file, "w") as file:
        file.writelines(
            f"In folder and subfolders of {raw_folder.parent} are {analysis_results.number_files} files \n"
            f"The mean Values of the files are: \n"
        )

    analysis_results.sample_mean.to_csv(analysis_report_file, mode="a", header=False)


# %%
if __name__ == "__main__":
    # %%
    raw_folder = params.absolute_path(params.RAW_DATA.FOLDER)
    analysis_folder = params.absolute_path(params.DATA_SET_REPORT.FOLDER)
    analysis_folder.mkdir(exist_ok=True)
    analysis_report_file = params.DATA_SET_REPORT.ANALYSIS_REPORT_FILE

    # %%
    raw_data_dataframe = read_raw_samples(raw_folder)

    # %%
    analysis_results = analyse(raw_folder, raw_data_dataframe)

    # %%
    save_analysis_results(analysis_report_file, analysis_results)
# %%
