#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@File    :   chunker.py
@Time    :   2025/06/18 10:00:00
@Author  :   codemilestones
@Version :   1.0
@Desc    :   Chunker for the RAG pipeline
'''

import os
from os.path import split

from tree_sitter import Tree
from tree_sitter import Node
from tree_sitter_languages import get_language, get_parser

from dataclasses import dataclass, field
import re


def get_line_number(index: int, source_code: str) -> int:
    total_chars = 0
    for line_number, line in enumerate(source_code.splitlines(keepends=True), start=1):
        total_chars += len(line)
        if total_chars > index:
            return line_number - 1
    return line_number


def char_len(s: str) -> int:  # old len function
    return len(s)


# def non_whitespace_len(s: str) -> int: # new len function
#     return len(re.sub("\s", "", s))

def non_whitespace_len(s):
    # Decode if it's bytes
    if isinstance(s, bytes):
        s = s.decode('utf-8')  # or the correct encoding for your use case
    return len(re.sub(r"\s", "", s))  # Use 'r' prefix for raw string


@dataclass
class Span:
    start: int
    end: int

    def extract(self, s: str) -> str:
        return s[self.start: self.end]

    # extract the lines of the chunk, and cover the content before and after the chunk
    def extract_lines(self, s: str, cover_content: int = 150) -> str:
        lines = s.splitlines()
        before_lines = lines[:self.start][::-1]  # Reverse the lines
        before_chunk = []
        chunk_len = 0
        # Get before context

        for line in before_lines:
            chunk_len += len(line)
            if chunk_len >= cover_content:
                break
            before_chunk.append(line)
        before_chunk.reverse()  # Restore original order
            
        # Get after context
        after_lines = lines[self.end:]
        after_chunk = []
        chunk_len = 0
        for line in after_lines:
            chunk_len += len(line)
            if chunk_len >= cover_content:
                break
            after_chunk.append(line)
        chunk = lines[self.start:self.end]
        return "\n".join(before_chunk + chunk + after_chunk)

    def __add__(self, other):
        if isinstance(other, int):
            return Span(self.start + other, self.end + other)
        elif isinstance(other, Span):
            return Span(self.start, other.end)
        else:
            raise NotImplementedError()

    def __len__(self) -> int:
        return self.end - self.start


def chunker(
        tree: Tree,
        source_code: str,
        MAX_CHARS=512 * 5,
        coalesce=150  # Any chunk less than 50 characters long gets coalesced with the next chunk
) -> list[Span]:
    # 1. Recursively form chunks based on the last post (https://docs.sweep.dev/blogs/chunking-2m-files)
    def chunk_node(node: Node) -> list[Span]:
        chunks: list[Span] = []
        current_chunk: Span = Span(node.start_byte, node.start_byte)
        node_children = node.children
        for child in node_children:
            if child.end_byte - child.start_byte > MAX_CHARS:
                chunks.append(current_chunk)
                current_chunk = Span(child.end_byte, child.end_byte)
                chunks.extend(chunk_node(child))
            elif child.end_byte - child.start_byte + len(current_chunk) > MAX_CHARS:
                chunks.append(current_chunk)
                current_chunk = Span(child.start_byte, child.end_byte)
            else:
                current_chunk += Span(child.start_byte, child.end_byte)
        chunks.append(current_chunk)
        return chunks

    chunks = chunk_node(tree.root_node)

    # 2. Filling in the gaps
    for prev, curr in zip(chunks[:-1], chunks[1:]):
        prev.end = curr.start
        curr.start = tree.root_node.end_byte

    # 3. Combining small chunks with bigger ones
    new_chunks = []
    current_chunk = Span(0, 0)
    for chunk in chunks:
        current_chunk += chunk
        if non_whitespace_len(current_chunk.extract(source_code)) > coalesce \
                and "\n" in current_chunk.extract(source_code):
            new_chunks.append(current_chunk)
            current_chunk = Span(chunk.end, chunk.end)
    if len(current_chunk) > 0:
        new_chunks.append(current_chunk)

    # 4. Changing line numbers
    line_chunks = [Span(get_line_number(chunk.start, source_code),
                        get_line_number(chunk.end, source_code)) for chunk in new_chunks]

    # 5. Eliminating empty chunks
    line_chunks = [chunk for chunk in line_chunks if len(chunk) > 0]

    return line_chunks


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径


def remove_import(content: str):
    content = re.sub(r'import {(.|\n)*} from.*[^\n]+\n', '', content)  # remove import from
    content = re.sub(r'import [^\n]+\n', '', content)  # remove import
    return content


def is_thrift(content: str):
    return content.startswith('''/**
 * Autogenerated by Thrift Compiler (0.9.3)
 *
 * DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
 *  @generated
 */''')

class Documents:
    """
        获取已分好类的文档
    """
    def __init__(self, path: str = '', index: int = 0, content: str = '') -> None:
        self.path = path
        self.index = index
        self.content = content

def split_to_segmenmt(project_name: str, max_chars: int = 512 * 5, cover_content: int = 150) -> list[Documents]:
    suffix = ("java", "html", "css", "js", "vue", "ts", "jsx", "tsx", "swift", "kt", "vue")

    documents = []

    suffix_map = {
        "java": "java",
        "html": "html",
        "css": "css",
        "js": "javascript",
        "ts": "typescript",
        "tsx": "tsx",
        "kt": "kotlin",
        "vue": "typescript",
    }
    parse_map = {}
    for i in suffix_map.values():
        parse_map[i] = get_parser(i)
    for root, dirs, files in os.walk(project_name):
        for file in files:
            suf = file.split('.')[-1]
            if suf in suffix:
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    # new_root = root.replace(project_name, 'segment/' + project_name, 1)
                    # mkdir(new_root)
                    content = f.read()
                    if is_thrift(content):
                        continue
                    content = remove_import(content)
                    content_bytes = bytes(content, 'UTF-8')
                    parser = parse_map[suffix_map[suf]]
                    tree = parser.parse(content_bytes)
                    segment = 0
                    for chunk in chunker(tree, content, max_chars):
                        new_content = chunk.extract_lines(content, cover_content)
                        documents.append(Documents(path=os.path.join(root, file), index=segment, content=new_content))
                        segment += 1

    return documents

