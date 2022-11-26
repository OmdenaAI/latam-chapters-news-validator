import logging
from jsonformatter import JsonFormatter
import os
import torch
from transformers import AutoTokenizer
import onnxruntime as ort
from pydantic import BaseModel

#
# Models for predict requests
#

class PredictInput(BaseModel):
    text: str

class PredictResponse(BaseModel):
    text: str = None
    label: str = None
    status: str

#
# Helper classes and functions
#

format = '''{
    "level":           "levelname",
    "logger_name":     "%(name)s.%(funcName)s",
    "timestamp":       "asctime",
    "message":         "message"
}'''

def get_logger(name: str, level: int = logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    formatter = JsonFormatter(format)

    logHandler = logging.StreamHandler()
    logHandler.setFormatter(formatter)
    logHandler.setLevel(level)

    logger.addHandler(logHandler)
    return logger

class SKLearnWrapper:
    def __init__(self, tokenizer=None, st_model=None, clf=None):
        self.tokenizer = tokenizer
        self.st_model = st_model
        self.clf = clf
    
    def mean_pooling(self, model_output, attention_mask):
        token_embeddings = torch.from_numpy(model_output)
        attention_mask = torch.from_numpy(attention_mask)
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        return sum_embeddings / sum_mask
    
    def encode(self, tokenized_sentences):
        """
        'tokenized_sentences' is of type transformers.tokenization_utils_base.BatchEncoding
        but onnxruntime expects a python dict obtained by 'tokenized_sentences.data'
        """
        embeddings = self.st_model.run(None, tokenized_sentences.data)
        pooled_embeddings = self.mean_pooling(embeddings[0], tokenized_sentences["attention_mask"])
        return pooled_embeddings
    
    def predict_head(self, embeddings):
        """
        Predict class with skl2onnx scikit-learn model
        """
        input_name = self.clf.get_inputs()[0].name
        label_name = self.clf.get_outputs()[0].name
        predicted_classes = self.clf.run([label_name], {input_name: embeddings.numpy()})[0]
        return predicted_classes

    def predict(self, sentences):
        """
        Full prediction pipeline
        """
        inputs = self.tokenizer(sentences, padding=True, truncation=True, return_tensors='np')
        embeddings = self.encode(inputs)
        return self.predict_head(embeddings)

    def load(self, path):
        self.tokenizer = AutoTokenizer.from_pretrained(path)
        self.st_model = ort.InferenceSession(os.path.join(path, "model.onnx"), providers=['CPUExecutionProvider'])
        self.clf = ort.InferenceSession(os.path.join(path, "model_head.onnx"))

class SetFitPipeline:
    def __init__(self, model_name_or_path) -> None:
        base_model = SKLearnWrapper()
        base_model.load(model_name_or_path)
        self.model = base_model

    def __call__(self, inputs, *args, **kwargs):
        model_outputs = self.model.predict(inputs)
        return model_outputs
