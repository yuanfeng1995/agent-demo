# -*- coding: utf-8 -*-
from tools.manager import ToolManager
from tools.calc import CalcTool
from tools.search import SearchTool
from tools.time import TimeTool
from tools.file import FileTool
from llm import LLM
from memory import Memory
import re


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
        self.tool_manager.register(FileTool())

        # 初始化 LLM
        self.llm = LLM()

        # 初始化记忆
        self.memory = Memory()
        self.active_document_path = ""
        self.active_document_content = ""
        self.active_document_summary = ""

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

    # def run(self, user_input):
    #     """
    #     执行用户输入：决定工具，运行工具，返回结果。
    #
    #     参数:
    #     user_input (str): 用户的输入字符串。
    #
    #     返回:
    #     str: 工具执行的结果字符串。
    #     """
    #     # 添加用户输入到记忆
    #     self.memory.add('user', user_input)
    #
    #     tool_name, tool_input = self.decide(user_input)
    #
    #     result = self.tool_manager.execute(tool_name, tool_input)
    #
    #     if tool_name == 'file':
    #         # 如果是文件工具，生成摘要
    #         summary = self.llm.summarize(result)
    #         final_result = f"[调用工具: {tool_name}] → {summary}"
    #     else:
    #         final_result = f"[调用工具: {tool_name}] → {result}"
    #
    #     # 添加助手响应到记忆
    #     self.memory.add('assistant', final_result)
    #
    #     return final_result

    def _is_math_expression(self, text: str) -> bool:
        return re.fullmatch(r"[0-9\.\+\-\*\/\(\)\s]+", text.strip()) is not None

    def _looks_like_tool_command(self, user_input: str) -> bool:
        text = user_input.strip()
        lower_text = text.lower()

        if self._is_math_expression(text):
            return True

        file_pattern = r"\.(txt|md|csv|json|log|pdf|docx?)\b"
        if re.search(file_pattern, lower_text):
            return True

        keywords = [
            "读取", "打开", "分析", "总结", "search", "搜索",
            "calc", "计算", "时间", "几点", "time"
        ]
        return any(k in lower_text for k in keywords)

    def _document_context(self) -> str:
        if not self.active_document_path:
            return ""
        summary = self.active_document_summary or "暂无摘要"
        content = self.active_document_content.strip()
        if len(content) > 4000:
            content = content[:4000] + "\n[文档内容已截断]"
        return (
            f"文档路径: {self.active_document_path}\n"
            f"文档摘要: {summary}\n"
            f"文档内容:\n{content}"
        )

    def run(self, user_input):
        """
        执行用户输入：决定工具，运行工具，返回结果。

        参数:
        user_input (str): 用户的输入字符串。

        返回:
        str: 工具执行的结果字符串。
        """
        # 👉 Step 1: 记录用户输入
        self.memory.add("user", user_input)

        # 有活动文档时，普通追问直接走对话，不再重新选工具。
        if self.active_document_path and not self._looks_like_tool_command(user_input):
            response = self.llm.chat_with_memory(
                user_input,
                self.memory.get(),
                document_context=self._document_context()
            )
            self.memory.add("assistant", response)
            return response

        tools = self.tool_manager.list_tools() + ["chat"]

        # 👉 Step 2: LLM 决策（仍然用于工具调用）
        decision = self.llm.decide_tool(user_input, tools)

        tool_name = decision.get("tool", "chat")
        tool_input = decision.get("input", user_input)

        if tool_name == "chat":
            response = self.llm.chat_with_memory(
                user_input,
                self.memory.get(),
                document_context=self._document_context()
            )
            self.memory.add("assistant", response)
            return response

        tool_result = self.tool_manager.execute(tool_name, str(tool_input))

        # 👉 Step 3: 如果是 file，走总结
        if tool_name == "file":
            if isinstance(tool_result, dict) and tool_result.get("ok"):
                content = str(tool_result.get("content", ""))
                self.active_document_path = str(tool_result.get("path", ""))
                self.active_document_content = content
                self.active_document_summary = self.llm.summarize(content)
                response = self.active_document_summary
            elif isinstance(tool_result, dict):
                response = str(tool_result.get("error", "文件处理失败。"))
            else:
                response = "文件工具返回格式异常。"
        else:
            # 👉 Step 4: 普通对话（带 memory）
            response = self.llm.chat_with_memory(
                f"用户问题：{user_input}\n工具结果：{tool_result}",
                self.memory.get(),
                document_context=self._document_context()
            )

        # 👉 Step 5: 记录AI输出
        self.memory.add("assistant", response)

        return response
