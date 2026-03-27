# -*- coding: utf-8 -*-
from tools.manager import ToolManager
from tools.calc import CalcTool
from tools.search import SearchTool
from tools.time import TimeTool


class Agent:
    """
    Agent 类用于模拟一个简单的代理，根据用户输入决定使用哪个工具并执行。
    """

    def __init__(self):
        """
        初始化 Agent 实例。
        创建工具字典，包含计算和搜索工具。
        """
        self.tool_manager = ToolManager()

        # 注册工具
        self.tool_manager.register(CalcTool())
        self.tool_manager.register(SearchTool())
        self.tool_manager.register(TimeTool())

    def decide(self, user_input):
        """
        根据用户输入决定使用哪个工具。
        第一版：用规则代替 LLM，如果输入包含运算符则使用计算工具，否则使用搜索工具。

        参数:
        user_input (str): 用户的输入字符串。

        返回:
        tuple: (工具名称, 工具输入)
        """
        if any(op in user_input for op in ["+", "-", "*", "/"]):
            return "calc", user_input
        elif "时间" in user_input or "time" in user_input.lower():
            return "time", user_input
        else:
            return "search", user_input

    def run(self, user_input):
        """
        执行用户输入：决定工具，运行工具，返回结果。

        参数:
        user_input (str): 用户的输入字符串。

        返回:
        str: 工具执行的结果字符串。
        """
        tool_name, tool_input = self.decide(user_input)

        result = self.tool_manager.execute(tool_name, tool_input)

        return f"[调用工具: {tool_name}] → {result}"