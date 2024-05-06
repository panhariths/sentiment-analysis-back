import torch
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub

import sys
sys.path.append("/Users/panharithsun/Documents/fyp_demo/FastAPI-template")

from sentiment_model.full_tokenizer import FullTokenizer

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class BERTKhmerEmbedder(object):
    def __init__(
        self,
        model_path="/Users/panharithsun/Documents/fyp_demo/FastAPI-template/sentiment_model/bert_module_khmer",
        vocab_size=167896,
        vocab_path="/Users/panharithsun/Documents/fyp_demo/FastAPI-template/sentiment_model/bert_module_khmer/assets/vocab_file_BERT_.txt",
        **kwarg
    ):
        super().__init__()
        self.model = hub.load(model_path)
        self.tokenizer = FullTokenizer(vocab_file=vocab_path, do_lower_case=True)

    def insert_special_tokens(self, tokens):
        classification_token = "[CLS]"
        separator_token = "[SEP]"

        tokens.insert(0, classification_token)
        tokens.append(separator_token)

        return tokens

    def tokens_to_indexes(self, tokens):

        formatted_tokens = self.insert_special_tokens(tokens)
        indexed_tokens = self.tokenizer.convert_tokens_to_ids(formatted_tokens)

        return indexed_tokens

    def convert_sentence_to_features(self, tokens_list, max_seq_len):
        tokens = ["[CLS]"]
        tokens.extend(tokens_list)
        if len(tokens) > max_seq_len - 1:
            tokens = tokens[: max_seq_len - 1]
        tokens.append("[SEP]")

        input_ids = self.tokenizer.convert_tokens_to_ids(tokens)
        input_mask = [1] * len(input_ids)
        segment_ids = [0] * len(input_ids)

        zero_padding = [0] * (max_seq_len - len(input_ids))

        input_ids.extend(zero_padding)
        input_mask.extend(zero_padding)
        segment_ids.extend(zero_padding)

        return input_ids, input_mask, segment_ids

    def convert_sentences_to_features(self, tokens_list, max_seq_len=64):
        all_input_ids = []
        all_input_mask = []
        all_segment_ids = []

        for tokens in tokens_list:
            input_ids, input_mask, segment_ids = self.convert_sentence_to_features(
                tokens, max_seq_len
            )
            all_input_ids.append(input_ids)
            all_input_mask.append(input_mask)
            all_segment_ids.append(segment_ids)

        return all_input_ids, all_input_mask, all_segment_ids

    def extract_word_embeddings(self, tokens_list, batch_size=512, max_seq_len=64, **kwargs):

        input_ids_vals, input_mask_vals, segment_ids_vals = (
            self.convert_sentences_to_features(tokens_list, max_seq_len)
        )

        # Create a TensorFlow dataset from the input tensors
        dataset = tf.data.Dataset.from_tensor_slices((input_ids_vals, input_mask_vals, segment_ids_vals))
        dataset = dataset.batch(batch_size)

        pooled_embeddings = []

        for input_ids_batch, input_mask_batch, segment_ids_batch in dataset:
            # Get the BERT outputs
            bert_outputs = self.model.signatures['tokens'](input_ids=input_ids_batch, input_mask=input_mask_batch, segment_ids=segment_ids_batch)

            # Append the pooled embeddings to the list
            pooled_embeddings.append(bert_outputs['pooled_output'].numpy())

        return np.concatenate(pooled_embeddings, axis=0)
