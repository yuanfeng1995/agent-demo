# -*- coding: utf-8 -*-
from openai import OpenAI
import json
from typing import List, Dict, Any
import os
import re


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
        supported_tools = list(tools)
        if "chat" not in supported_tools:
            supported_tools.append("chat")

        # 生成工具描述
        tool_desc = "\n".join([f"- {name}" for name in supported_tools])

        # 构建系统提示
        system_prompt = (
            "你是一个AI助手，需要选择合适的工具。\n\n"
            "可用工具：\n" + tool_desc + "\n\n"
            "规则：\n"
            "1) 只有在用户明确要求读文件、计算、搜索、查时间时才调用工具。\n"
            "2) 如果是对上一轮内容的追问或普通对话，选择 chat。\n"
            "3) tool 只能是可用工具之一。\n\n"
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
            return {"tool": "chat", "input": user_input}

        content = response.choices[0].message.content

        # 解析 JSON 响应
        if content is None:
            return {"tool": "chat", "input": user_input}
        try:
            clean = content.strip()
            # 兼容 ```json ... ``` 包裹
            clean = re.sub(r"^```(?:json)?\s*", "", clean)
            clean = re.sub(r"\s*```$", "", clean)
            result = json.loads(clean)
            tool = result.get("tool", "chat")
            tool_input = result.get("input", user_input)
            if tool not in supported_tools:
                tool = "chat"
                tool_input = user_input
            return {"tool": tool, "input": tool_input}
        except json.JSONDecodeError:
            # 如果解析失败，返回默认值
            return {"tool": "chat", "input": user_input}

    def summarize(self, document: str) -> str:
        """
        使用 LLM 生成文档的摘要。

        参数:
        document (str): 要摘要的文档内容。

        返回:
        str: 文档的摘要。
        """
        # 构建系统提示
        system_prompt = (
            "你是一个AI助手，负责生成文档的简洁摘要。\n"
            "请提供一个简短、准确的摘要，突出主要观点。"
        )

        # 调用 OpenAI API
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",  # DeepSeek 聊天模型
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"请摘要以下文档：\n\n{document}"}
                ]
            )
        except Exception as e:
            # 如果 API 调用失败，返回错误信息
            return f"摘要生成失败: {e}"

        content = response.choices[0].message.content

        # 返回摘要内容
        return content if content else "无法生成摘要。"

    def chat_with_memory(
        self,
        user_input: str,
        memory: List[Dict[str, Any]],
        document_context: str = ""
    ) -> str:
        """
        使用记忆进行聊天。

        参数:
        user_input (str): 用户的输入。
        memory (List[Dict[str, Any]]): 对话历史。

        返回:
        str: 聊天响应。
        """
        # 构建消息列表
        messages: List[Dict[str, Any]] = []
        if document_context:
            messages.append({
                "role": "system",
                "content": (
                    "以下是当前正在讨论的文档上下文，请优先基于它回答：\n"
                    f"{document_context}"
                )
            })
        messages.extend(memory)
        messages.append({"role": "user", "content": user_input})

        # 调用 OpenAI API
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",  # DeepSeek 聊天模型
                messages=messages
            )
        except Exception as e:
            # 如果 API 调用失败，返回错误信息
            return f"聊天失败: {e}"

        content = response.choices[0].message.content

        # 返回聊天内容
        return content if content else "无法生成响应。"
