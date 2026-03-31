import urllib.request
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models

# Configuration
CLASSES = ['apple', 'car', 'cat', 'house', 'tree', 'sun']
MAX_ITEMS_PER_CLASS = 5000 # Enough for good accuracy but fast to process locally
IMAGE_SIZE = 28
DOWNLOAD_DIR = 'data'
MODEL_PATH = '../backend/model.h5'
CLASSES_PATH = '../backend/classes.txt'

def download_data():
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
        
    for cls in CLASSES:
        url = f"https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/{cls}.npy"
        file_path = os.path.join(DOWNLOAD_DIR, f"{cls}.npy")
        if not os.path.exists(file_path):
            print(f"Downloading {cls}.npy...")
            urllib.request.urlretrieve(url, file_path)
        else:
            print(f"{cls}.npy already exists. Skipping download.")

def load_data():
    X = np.empty((0, IMAGE_SIZE * IMAGE_SIZE))
    y = np.empty((0,))
    
    for idx, cls in enumerate(CLASSES):
        file_path = os.path.join(DOWNLOAD_DIR, f"{cls}.npy")
        print(f"Loading {cls}.npy...")
        data = np.load(file_path)
        data = data[:MAX_ITEMS_PER_CLASS] # Limit items
        labels = np.full((data.shape[0],), idx)
        
        X = np.concatenate((X, data), axis=0)
        y = np.concatenate((y, labels), axis=0)
        
    # Reshape and normalize
    X = X.reshape(-1, IMAGE_SIZE, IMAGE_SIZE, 1).astype('float32') / 255.0
    
    # Shuffle
    permutation = np.random.permutation(X.shape[0])
    X = X[permutation]
    y = y[permutation]
    
    return X, y

def build_model(num_classes):
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(IMAGE_SIZE, IMAGE_SIZE, 1)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model

if __name__ == '__main__':
    print("Starting data download...")
    download_data()
    
    print("Loading data...")
    X, y = load_data()
    print(f"Data loaded. X shape: {X.shape}, y shape: {y.shape}")
    
    model = build_model(len(CLASSES))
    model.summary()
    
    print("Training model...")
    # Train
    model.fit(X, y, epochs=3, batch_size=64, validation_split=0.2)
    
    if not os.path.exists('../backend'):
        os.makedirs('../backend')
        
    print(f"Saving model to {MODEL_PATH}...")
    model.save(MODEL_PATH)
    
    print(f"Saving classes to {CLASSES_PATH}")
    with open(CLASSES_PATH, 'w') as f:
        f.write('\n'.join(CLASSES))
        
    print("Training complete!")
