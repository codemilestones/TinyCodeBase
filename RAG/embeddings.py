#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@File    :   embeddings.py
@Time    :   2025/06/18 10:00:00
@Author  :   codemilestones
@Version :   1.0
@Desc    :   None
'''

import os
from copy import copy
from typing import Dict, List, Optional, Tuple, Union
import numpy as np

os.environ['CURL_CA_BUNDLE'] = ''
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())


class BaseEmbeddings:
    """
    Base class for embeddings
    """
    def __init__(self, path: str, is_api: bool) -> None:
        self.path = path
        self.is_api = is_api
    
    def get_embedding(self, text: str, model: str) -> List[float]:
        raise NotImplementedError
    
    @classmethod
    def cosine_similarity(cls, vector1: List[float], vector2: List[float]) -> float:
        """
        calculate cosine similarity between two vectors
        """
        dot_product = np.dot(vector1, vector2)
        magnitude = np.linalg.norm(vector1) * np.linalg.norm(vector2)
        if not magnitude:
            return 0
        return dot_product / magnitude

OPENAI_API_KEY = "sk-gZZFW6G63FCG3LvoFe700862425e4aF2BbC49495443e93B5"
OPENAI_BASE_URL = "https://aihubmix.com/v1"

class OpenAIEmbedding(BaseEmbeddings):
    """
    class for OpenAI embeddings
    """
    def __init__(self, path: str = '', is_api: bool = True) -> None:
        super().__init__(path, is_api)
        if self.is_api:
            from openai import OpenAI
            self.client = OpenAI(
                api_key=OPENAI_API_KEY,
                base_url=OPENAI_BASE_URL
            )
    
    def get_embedding(self, text: str, model: str = "text-embedding-3-small") -> List[float]:
        if self.is_api:
            text = text.replace("\n", " ")
            return self.client.embeddings.create(input=[text], model=model).data[0].embedding
        else:
            raise NotImplementedError