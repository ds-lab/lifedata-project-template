from __future__ import annotations

import numpy as np
import pandas as pd

from {{cookiecutter.project_name}}.model_training import model
from {{cookiecutter.project_name}}.query.qs_base import QueryStrategy
from {{cookiecutter.project_name}}.query.qs_base import QueryData


class Uncertainty(QueryStrategy):
    def __init__(self, model_instance: model.Model) -> None:
        super().__init__()
        self._model_instance = model_instance
        self._strategy_name_identifier = "Uncertainty Selector"
        self._strategy_type_identifier = "Informativeness"

    def assess(
        self,
        X: QueryData
    ) -> QueryStrategy:
        self._X = X

        sample_ids = self._X.sample_ids

        predictions = self._get_predictions()
        uncertainty_score = self._calculate_uncertainty_score(predictions)
        self._score_df = self._create_score_df_with_information(uncertainty_score, sample_ids)

        return self

    def query(self, query_set_size: int) -> pd.DataFrame:
        self._check_assessed()
        self._check_query_set_size(query_set_size)

        self._query_set_size = query_set_size
        self._query_df = self._score_df.nlargest(
            self._query_set_size, self._query_score_column_names[0]
        )
        return self._query_df

    def _calculate_uncertainty_score(self, predictions: np.ndarray) -> np.ndarray:
        uncertainty_score = 1 - np.max(predictions, axis=1)
        return uncertainty_score

    def _get_predictions(self) -> np.ndarray:
        predictions = self._model_instance.predict_probability(self._X.features)
        error_msg = "At least one prediction is nan."
        self._check_nan(predictions, error_msg)
        return predictions
