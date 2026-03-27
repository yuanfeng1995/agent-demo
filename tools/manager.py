# -*- coding: utf-8 -*-
class ToolManager:
    """
    ToolManager 类用于管理工具的注册、执行和列出。
    它维护一个工具字典，支持动态注册工具并执行它们。
    """
    def __init__(self):
        """
        初始化 ToolManager 实例。
        创建一个空的工具字典。
        """
        self.tools = {}

    def register(self, tool):
        """
        注册一个工具到工具管理器中。

        参数:
        tool: 要注册的工具对象，必须有 name 属性。
        """
        self.tools[tool.name] = tool

    def execute(self, name, input_str):
        """
        根据名称执行指定的工具。

        参数:
        name (str): 工具的名称。
        input_str: 传递给工具的输入字符串。

        返回:
        str: 工具执行的结果，如果工具不存在则返回错误消息。
        """
        if name not in self.tools:
            return f"工具 {name} 不存在"
        return self.tools[name].run(input_str)

    def list_tools(self):
        """
        列出所有已注册工具的名称。

        返回:
        list: 工具名称的列表。
        """
        return list(self.tools.keys())