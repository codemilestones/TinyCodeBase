#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@File    :   agent_llm.py
@Time    :   2025/06/24 10:00:00
@Author  :   codemilestones
@Version :   1.0
@Desc    :   Agent LLM
'''
OPENAI_BASE_URL = "https://aihubmix.com/v1"


class AgentLLM:
    def __init__(self, path: str = '', model: str = "Doubao-1.5-lite-32k") -> None:
        self.model = model

    def chat(self, prompt: str, history: list[dict], meta_instruction: str) -> tuple[str, list[dict]]:
        from openai import OpenAI
        client = OpenAI(
            api_key="sk-En8qPIGvNTidf5kvE0F44dC4CfC248A384D34428EaF116Bb",
            base_url=OPENAI_BASE_URL
        )

        messages = []
        if meta_instruction:
            messages.append({"role": "system", "content": meta_instruction})
        for entry in history:
            messages.append(entry)
        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.1
        )

        ai_response = response.choices[0].message.content
        new_history = history.copy()
        new_history.append({"role": "user", "content": prompt})
        new_history.append({"role": "assistant", "content": ai_response})

        return ai_response, new_history