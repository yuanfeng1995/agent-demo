# -*- coding: utf-8 -*-
from tools import CalcTool, SearchTool


class Agent:
    def __init__(self):
        self.tools = {
            'calc': CalcTool(),
            'search': SearchTool()
        }
    
    def decide(self, user_input):
        # 🔴 第一版：用规则代替 LLM
        if any(op in user_input for op in ['+', '-', '*', '/']):
            return 'calc', user_input
        else:
            return "search", user_input
    
    def run(self, user_input):
        tool_name, tool_input = self.decide(user_input)
        tool = self.tools[tool_name]
        result = tool.run(tool_input)
        return f'[call tool: {tool_name}]->{result}'
    