# -*- coding: utf-8 -*-
from agent import Agent

agent = Agent()

while True:
    user_input = input(">>> ")
    result = agent.run(user_input)
    print(result)