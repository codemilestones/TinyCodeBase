#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@File    :   tiny_code_rag.py
@Time    :   2025/06/18 10:00:00
@Author  :   codemilestones
@Version :   1.0
@Desc    :   RAG pipeline for tiny codebase
'''

from llm import DoubaoLiteModel
from vector_base import VectorStore
from chunker_code import split_to_segmenmt
from chunker_text import ReadFiles
from embeddings import OpenAIEmbedding

if __name__ == "__main__":
    ## 1. prepare the data
    code_docs = split_to_segmenmt("~/workspace/tiny-universe", cover_content=50)
    text_docs = ReadFiles('~/workspace/tiny-universe').get_content(max_token_len=600, cover_content=150)

    # Extract content strings from Documents objects
    doc_contents = [doc.content for doc in code_docs] + text_docs

    vector_store = VectorStore(document=doc_contents)

    # get the vector
    if not vector_store.load_vector():
        vector_store.get_vector(OpenAIEmbedding())
        vector_store.persist()

    # 2. get the llm model
    model = DoubaoLiteModel()

    # 3. wite user input, this is the main loop, with history
    history = []
    while True:
        user_input = input("请输入问题(输入exit退出): ")
        if user_input == "exit":
            break
        contents = vector_store.query(user_input, OpenAIEmbedding(), 3)
        response = model.chat(user_input, history, "\n".join(contents))
        print(response)
        print("-"*100)
        print("\n")
        history.append({'role': 'user', 'content': user_input})
        history.append({'role': 'assistant', 'content': response})