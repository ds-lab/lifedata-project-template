from typing import Any
import numpy as np 
import pandas as pd

from {{cookiecutter.project_name}}.query.qs_base import QueryStrategy
from {{cookiecutter.project_name}}.query.qs_base import QueryData


class RandomQuery(QueryStrategy):
    def __init__(self, random_state: int) -> None:
        super().__init__()
        self._strategy_type_identifier = "Random"
        self._strategy_name_identifier = "Random Selector"
        np.random.seed(random_state)

    def assess(
        self,
        X: QueryData
    ) -> QueryStrategy:
        sample_ids = X.sample_ids
        number_of_samples = len(sample_ids)
        random_score = np.random.uniform(low=0.0, high=1.0, size=(number_of_samples, 1)).flatten()
        self._score_df = self._create_score_df_with_information(random_score, sample_ids)
        return self

    def query(self, query_set_size: int) -> pd.DataFrame:
        self._query_df = self._score_df.nlargest(query_set_size, self._query_score_column_names[0])
        return self._query_df
