from __future__ import annotations

from abc import ABCMeta
from abc import abstractmethod
from typing import List
from typing import Tuple
from typing import Any
from dataclasses import dataclass

import numpy as np
import pandas as pd

from {{cookiecutter.project_name}}.util import filter_data_from_df
from {{cookiecutter.project_name}}.util import get_identical_data_from_df

@dataclass
class QueryData:
    sample_ids: Any
    features: Any

    def __len__(self):
        return len(self.sample_ids)

class QueryStrategy(metaclass=ABCMeta):
    """Abstract base class for all query strategies.

    A query strategy is designed as follows:
        1.  The init method should receive as arguments everything that is required to compute  \n
            query strategy, except from `query_set_size`, `unlabeled_df` (data from which the \n
            samples are quired) and `weights` (a weighting score of each sample).
        2.  First, `assess` must be called. In `assess` a score, which represents the conformance to \n
            the query strategy, is calculated.
        3.  Second and last, `query` must be called. `Query` selects and returns the most suitable \n
            samples based on the previously calculated score.
    """

    def __init__(self) -> None:
        """Init method for all query strategies."""
        self._score_df = pd.DataFrame()
        self._query_df = pd.DataFrame()
        self._strategy_type_identifier = "Baseclass"
        self._strategy_name_identifier = "Baseclass_No_Selector"
        self._query_score_column_names = [
            "query_score",
            "strategy_type_identifier",
            "strategy_name_identifier",
        ]

    @property
    def query_score_column_name(self) -> List[str]:
        return self._query_score_column_names

    @property
    def strategy_type_identifier(self) -> str:
        return self._strategy_type_identifier

    @property
    def strategy_name_identifier(self) -> str:
        return self._strategy_name_identifier

    @property
    def column_names(self) -> Tuple[str]:
        return self._query_df.columns

    @property
    def score(self) -> pd.DataFrame:
        """The calculated score for each sample.

        Raises:
            AttributeError: If the score is accessed before `assess` has been called.

        Returns:
            pd.DataFrame: The calculated score for each sample.
        """
        if len(self._score_df) == 0:
            raise AttributeError(
                "You have to call assess before you can access the score_df."
            )
        else:
            return self._score_df

    @property
    def query_df(self) -> pd.DataFrame:
        """The query set.

        Raises:
            AttributeError: If the query set is accessed before `assess` or `query` have been called.

        Returns:
            pd.DataFrame: The query set.
        """
        if len(self._query_df) == 0:
            raise AttributeError(
                "You have to call `query` before you can access the query_df."
            )
        else:
            return self._query_df

    def _check_assessed(self) -> None:
        if len(self._score_df) == 0:
            raise AttributeError("You have to call assess before query.")

    def _check_query_set_size(self, query_set_size: int) -> None:
        if query_set_size <= 0:
            raise ValueError("Queryset should contain more than zero samples.")

    def _check_nan(self, array: np.ndarray, error_msg: str) -> None:
        if np.isnan(array).any():
            raise ValueError(error_msg)

    @abstractmethod
    def assess(
        self,
        X: QueryData,
    ) -> QueryStrategy:
        raise NotImplementedError("Must be implemented by the subclass.")

    @abstractmethod
    def query(self, query_set_size: int) -> pd.DataFrame:
        raise NotImplementedError("Must be implemented by the subclass.")

    def query_excluding_samples_in_df(
        self, query_set_size: int, samples_df: pd.DataFrame
    ) -> pd.DataFrame:
        query_df_without_samples = pd.DataFrame()
        new_query_set_size = query_set_size
        while len(query_df_without_samples) != query_set_size:
            query_df = self.query(new_query_set_size)
            duplicates_df = get_identical_data_from_df(query_df, samples_df)
            number_of_duplicates = len(duplicates_df)
            new_query_set_size = query_set_size + number_of_duplicates
            query_df_without_samples = filter_data_from_df(query_df, duplicates_df)
        return query_df_without_samples

    def assess_query(
        self,
        X: QueryData,
        query_set_size: int,
    ) -> pd.DataFrame:
        """Combination of `assess` and `query`.

        This is equivalent to calling `asses` followed by `query`.

        Args:
            X (QueryData): Input from which the query set is selected.
            query_set_size (int): The size of the resulting query set.

        Returns:
            pd.DataFrame: A dataframe containing `query_set_size` queried samples.
        """
        self.assess(X)
        query_df = self.query(query_set_size)

        return query_df

    def _create_score_df_with_information(
        self, score: List[float], sample_ids: List[str]
    ) -> pd.DataFrame:
        list_strategy_type_identifier = [self._strategy_type_identifier] * len(score)
        list_strategy_name_identifier = [self._strategy_name_identifier] * len(score)

        score_dict_with_information = {
            "sample_id": sample_ids,
            self._query_score_column_names[0]: score,
            self._query_score_column_names[1]: list_strategy_type_identifier,
            self._query_score_column_names[2]: list_strategy_name_identifier,
        }

        score_df_with_information = pd.DataFrame(score_dict_with_information)
        return score_df_with_information
