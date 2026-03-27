# -*- coding: utf-8 -*-
"""
主程序文件，用于运行Agent实例，处理用户输入并输出结果。
"""
from agent import Agent

agent = Agent()

while True:
    user_input = input(">>> ")
    result = agent.run(user_input)
    print(result)