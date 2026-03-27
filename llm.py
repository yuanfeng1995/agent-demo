# -*- coding: utf-8 -*-
from openai import OpenAI
import json
from typing import List, Dict, Any
import os


class LLM:
    """
    LLM 类用于与 DeepSeek API 交互，决定使用哪个工具。
    """

    def __init__(self, api_key: str = None, base_url: str = "https://api.deepseek.com"):
        """
        初始化 LLM 实例。

        参数:
        api_key (str, optional): DeepSeek API 密钥。如果未提供，从环境变量 DEEPSEEK_API_KEY 获取。
        base_url (str): DeepSeek API 基础 URL。
        """
        if api_key is None:
            api_key = os.getenv('DEEPSEEK_API_KEY')  # type: ignore
            if api_key is None:
                raise ValueError("DEEPSEEK_API_KEY environment variable is not set")
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def decide_tool(self, user_input: str, tools: List[str]) -> Dict[str, Any]:
        """
        根据用户输入和可用工具，使用 LLM 决定使用哪个工具。

        参数:
        user_input (str): 用户的输入字符串。
        tools (List[str]): 可用工具名称的列表。

        返回:
        Dict[str, Any]: 包含 "tool" 和 "input" 的字典。
        """
        # 生成工具描述
        tool_desc = "\n".join([f"- {name}" for name in tools])

        # 构建系统提示
        system_prompt = (
            "你是一个AI助手，需要选择合适的工具。\n\n"
            "可用工具：\n" + tool_desc + "\n\n"
            "请返回JSON格式：\n"
            "{\n"
            "  \"tool\": \"工具名称\",\n"
            "  \"input\": \"传递给工具的输入\"\n"
            "}"
        )

        # 调用 OpenAI API
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",  # DeepSeek 聊天模型
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ]
            )
        except Exception as e:
            # 如果 API 调用失败，返回默认值
            print(f"API 调用失败: {e}")
            return {"tool": "search", "input": user_input}

        content = response.choices[0].message.content

        # 解析 JSON 响应
        if content is None:
            return {"tool": "search", "input": user_input}
        try:
            result = json.loads(content)
            return result
        except json.JSONDecodeError:
            # 如果解析失败，返回默认值
            return {"tool": "search", "input": user_input}