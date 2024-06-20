from fastapi import APIRouter
from typing import Optional
from pydantic import BaseModel
import pickle
import time
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from khmernltk import word_tokenize

import sys
sys.path.append("/Users/panharithsun/Documents/fyp_demo/FastAPI-template")

from sentiment_model.bert_khmer import BERTKhmerEmbedder
from sentiment_model.sa_model import SAModel
from sentiment_model.preprocessing import preprocess

class SentimentResponseSchema(BaseModel):
    sentiments: Optional[list[float]] = []
    elapsed_time: Optional[float] = 0.0
class SentimentRequestSchema(BaseModel):
    text: str

router = APIRouter()

# BILSTM
bilstm_model = SAModel()

# SVM
with open('/Users/panharithsun/Documents/fyp_demo/FastAPI-template/sentiment_model/sentiment_svm_proba.pkl', 'rb') as f:
    svm_model = pickle.load(f)

# KNN
with open('/Users/panharithsun/Documents/fyp_demo/FastAPI-template/sentiment_model/sentiment_knn.pkl', 'rb') as f:
    knn_model = pickle.load(f)

# NB
with open('/Users/panharithsun/Documents/fyp_demo/FastAPI-template/sentiment_model/sentiment_nb.pkl', 'rb') as f:
    nb_model = pickle.load(f)

# RF
with open('/Users/panharithsun/Documents/fyp_demo/FastAPI-template/sentiment_model/sentiment_rf.pkl', 'rb') as f:
    rf_model = pickle.load(f)

def process_input(input):
    """ Text input """

    input_text = input

    """ Text Cleaning """

    cleaned_text = preprocess(input_text)
    print("Finished cleaning text...")

    """ Word tokenization """
    
    tokenized_sentence = word_tokenize(cleaned_text)
    print("Finished tokenizing text...")

    """ Word embedding """

    khmer_bert = BERTKhmerEmbedder()
    embedded = khmer_bert.extract_word_embeddings([tokenized_sentence])

    print("Finished embeding text...")
    print("Received embedding of shape: ", embedded.shape)

    return embedded

def show_multiclass_result(prediction, input_text):

    prediction_class_index = np.argmax(prediction)
    classes = ['Negative', 'Neutral', 'Positive']

    # Find the index of the maximum value in the result array
    overall_sentiment_index = prediction_class_index
    overall_sentiment = classes[overall_sentiment_index]

    # Print overall sentiment
    print("Text:", input_text)
    print("Overall sentiment:", overall_sentiment)

    # Print prediction per class
    print("\nPrediction per class:")
    for class_name, probability in zip(classes, prediction[0]):
        print(f"{class_name}: {probability}")

    sentiment_dict = SentimentResponseSchema()
    sentiment_dict.sentiments = prediction.tolist()[0]
    
    return sentiment_dict

@router.post(
    "/sentiment",
    response_model=SentimentResponseSchema,
)
async def get_sentiment(
  payload: SentimentRequestSchema
):
    start_time = time.time()  

    embedded = process_input(payload.text)

    """ Sentiment Analysis Model """

    prediction = bilstm_model.predict(embedded)

    print("Finished running model...")

    sentiment_dict = show_multiclass_result(prediction, payload.text)

    end_time = time.time()    # Record the end time
    elapsed_time = end_time - start_time  # Calculate elapsed time
    print(f"Time elapsed: {elapsed_time:.6f} seconds")

    sentiment_dict.elapsed_time = elapsed_time
    
    return sentiment_dict


@router.post(
    "/sentiment-svm",
    response_model=SentimentResponseSchema,
)
async def get_sentiment_svm(
  payload: SentimentRequestSchema
):
    start_time = time.time()  

    embedded = process_input(payload.text)

    """ Sentiment Analysis Model """

    prediction = svm_model.predict_proba(embedded)

    print(prediction)

    print("Finished running model...")

    sentiment_dict = show_multiclass_result(prediction, payload.text)

    end_time = time.time()    # Record the end time
    elapsed_time = end_time - start_time  # Calculate elapsed time
    print(f"Time elapsed: {elapsed_time:.6f} seconds")

    sentiment_dict.elapsed_time = elapsed_time
    
    return sentiment_dict


@router.post(
    "/sentiment-knn",
    response_model=SentimentResponseSchema,
)
async def get_sentiment_knn(
  payload: SentimentRequestSchema
):
    start_time = time.time()  

    embedded = process_input(payload.text)

    """ Sentiment Analysis Model """

    prediction = knn_model.predict_proba(embedded)

    print(prediction)

    print("Finished running model...")

    sentiment_dict = show_multiclass_result(prediction, payload.text)

    end_time = time.time()    # Record the end time
    elapsed_time = end_time - start_time  # Calculate elapsed time
    print(f"Time elapsed: {elapsed_time:.6f} seconds")
    
    sentiment_dict.elapsed_time = elapsed_time
    
    return sentiment_dict


@router.post(
    "/sentiment-nb",
    response_model=SentimentResponseSchema,
)
async def get_sentiment_nb(
  payload: SentimentRequestSchema
):
    start_time = time.time()  

    embedded = process_input(payload.text)

    scaler = MinMaxScaler()
    scaled_embedded = scaler.fit_transform(embedded)


    """ Sentiment Analysis Model """

    prediction = nb_model.predict_proba(scaled_embedded)

    print(prediction)

    print("Finished running model...")

    sentiment_dict = show_multiclass_result(prediction, payload.text)

    end_time = time.time()    # Record the end time
    elapsed_time = end_time - start_time  # Calculate elapsed time
    print(f"Time elapsed: {elapsed_time:.6f} seconds")
    
    sentiment_dict.elapsed_time = elapsed_time
    
    return sentiment_dict


@router.post(
    "/sentiment-rf",
    response_model=SentimentResponseSchema,
)
async def get_sentiment_rf(
  payload: SentimentRequestSchema
):
    start_time = time.time()  

    embedded = process_input(payload.text)

    """ Sentiment Analysis Model """

    prediction = rf_model.predict_proba(embedded)

    print(prediction)

    print("Finished running model...")

    sentiment_dict = show_multiclass_result(prediction, payload.text)

    end_time = time.time()    # Record the end time
    elapsed_time = end_time - start_time  # Calculate elapsed time
    print(f"Time elapsed: {elapsed_time:.6f} seconds")
    
    sentiment_dict.elapsed_time = elapsed_time
    
    return sentiment_dict
