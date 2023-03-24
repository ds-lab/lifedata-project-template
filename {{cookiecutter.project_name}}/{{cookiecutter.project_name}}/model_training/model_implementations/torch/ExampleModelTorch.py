from typing import Type
from {{cookiecutter.project_name}}.model_training.modelwrapper_torch import ModelWrapperTorch
from torch import nn
from torch import optim
import torch
import numpy as np
from tqdm import tqdm
import params
class ExampleModel(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.layers = nn.Sequential(nn.Linear(4, 10), nn.ReLU(), nn.Linear(10, 1))

    def forward(self, x):
        x = self.layers(x)
        return x

class ExampleModelTorch(ModelWrapperTorch):
    def __init__(self, model_training: Type[params.MODEL_TRAINING]):
        super().__init__(model_training)
    
    def define_model(self) ->None:
        self.model = ExampleModel()
        self.optimizer = optim.Adam(self.model.parameters(), self.learning_rate)
        self.criterion = nn.BCEWithLogitsLoss()
    
    def fit_model(self, features_train: np.ndarray, labels_train: np.ndarray) -> None:
        self.model.train()
        self.model.to(self.device)

        loss_value = 0.0
        steps = 0

        # create a simple train dataset
        features_train_tensor = torch.from_numpy(features_train)
        labels_train_tensor = torch.from_numpy(labels_train)
        train_dataset = torch.utils.data.TensorDataset(features_train_tensor, labels_train_tensor)

        # train data loader
        train_loader = torch.utils.data.DataLoader(train_dataset, self.batch_size)

        for epoch in tqdm(range(self.epochs)):
            for x, y in train_loader:
                x = x.to(self.device, torch.float)
                y = y.to(self.device, torch.float)

                # zero the parameter gradients
                self.optimizer.zero_grad()

                # forward and backward pass
                pred = self.model(x).flatten()
                loss = self.criterion(pred, y)
                loss.backward()

                loss_value += loss.item()
                steps += 1

                self.optimizer.step()

            self._on_epoch_end(epoch, loss_value, steps)
            loss_value = 0
            steps = 0
    
    def _on_epoch_end(self, epoch: int, loss_value: float, steps: int) -> None:
        self.save_model()

        epoch_loss = loss_value / steps
        
        history = {"epoch": epoch, 
                   "loss": epoch_loss
                   }
        
        self._history_logger(history)

    def read_model(self) -> None:
        self.define_model()
        self.model.to("cpu")

        checkpoint_dict = torch.load(self.model_file, self.device)

        self.model.load_state_dict(checkpoint_dict[self.model_state_dict_id])
        self.optimizer.load_state_dict(checkpoint_dict[self.optimizer_state_dict_id])

        self.model.to(self.device)

    def predict_probability(self, X: np.ndarray) -> np.ndarray:
        all_pred_probabilities = []

        self.model.eval()
        self.model.to(self.device)

        # create a simple dataset
        X_tensor = torch.from_numpy(X)
        prediction_dataset = torch.utils.data.TensorDataset(X_tensor)

        # prediction data loader
        prediction_dataloader = torch.utils.data.DataLoader(prediction_dataset, self.batch_size)

        with torch.no_grad():
            for x in prediction_dataloader:
                x = x[0].to(self.device, torch.float)

                pred = self.model(x).flatten()
                pred_proba = torch.sigmoid(pred)

                all_pred_probabilities.append(pred_proba)

        predicted_probabilities = torch.cat(all_pred_probabilities, dim=0).cpu().numpy().reshape((-1, 1))

        return predicted_probabilities