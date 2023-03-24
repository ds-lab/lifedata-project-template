from typing import Any, ClassVar, Type
import torch
import numpy as np
import pandas as pd

from {{cookiecutter.project_name}}.model_training.model import Model
import params

def get_pytorch_device() -> str:
    device = (
        "cuda:0"
        if torch.cuda.is_available()
        else ("mps" if torch.backends.mps.is_available() else "cpu")
    )

    return device


class ModelWrapperTorch(Model):
    model_state_dict_id: ClassVar[str] = "model_state_dict"
    optimizer_state_dict_id: ClassVar[str] = "optimizer_state_dict"

    def __init__(self, model_training: Type[params.MODEL_TRAINING]):
        super().__init__(model_training)

        self.model = torch.nn.Module()
        self.device = get_pytorch_device()


    def save_model(self) -> None:
        self.model.to("cpu")
        
        with torch.no_grad():
            checkpoint_dict = {
                self.model_state_dict_id: self.model.state_dict(),
                self.optimizer_state_dict_id: self.optimizer.state_dict(),
            }

        torch.save(checkpoint_dict, self.model_file)
        self.model.to(self.device)

    def predict_classes(self, features: Any) ->np.ndarray:
        pred_classes = np.argmax(self.predict_probability(features), axis=-1)
        pred_classes = np.atleast_1d(pred_classes)
        
        return pred_classes

    def _history_logger(self, history: dict) -> None:
        if self.history_file.exists():
            try:
                history_df = pd.read_csv(self.history_file, delimiter=";")
            except pd.errors.EmptyDataError:
                history_df = pd.DataFrame()
        else:
            history_df = pd.DataFrame()

        new_row = pd.DataFrame([history])
        history_df = pd.concat([history_df, new_row], axis=0, join="outer", ignore_index=True)

        history_df.to_csv(self.history_file, sep=";", index=False)
