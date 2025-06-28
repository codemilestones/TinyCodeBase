#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@File    :   tools.py
@Time    :   2025/06/24 10:00:00
@Author  :   codemilestones
@Version :   1.0
@Desc    :   Tools, 提供多种工具类
'''

import os, json
import requests

from tree_sitter_parser import check_code

class Tools:
    def __init__(self) -> None:
        self.toolConfig = self._tools()
    
    def _tools(self):
        tools = [
            {
                'name_for_human': '谷歌搜索',
                'name_for_model': 'google_search',
                'description_for_model': '谷歌搜索是一个通用搜索引擎，可用于访问互联网、查询百科知识、了解时事新闻等。',
                'parameters': [
                    {
                        'name': 'search_query',
                        'description': '搜索关键词或短语',
                        'required': True,
                        'schema': {'type': 'string'},
                    }
                ],
            },
            {
                'name_for_human': '代码检查',
                'name_for_model': 'code_check',
                'description_for_model': '代码检查是一个代码检查工具，可用于检查代码的错误和问题。',
                'parameters': [
                    {
                        'name': 'language',
                        'description': '语言类型全称',
                        'required': True,
                        'schema': {'type': 'string'},
                    },
                    {
                        'name': 'source_code',
                        'description': '源代码',
                        'required': True,
                        'schema': {'type': 'string'},
                    }
                ]
            }
        ]
        return tools

    def google_search(self, search_query: str):
        url = "https://google.serper.dev/search"

        payload = json.dumps({"q": search_query})
        headers = {
            'X-API-KEY': '4c6e90b1d8092ba79cbb85bee45ec17693976a58',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload).json()

        return response['organic'][0]['snippet']

    def code_check(self, language: str, source_code: str):
        return check_code(language, source_code)

