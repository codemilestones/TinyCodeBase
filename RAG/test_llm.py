#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@File    :   test_llm.py
@Time    :   2025/06/18 10:00:00
@Author  :   codemilestones
@Version :   1.0
@Desc    :   Test the llm pipeline
'''

from llm import DoubaoLiteModel

if __name__ == "__main__":
    model = DoubaoLiteModel()
    print(model.chat("大模型是什么？", [], ""))