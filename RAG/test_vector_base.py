#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@File    :   test_vector_base.py
@Time    :   2025/06/18 10:00:00
@Author  :   codemilestones
@Version :   1.0
@Desc    :   Test the vector base pipeline
'''

from vector_base import VectorStore
from embeddings import OpenAIEmbedding
from chunker_code import split_to_segmenmt
from chunker_text import ReadFiles

if __name__ == "__main__":

    code_docs = split_to_segmenmt("~/workspace/tiny-universe", cover_content=50)
    text_docs = ReadFiles('~/workspace/tiny-universe').get_content(max_token_len=600, cover_content=150)

    # Extract content strings from Documents objects
    doc_contents = [doc.content for doc in code_docs] + text_docs

    vector_store = VectorStore(document=doc_contents)

    if not vector_store.load_vector():
        vector_store.get_vector(OpenAIEmbedding())
        vector_store.persist()

    for doc in vector_store.query("RAG 的组成部分是那些?", OpenAIEmbedding(), 3):
        print(doc)
        print("-"*100)