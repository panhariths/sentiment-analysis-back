from fastapi import APIRouter
from typing import Optional
from pydantic import BaseModel
import pickle
import time

import numpy as np
from khmernltk import word_tokenize

import sys
sys.path.append("/Users/panharithsun/Documents/fyp_demo/FastAPI-template")

from sentiment_model.bert_khmer import BERTKhmerEmbedder
from sentiment_model.sa_model import SAModel
from sentiment_model.preprocessing import preprocess

class SentimentResponseSchema(BaseModel):
    sentiments: Optional[list[float]] = []
class SentimentRequestSchema(BaseModel):
    text: str

router = APIRouter()

@router.post(
    "/sentiment",
    response_model=SentimentResponseSchema,
    # responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_sentiment(
  payload: SentimentRequestSchema
):
    start_time = time.time()  
    
    """ Text input """

    input_text = payload.text

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

    """ Sentiment Analysis Model """

    model = SAModel()
    prediction = model.predict(embedded)

    print("Finished running model...")

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

    end_time = time.time()    # Record the end time
    elapsed_time = end_time - start_time  # Calculate elapsed time
    print(f"Time elapsed: {elapsed_time:.6f} seconds")
    
    return sentiment_dict


@router.post(
    "/sentiment-svm",
    response_model=SentimentResponseSchema,
    # responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_sentiment_svm(
  payload: SentimentRequestSchema
):
    start_time = time.time()  
    
    """ Text input """

    input_text = payload.text

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

    """ Sentiment Analysis Model """

    with open('/Users/panharithsun/Documents/fyp_demo/FastAPI-template/sentiment_model/sentiment_svm_proba.pkl', 'rb') as f:
        model = pickle.load(f)
    prediction = model.predict_proba(embedded)

    print(prediction)

    print("Finished running model...")

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

    end_time = time.time()    # Record the end time
    elapsed_time = end_time - start_time  # Calculate elapsed time
    print(f"Time elapsed: {elapsed_time:.6f} seconds")
    
    return sentiment_dict
