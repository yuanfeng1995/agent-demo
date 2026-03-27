# -*- coding: utf-8 -*-
from .base import BaseTool
import os


class FileTool(BaseTool):
    """
    FileTool 类用于读取文件内容。
    给定文件路径，返回文件的内容。
    """
    name = 'file'

    def run(self, input_str: str) -> dict:
        """
        读取指定文件的内容。

        参数:
        input_str (str): 文件路径。

        返回:
        dict: 包含 ok/path/content 或 ok/path/error 的结构化结果。
        """
        path = input_str.strip()
        if not os.path.exists(path):
            return {
                "ok": False,
                "path": path,
                "error": f"文件 '{path}' 不存在。"
            }
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            return {
                "ok": True,
                "path": path,
                "content": content
            }
        except Exception as e:
            return {
                "ok": False,
                "path": path,
                "error": f"读取文件 '{path}' 时出错: {str(e)}"
            }
