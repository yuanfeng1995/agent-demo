# -*- coding: utf-8 -*-

class CalcTool:
    name = 'calc'

    def run(self, input:str):
        try:
            return str(eval(input))
        except:
            return 'Calc failed'
        

class SearchTool:
    name = 'search'

    def run(self, query):
        return f'Simulated search results:{query}'
