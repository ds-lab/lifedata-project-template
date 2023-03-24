from typing import List
from typing import Any

import numpy as np 
import pandas as pd 

from {{cookiecutter.project_name}}.query.qs_base import QueryStrategy
from {{cookiecutter.project_name}}.query.qs_base import QueryData

class CustomizedQS(QueryStrategy):
    """
    Implementation of a general purpose QueryStrategy accumulator. Can take an arbitrary length of QueryStrategies and
    return the query set according to its relative percentages.
    """

    def __init__(
        self,
        weights_per_qs: List[float],
        array_of_qs: List[QueryStrategy],
        index_default_qs: int = 0,
    ) -> None:
        """ "Configure the proportional rdi query strategy.

        Args:
            weights_per_qs (float[]): Weights per Query Strategy. Sets how many samples are retrieved per each QS relatively (up to total query set size)
            array_of_qs (QueryStrategy[]): List of different QueryStrategies to be used with the previously defined proportionalities
        """
        self._percentages_per_qs = self.check_percentages(weights_per_qs)
        self._array_of_qs = array_of_qs
        self._index_default_qs = index_default_qs

    def assess(
        self,
        X: QueryData,
    ) -> QueryStrategy:
        """Assess each sample with both query strategies.
        The score for each sample consists of both informativeness and representativeness and is NOT \n
        combined. So the score dataframe has two columns.

        Args:
            X (QueryData): Input from which the samples are queried.
        Returns:
            QueryStrategy: The object that has already assessed the data.
        """

        self._X = X
        # assess each query strategy
        for qs in self._array_of_qs:
            self._assessed = True
            qs.assess(
                X=self._X,
            )

        return self

    def _check_assessed(self) -> None:
        """Overwrite default function from base.
        Customized QueryStrategy does not create a score dataframe, only checks if it was run.
        """
        if not self._assessed:
            raise AttributeError("You have to call assess before query.")

    def query(self, query_set_size: int) -> pd.DataFrame:
        """Query samples.
        Choose  a number of `query_set_size` of samples from  `X` where `percentage_informativeness`\n
        percent are informativeness samples and percentage_representativeness percent are representativeness samples.

        Args:
            query_set_size (int): The size of the resulting query set.

        Raises:
            ValueError: If the `query_set_size` <= 0.
            AttributeError: If `query` is called before `assess`Ï.
        Returns:
            pd.DataFrame: A dataframe containing the query set of size `query_set_size`.
        """

        # perform checks
        self._check_assessed()
        self._check_query_set_size(query_set_size)

        self._query_set_size = query_set_size
        self._query_df = pd.DataFrame(columns=["sample_id"])
        data_frames = []

        for qs in self._array_of_qs:
            temp_qs_query_df = qs.query(query_set_size=query_set_size)
            data_frames.append(temp_qs_query_df)

        steps = np.asarray(self._percentages_per_qs)
        perc = steps.copy()
        indices = np.zeros(len(self._array_of_qs), dtype=np.int32)

        for _ in range(0, query_set_size):
            max_el = np.argmax(steps)

            # Check if a sample ID is already in the query frame, and skip it if necessary
            s_id = data_frames[max_el].iloc[[indices[max_el]]]["sample_id"].iat[0]
            while s_id in self._query_df["sample_id"].unique():
                indices[max_el] += 1
                s_id = data_frames[max_el].iloc[[indices[max_el]]]["sample_id"].iat[0]

            self._query_df = pd.concat(
                [self._query_df, data_frames[max_el].iloc[[indices[max_el]]]]
            )
            steps[max_el] -= 1
            indices[max_el] += 1
            steps = np.add(steps, perc)

        return self._query_df

    def _append_dataframes_with_infos(self, query_df: pd.DataFrame) -> None:
        """Append the new data frame to any previous existing Query dataframe. Added scores and type / name of the QueryStrategy responsible for these sampleIDs

        Args:
            query_df (pd.DataFrame): The informativness query dataframe.
            query_strategy_identifier (str): Type of query strategy, i.e. type [informativeness, representativeness, diversity].
            query_name_identifier (str): The name of QueryStrategy for better verification, e.g. Best vs Second best, Density weighted Diversity, etc.

        Returns:
            pd.DataFrame: The query dataframe with additional informations.
        """
        # append query strategy information
        local_query_df = query_df.copy()
        self._query_df = pd.concat([self._query_df, local_query_df])

    def check_percentages(self, percentages_per_qs: List[float]) -> np.ndarray:
        temp_percentages_per_qs = percentages_per_qs / np.sum(percentages_per_qs)
        # any potential error here would be up to floating point operations, so no check necessary

        return temp_percentages_per_qs
