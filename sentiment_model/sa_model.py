import keras
import tensorflow as tf
tf.compat.v1.enable_eager_execution()

import sys
sys.path.append("/Users/panharithsun/Documents/fyp_demo/FastAPI-template")

from sentiment_model.sa_bilstm import SaBiLSTM

class SAModel():
  def __init__(self):
    self.model = keras.models.load_model(
        "/Users/panharithsun/Documents/fyp_demo/FastAPI-template/sentiment_model/sentiment_analysis_bert_khmer_10ep.keras",
        custom_objects={'SaBiLSTM': SaBiLSTM},
        compile=True,
        safe_mode=True
    )

  def predict(self, embedded_vector):
    embedded_vector = tf.expand_dims(embedded_vector, axis=1)
    prediction = self.model.predict(embedded_vector)

    return prediction
