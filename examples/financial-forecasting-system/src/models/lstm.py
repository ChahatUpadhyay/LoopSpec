import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.preprocessing import MinMaxScaler
from typing import Tuple, Optional
import logging

from ..utils.logging import get_logger

logger = get_logger(__name__)


class LSTMModel:
    """LSTM model for time series forecasting."""
    
    def __init__(
        self,
        sequence_length: int = 60,
        lstm_units: int = 50,
        dropout_rate: float = 0.2,
        dense_units: int = 25,
        learning_rate: float = 0.001
    ):
        """
        Initialize LSTM model.
        
        Args:
            sequence_length: Input sequence length
            lstm_units: Number of LSTM units
            dropout_rate: Dropout rate
            dense_units: Number of dense layer units
            learning_rate: Learning rate
        """
        self.sequence_length = sequence_length
        self.lstm_units = lstm_units
        self.dropout_rate = dropout_rate
        self.dense_units = dense_units
        self.learning_rate = learning_rate
        self.model = None
        self.scaler = MinMaxScaler()
        
    def prepare_sequences(
        self,
        data: np.ndarray,
        target: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare sequences for LSTM training.
        
        Args:
            data: Input data
            target: Target data
        
        Returns:
            Tuple of (X, y) sequences
        """
        X, y = [], []
        
        for i in range(len(data) - self.sequence_length):
            X.append(data[i:i + self.sequence_length])
            y.append(target[i + self.sequence_length])
        
        return np.array(X), np.array(y)
    
    def build_model(self, input_shape: Tuple[int, int]) -> keras.Model:
        """
        Build LSTM model architecture.
        
        Args:
            input_shape: Input shape (sequence_length, features)
        
        Returns:
            Compiled Keras model
        """
        model = keras.Sequential([
            layers.LSTM(
                self.lstm_units,
                return_sequences=True,
                input_shape=input_shape
            ),
            layers.Dropout(self.dropout_rate),
            layers.LSTM(self.lstm_units, return_sequences=False),
            layers.Dropout(self.dropout_rate),
            layers.Dense(self.dense_units),
            layers.Dense(1)
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=self.learning_rate),
            loss="mse",
            metrics=["mae"]
        )
        
        return model
    
    def train(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        epochs: int = 50,
        batch_size: int = 32,
        validation_split: float = 0.2,
        verbose: int = 0
    ) -> keras.Model:
        """
        Train LSTM model.
        
        Args:
            X: Feature DataFrame
            y: Target series
            epochs: Number of training epochs
            batch_size: Batch size
            validation_split: Validation split ratio
            verbose: Verbosity level
        
        Returns:
            Trained model
        """
        # Scale data
        X_scaled = self.scaler.fit_transform(X)
        y_scaled = self.scaler.fit_transform(y.values.reshape(-1, 1)).flatten()
        
        # Prepare sequences
        X_seq, y_seq = self.prepare_sequences(X_scaled, y_scaled)
        
        # Build model
        input_shape = (self.sequence_length, X.shape[1])
        self.model = self.build_model(input_shape)
        
        logger.info(f"Training LSTM model for {epochs} epochs")
        
        # Train with early stopping
        early_stopping = keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=10,
            restore_best_weights=True
        )
        
        history = self.model.fit(
            X_seq, y_seq,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            callbacks=[early_stopping],
            verbose=verbose
        )
        
        logger.info(f"LSTM model trained. Final loss: {history.history['loss'][-1]:.4f}")
        return self.model
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Make predictions with trained model.
        
        Args:
            X: Feature DataFrame
        
        Returns:
            Predictions array
        """
        if self.model is None:
            raise ValueError("Model must be trained before prediction")
        
        # Scale input
        X_scaled = self.scaler.transform(X)
        
        # Prepare sequences
        X_seq, _ = self.prepare_sequences(X_scaled, np.zeros(len(X)))
        
        # Predict
        predictions_scaled = self.model.predict(X_seq, verbose=0)
        
        # Inverse scale
        predictions = self.scaler.inverse_transform(predictions_scaled).flatten()
        
        return predictions
