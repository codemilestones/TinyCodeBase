
#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@File    :   test_chunker.py
@Time    :   2025/06/18 10:00:00
@Author  :   codemilestones
@Version :   1.0
@Desc    :   Test the chunker pipeline
'''

from chunker_code import split_to_segmenmt
from chunker_text import ReadFiles

if __name__ == "__main__":
    code_docs = split_to_segmenmt("/Users/lizhe/SEO/workspace/codev-backend", cover_content=150)

    for doc in code_docs[:10]:
        print(doc.path, "\n")
        print(doc.index, "\n")
        print(doc.content, "\n")
        print("-"*100)

    docs = ReadFiles('/Users/lizhe/SEO/workspace/codev-backend').get_content(max_token_len=600, cover_content=150)

    for doc in docs:
        print(doc, "\n")
        print("-"*100)
