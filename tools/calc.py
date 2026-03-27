# -*- coding: utf-8 -*-
from .base import BaseTool
class CalcTool(BaseTool):
    """
    CalcTool 类用于执行简单的数学计算。
    使用 eval 函数计算输入的表达式。
    """
    name = 'calc'

    def run(self, input_str: str) -> str:
        """
        执行数学计算。

        参数:
        input_str (str): 数学表达式字符串。

        返回:
        str: 计算结果的字符串表示，如果失败则返回错误消息。
        """
        try:
            return str(eval(input_str))
        except:
            return 'Calc failed'
