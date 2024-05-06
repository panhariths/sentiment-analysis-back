import numpy as np
from khmernltk import word_tokenize

import sys
sys.path.append("/Users/panharithsun/Documents/fyp_demo/FastAPI-template")

from sentiment_model.bert_khmer import BERTKhmerEmbedder
from sentiment_model.sa_model import SAModel
from sentiment_model.preprocessing import preprocess

if __name__ == "__main__":
    
    """ Text input """

    input_text = "សាំងវិចឆ្ងាញ់ តែបើគ្មានការចុះតម្លៃទេ តម្លៃគិតទៅរាងថ្លៃបន្តិច"

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

