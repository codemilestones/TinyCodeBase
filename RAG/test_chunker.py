
#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@File    :   test_chunker.py
@Time    :   2025/06/18 10:00:00
@Author  :   codemilestones
@Version :   1.0
@Desc    :   Test the chunker pipeline, you could test the codebase with https://github.com/datawhalechina/tiny-universe/
'''

from chunker_code import split_to_segmenmt
from chunker_text import ReadFiles

if __name__ == "__main__":
    code_docs = split_to_segmenmt("~/workspace/tiny-universe", cover_content=150)

    for doc in code_docs[:10]:
        print(doc.path, "\n")
        print(doc.index, "\n")
        print(doc.content, "\n")
        print("-"*100)

    docs = ReadFiles('~/workspace/tiny-universe').get_content(max_token_len=600, cover_content=150)

    for doc in docs[:10]:
        print(doc, "\n")
        print("-"*100)
