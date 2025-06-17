#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@File    :   test_embeddings.py
@Time    :   2025/06/18 10:00:00
@Author  :   codemilestones
@Version :   1.0
@Desc    :   Test the embeddings pipeline
'''

from embeddings import OpenAIEmbedding

if __name__ == "__main__":
    embedding = OpenAIEmbedding()

    test_text_1 = "Hello, world! This is a test."
    test_embedding_1 = embedding.get_embedding(test_text_1)

    print("test_embedding_1 length: ", len(test_embedding_1), "text length: ", len(test_text_1))

    test_text_2 = "Hello, world! This is a embedding test."
    test_embedding_2 = embedding.get_embedding(test_text_2)

    print("test_embedding_2 length: ", len(test_embedding_2), "text length: ", len(test_text_2))

    print("cosine similarity 1 to 2: ", OpenAIEmbedding.cosine_similarity(test_embedding_1, test_embedding_2))
    
    test_text_3 = "I want to study how to use the embedding model."
    test_embedding_3 = embedding.get_embedding(test_text_3)

    print("test_embedding_3 length: ", len(test_embedding_3), "text length: ", len(test_text_3))

    print("cosine similarity 1 to 3: ", OpenAIEmbedding.cosine_similarity(test_embedding_1, test_embedding_3))
    
    test_text_long = '''
Retrieval augmented generation (RAG) is an architecture for optimizing the performance of an artificial intelligence (AI) model by connecting it with external knowledge bases. RAG helps large language models (LLMs) deliver more relevant responses at a higher quality.

Generative AI (gen AI) models are trained on large datasets and refer to this information to generate outputs. However, training datasets are finite and limited to the information the AI developer can access—public domain works, internet articles, social media content and other publicly accessible data.

RAG allows generative AI models to access additional external knowledge bases, such as internal organizational data, scholarly journals and specialized datasets. By integrating relevant information into the generation process, chatbots and other natural language processing (NLP) tools can create more accurate domain-specific content without needing further training.

'''
    test_embedding_long = embedding.get_embedding(test_text_long)

    print("test_embedding_long length: ", len(test_embedding_long), "text length: ", len(test_text_long))

    print("cosine similarity 1 to long: ", OpenAIEmbedding.cosine_similarity(test_embedding_1, test_embedding_long))