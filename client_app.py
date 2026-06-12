import sys
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from collections import OrderedDict
import numpy as np
import flwr as fl
from task import load_data
from codecarbon import EmissionsTracker, OfflineEmissionsTracker  # 1. Import CodeCarbon
import os

# --- 1. Simple Neural Network (Now accepts num_features dynamically) ---
class SimpleNet(nn.Module):
    def __init__(self, num_features):
        super(SimpleNet, self).__init__()
        self.fc1 = nn.Linear(num_features, 16) 
        self.fc2 = nn.Linear(16, 2)  

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# --- 2. Flower Client ---
class FlowerClient(fl.client.NumPyClient):
    def __init__(self, train_pool, test_pool, partition_id):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.partition_id = partition_id

        # ✅ FIX: Dynamically get the number of features from the CatBoost Pool
        num_features = train_pool.get_features().shape[1]
        print(f"📊 Detected {num_features} features in dataset.")
        
        self.model = SimpleNet(num_features=num_features).to(self.device)
        
        self.train_loader = self._pool_to_dataloader(train_pool)
        self.test_loader = self._pool_to_dataloader(test_pool, shuffle=False)
        
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.SGD(self.model.parameters(), lr=0.01)

    def _pool_to_dataloader(self, pool, batch_size=32, shuffle=True):
        """Helper to convert CatBoost Pool to PyTorch DataLoader"""
        if pool is None:
            return None
            
        features = pool.get_features()
        labels = pool.get_label()
        
        X_tensor = torch.from_numpy(features).float()
        y_tensor = torch.from_numpy(labels).long()
        
        dataset = TensorDataset(X_tensor, y_tensor)
        return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)

    def get_parameters(self, config):
        return [val.cpu().numpy() for _, val in self.model.state_dict().items()]

    def set_parameters(self, parameters):
        params_dict = zip(self.model.state_dict().keys(), parameters)
        state_dict = OrderedDict({k: torch.tensor(v) for k, v in params_dict})
        self.model.load_state_dict(state_dict, strict=True)

    def fit(self, parameters, config):
        # Extract the current round number sent by the Flower server
        current_round = config.get("server_round", 0)
        
        # ✅ FIX: Creating a unique path dynamically matching your style
        output_dir = f"/home/ncuser/Desktop/CESI_Test_FL_In_Nukes/metrics_{self.partition_id}"
        os.makedirs(output_dir, exist_ok=True)  

        # ✅ FIX: Combined and cleaned the config dictionary
        tracker_config = {
            "project_name": f"flower_client_{self.partition_id}_round_{current_round}",
            "output_dir": output_dir,
            "output_file": f"emissions_client_{self.partition_id}.csv",  # Keeps client logs unique
            "country_iso_code": "FRA",
            "tracking_mode": "process"     
        }

        print(f"🌱 [Client {self.partition_id}] Starting local training for Round {current_round}...")

        with OfflineEmissionsTracker(**tracker_config):
            self.set_parameters(parameters)
            self.model.train()
            
            for batch_X, batch_y in self.train_loader:
                batch_X, batch_y = batch_X.to(self.device), batch_y.to(self.device)
                self.optimizer.zero_grad()
                outputs = self.model(batch_X)
                loss = self.criterion(outputs, batch_y)
                loss.backward()
                self.optimizer.step()
            
        return self.get_parameters(config={}), len(self.train_loader.dataset), {"loss": loss.item()}
    
    def evaluate(self, parameters, config):
        self.set_parameters(parameters)
        self.model.eval()
        total_loss, total_correct, total_samples = 0.0, 0, 0
        
        with torch.no_grad():
            for batch_X, batch_y in self.test_loader:
                batch_X, batch_y = batch_X.to(self.device), batch_y.to(self.device)
                outputs = self.model(batch_X)
                loss = self.criterion(outputs, batch_y)
                total_loss += loss.item() * batch_X.size(0)
                total_correct += (outputs.argmax(1) == batch_y).sum().item()
                total_samples += batch_X.size(0)
                
        avg_loss = total_loss / total_samples
        accuracy = total_correct / total_samples
        return float(avg_loss), total_samples, {"accuracy": accuracy}

# --- 3. Start Client ---
if __name__ == "__main__":
    partition_id = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    server_ip = sys.argv[2] if len(sys.argv) > 2 else "flower-server" 

    train_pool, test_pool = load_data(partition_id=partition_id, num_partitions=2)
    print(f" Starting PyTorch Client (Partition: {partition_id}) connecting to {server_ip}:8080")

    fl.client.start_numpy_client(
        server_address=f"{server_ip}:8080",
        client=FlowerClient(train_pool, test_pool)
    )