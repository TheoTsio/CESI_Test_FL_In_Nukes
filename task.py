import numpy as np
from catboost import Pool
from sklearn.model_selection import train_test_split

def load_data(partition_id: int, num_partitions: int):
    # Base random state modified by the partition ID ensures completely unique datasets
    np.random.seed(42 + partition_id)
    
    # 1. Create a dummy tabular matrix (200 records, 10 feature columns)
    X = np.random.randn(200, 10)
    y = np.random.randint(0, 2, size=200)
    
    # 2. Divide local records into processing and validation sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 3. Compile datasets into optimized CatBoost processing Pools
    train_pool = Pool(X_train, y_train)
    test_pool = Pool(X_test, y_test)
    
    print(f"📦 Loaded Partition {partition_id}: {len(X_train)} train samples, {len(X_test)} validation samples.")
    return train_pool, test_pool