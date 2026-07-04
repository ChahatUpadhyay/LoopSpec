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


class TransformerModel:
    """Transformer model for time series forecasting."""
    
    def __init__(
        self,
        sequence_length: int = 60,
        d_model: int = 64,
        n_heads: int = 4,
        n_layers: int = 2,
        dropout_rate: float = 0.1,
        learning_rate: float = 0.001
    ):
        """
        Initialize Transformer model.
        
        Args:
            sequence_length: Input sequence length
            d_model: Model dimension
            n_heads: Number of attention heads
            n_layers: Number of transformer layers
            dropout_rate: Dropout rate
            learning_rate: Learning rate
        """
        self.sequence_length = sequence_length
        self.d_model = d_model
        self.n_heads = n_heads
        self.n_layers = n_layers
        self.dropout_rate = dropout_rate
        self.learning_rate = learning_rate
        self.model = None
        self.scaler = MinMaxScaler()
        
    def transformer_encoder(self, inputs: keras.Input) -> keras.Layer:
        """
        Create transformer encoder block.
        
        Args:
            inputs: Input tensor
        
        Returns:
            Output tensor
        """
        # Self-attention
        attention_output = layers.MultiHeadAttention(
            num_heads=self.n_heads,
            key_dim=self.d_model // self.n_heads
        )(inputs, inputs)
        
        attention_output = layers.Dropout(self.dropout_rate)(attention_output)
        attention_output = layers.LayerNormalization(epsilon=1e-6)(inputs + attention_output)
        
        # Feed-forward
        ffn_output = layers.Dense(self.d_model * 4, activation="relu")(attention_output)
        ffn_output = layers.Dense(self.d_model)(ffn_output)
        ffn_output = layers.Dropout(self.dropout_rate)(ffn_output)
        ffn_output = layers.LayerNormalization(epsilon=1e-6)(attention_output + ffn_output)
        
        return ffn_output
    
    def build_model(self, input_shape: Tuple[int, int]) -> keras.Model:
        """
        Build Transformer model architecture.
        
        Args:
            input_shape: Input shape (sequence_length, features)
        
        Returns:
            Compiled Keras model
        """
        inputs = keras.Input(shape=input_shape)
        
        # Positional encoding (simplified as learnable embedding)
        x = layers.Dense(self.d_model)(inputs)
        
        # Add positional encoding
        positions = tf.range(start=0, limit=self.sequence_length, delta=1)
        position_embedding = layers.Embedding(
            input_dim=self.sequence_length,
            output_dim=self.d_model
        )(positions)
        x = x + position_embedding
        
        # Transformer encoder layers
        for _ in range(self.n_layers):
            x = self.transformer_encoder(x)
        
        # Global average pooling
        x = layers.GlobalAveragePooling1D()(x)
        
        # Output layers
        x = layers.Dropout(self.dropout_rate)(x)
        x = layers.Dense(64, activation="relu")(x)
        x = layers.Dropout(self.dropout_rate)(x)
        outputs = layers.Dense(1)(x)
        
        model = keras.Model(inputs=inputs, outputs=outputs)
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=self.learning_rate),
            loss="mse",
            metrics=["mae"]
        )
        
        return model
    
    def prepare_sequences(
        self,
        data: np.ndarray,
        target: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare sequences for Transformer training.
        
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
        Train Transformer model.
        
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
        
        logger.info(f"Training Transformer model for {epochs} epochs")
        
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
        
        logger.info(f"Transformer model trained. Final loss: {history.history['loss'][-1]:.4f}")
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
