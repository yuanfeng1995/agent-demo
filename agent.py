# -*- coding: utf-8 -*-
from tools.manager import ToolManager
from tools.calc import CalcTool
from tools.search import SearchTool
from tools.time import TimeTool
from llm import LLM


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

        # 初始化 LLM
        self.llm = LLM()

    def decide(self, user_input):
        """
        根据用户输入决定使用哪个工具。
        使用 LLM 代替规则来决定工具。

        参数:
        user_input (str): 用户的输入字符串。

        返回:
        tuple: (工具名称, 工具输入)
        """
        tools = self.tool_manager.list_tools()
        result = self.llm.decide_tool(user_input, tools)
        return result['tool'], result['input']

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