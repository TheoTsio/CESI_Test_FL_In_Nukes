import warnings
import flwr as fl
from flwr.server.strategy import FedAvg

# Suppress the deprecation warning since we are using the classic start function
warnings.filterwarnings("ignore", category=DeprecationWarning)

class FederatedServer:
    def __init__(self, num_rounds: int = 3, min_clients: int = 2):
        self.num_rounds = num_rounds
        self.min_clients = min_clients
        print(f"️  Initializing FederatedServer for {num_rounds} rounds...")

    def start(self):
        """This method actually starts and blocks the server."""
        strategy = FedAvg(
            fraction_fit=1.0,       
            fraction_evaluate=1.0,  
            min_fit_clients=self.min_clients,
            min_evaluate_clients=self.min_clients,
            min_available_clients=self.min_clients,
        )
        
        print("🌐 Starting Flower server on 0.0.0.0:8080... (Waiting for clients)")
        
        # This function blocks and keeps the server running
        fl.server.start_server(
            server_address="0.0.0.0:8080",
            config=fl.server.ServerConfig(num_rounds=self.num_rounds),
            strategy=strategy,
        )

if __name__ == "__main__":
    import sys
    # Allow passing the number of clients via command line (default to 2)
    min_c = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    
    # 1. Create the server instance
    my_server = FederatedServer(num_rounds=3, min_clients=min_c)
    
    # 2. Start it
    my_server.start()