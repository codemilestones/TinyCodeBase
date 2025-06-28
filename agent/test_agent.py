import json

from agent import Agent

def test_agent(question: str):
    agent = Agent()
    response, history = agent.text_completion(question)
    print("-"*100)
    print("final response:\n")
    print(response)
    print("-"*100)

if __name__ == '__main__':
    # test_agent('生成一段 python 冒泡排序代码')
    # test_agent("北京的天气怎么样？")
    test_agent('''
    def hello_world():
        print("Hello, World!")
                                      
    def hello_world2():::::
        print("Hello, World2!")

    请修复这段代码的错误

''')