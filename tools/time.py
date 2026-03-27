# -*- coding: utf-8 -*-
from base import BaseTool
from datetime import datetime

class TimeTool(BaseTool):
    """
    TimeTool 类用于获取当前时间。
    返回当前日期和时间的字符串表示。
    """
    name = 'time'

    def run(self, input_str: str) -> str:
        """
        获取当前时间。

        参数:
        input_str (str): 输入字符串（未使用）。

        返回:
        str: 当前时间的字符串表示。
        """
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")
