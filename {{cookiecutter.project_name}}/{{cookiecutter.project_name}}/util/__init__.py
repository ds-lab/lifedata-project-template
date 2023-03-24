import pandas as pd


def filter_data_from_df(
    input_df: pd.DataFrame,
    filter_df: pd.DataFrame,
) -> pd.DataFrame:
    """This function takes an input_df and filters out any records found in filter_df
        based upon the `sample_id` column

    Args:
        input_df ([pd.DataFrame]): DataFrame with list of records
        filter_df ([pd.DataFrame]): DataFrame containing list of records to be removed

    Returns:
        [pd.DataFrame]: filtered DataFrame without filter_df records
    """

    filtered_df = input_df[~input_df["sample_id"].isin(filter_df["sample_id"])]

    return filtered_df


def get_identical_data_from_df(
    first_df: pd.DataFrame, second_df: pd.DataFrame
) -> pd.DataFrame:
    """This function takes an input_df and filter_df and finds samples that are in both dataframes.

    Args:
        first_df ([pd.DataFrame]): DataFrame with list of records
        second_df ([pd.DataFrame]): DataFrame with list of records

    Returns:
        [pd.DataFrame]: DataFrame with samples that are in both input_df and filter_df.
    """
    filtered_df = first_df[first_df["sample_id"].isin(second_df["sample_id"])]

    return filtered_df
