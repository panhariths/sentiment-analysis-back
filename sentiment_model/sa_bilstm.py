import keras
from keras.models import Model # type: ignore
from keras.layers import LSTM, Dense, Bidirectional, Dropout, Activation # type: ignore

@keras.saving.register_keras_serializable('SaBiLSTM')
class SaBiLSTM(Model):
    def __init__(self, input_size=768, hidden_size=512, output_size=3, num_layers=2, dropout=0.5, **kwarg):
        super(SaBiLSTM, self).__init__()
        
        self.lstm_layers = num_layers
        self.hidden_size = hidden_size
        
        self.lstm = LSTM(units=hidden_size, return_sequences=True, dropout=0.2, input_shape=(None, input_size))
        self.bi_lstm = Bidirectional(self.lstm, merge_mode='concat')
        
        self.fc1 = Dense(hidden_size)
        self.relu = Activation('relu')
        self.dropout = Dropout(dropout) if isinstance(dropout, float) and 0 <= dropout <= 1 else Dropout(0.5)
        self.fc2 = Dense(output_size, activation='softmax')

    def call(self, x):

        output = self.bi_lstm(x)
        
        # Select the last output from the sequence
        output = output[:, -1, :]
        
        # Apply relu
        output = self.relu(output)
        
        # Dense layer
        output = self.fc1(output)
        
        # Apply dropout
        output = self.dropout(output)
        
        # Output layer
        output = self.fc2(output)
        
        return output
    
    def get_config(self):
        return {
            "lstm_layers": self.lstm_layers, 
            "hidden_size": self.hidden_size,
            # "lstm": self.lstm,
            # "bi_lstm": self.bi_lstm,
            # "fc1": self.fc1,
            # "dropout": self.dropout,
            # "fc2": self.fc2,
        }
    

