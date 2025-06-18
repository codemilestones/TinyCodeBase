#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@File    :   llm.py
@Time    :   2025/06/18 10:00:00
@Author  :   codemilestones
@Version :   1.0
@Desc    :   Base model class
'''
from embeddings import OPENAI_BASE_URL

PROMPT_TEMPLATE = {
    "RAG_PROMPT_TEMPLATE": """先对上下文进行内容总结,再使用上下文来回答用户的问题。总是使用中文回答。
        问题: {question}
        可参考的上下文：
        ···
        {context}
        ···
        如果给定的上下文无法让你做出回答，请回答数据库中没有这个内容，我不知道。
        有用的回答:""",
}

class BaseModel:
    def __init__(self, path: str = '') -> None:
        self.path = path

    def chat(self, prompt: str, history: list[dict], content: str) -> str:
        pass

    def load_model(self):
        pass


class DoubaoLiteModel(BaseModel):
    def __init__(self, path: str = '', model: str = "Doubao-1.5-lite-32k") -> None:
        super().__init__(path)
        self.model = model

    def chat(self, prompt: str, history: list[dict], content: str) -> str:
        from openai import OpenAI
        client = OpenAI(
            api_key="sk-En8qPIGvNTidf5kvE0F44dC4CfC248A384D34428EaF116Bb",
            base_url=OPENAI_BASE_URL
        )
        history.append({'role': 'user', 'content': PROMPT_TEMPLATE['RAG_PROMPT_TEMPLATE'].format(question=prompt, context=content)})
        response = client.chat.completions.create(
            model=self.model,
            messages=history,
            max_tokens=150,
            temperature=0.1
        )
        return response.choices[0].message.content