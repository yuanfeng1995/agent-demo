# -*- coding: utf-8 -*-
class BaseTool:
    """
    BaseTool 是所有工具的基类，定义了工具的基本接口。
    子类需要实现 name 属性和 run 方法。
    """
    name = ""

    def run(self, input_str: str) -> str:
        """
        执行工具的逻辑。

        参数:
        input_str (str): 输入字符串。

        返回:
        str: 执行结果。

        抛出:
        NotImplementedError: 如果子类没有实现此方法。
        """
        raise NotImplementedError