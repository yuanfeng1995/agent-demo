# -*- coding: utf-8 -*-
from typing import List, Dict, Any


class Memory:
    """
    Memory 类用于缓存对话上下文。
    存储消息历史，支持添加和获取上下文。
    """

    def __init__(self, max_history: int = 100):
        """
        初始化 Memory 实例。
        创建一个空的上下文列表。

        参数:
        max_history (int): 最大缓存消息数量，防止内存和 token 消耗过多。
        """
        self.context: List[Dict[str, Any]] = []
        self.max_history = max_history

    def add(self, role: str, content: str):
        """
        添加一条消息到上下文。

        参数:
        role (str): 消息角色，如 'user', 'assistant', 'system'。
        content (str): 消息内容。
        """
        self.context.append({"role": role, "content": content})
        if len(self.context) > self.max_history:
            self.context.pop(0)  # 超过最大历史记录数，移除最旧的消息

    def get(self) -> List[Dict[str, Any]]:
        """
        获取当前的上下文列表。

        返回:
        List[Dict[str, Any]]: 上下文消息列表。
        """
        return self.context

    def clear(self):
        """
        清空上下文。
        """
        self.context = []

    def get_recent(self, n: int = 10) -> List[Dict[str, Any]]:
        """
        获取最近的 n 条消息。

        参数:
        n (int): 要获取的消息数量。

        返回:
        List[Dict[str, Any]]: 最近的 n 条消息。
        """
        return self.context[-n:] if len(self.context) > n else self.context
