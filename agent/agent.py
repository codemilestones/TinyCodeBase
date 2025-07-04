import json5
import json

from tools import Tools
from agent_llm import AgentLLM

TOOL_DESC = """{name_for_model}: Call this tool to interact with the {name_for_human} API. What is the {name_for_human} API useful for? {description_for_model} Parameters: {parameters} Format the arguments as a JSON object."""
REACT_PROMPT = """Answer the following questions as best you can. You have access to the following tools:

{tool_descs}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can be repeated zero or more times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!
"""


class Agent:
    def __init__(self, path: str = '') -> None:
        self.path = path
        self.tool = Tools()
        self.system_prompt = self.build_system_input()
        self.model = AgentLLM()

    def build_system_input(self):
        tool_descs, tool_names = [], []
        for tool in self.tool.toolConfig:
            tool_descs.append(TOOL_DESC.format(**tool))
            tool_names.append(tool['name_for_model'])
        tool_descs = '\n\n'.join(tool_descs)
        tool_names = ','.join(tool_names)
        sys_prompt = REACT_PROMPT.format(tool_descs=tool_descs, tool_names=tool_names)
        print("-"*10 + "system_prompt" + "-"*10)
        print(sys_prompt)
        print("-"*10 + "system_prompt" + "-"*10)
        return sys_prompt
    
    def parse_latest_plugin_call(self, text):
        plugin_name, plugin_args = '', ''
        i = text.rfind('\nAction:')
        j = text.rfind('\nAction Input:')
        k = text.rfind('\nObservation:')
        if 0 <= i < j:  # If the text has `Action` and `Action input`,
            if k < j:  # but does not contain `Observation`,
                text = text.rstrip() + '\nObservation:'  # Add it back.
            k = text.rfind('\nObservation:')
            plugin_name = text[i + len('\nAction:') : j].strip()
            plugin_args = text[j + len('\nAction Input:') : k].strip()
            text = text[:k]
        return plugin_name, plugin_args, text
    
    def call_plugin(self, plugin_name, plugin_args):
        plugin_args = json5.loads(plugin_args)

        print("-"*10 + "call_plugin" + "-"*10)
        print("plugin_name:", plugin_name)
        print("plugin_args:", plugin_args)
        print("-"*10 + "call_plugin" + "-"*10)

        if plugin_name == 'google_search':
            return '\nObservation:' + self.tool.google_search(**plugin_args)
        elif plugin_name == 'code_check':
            return '\nObservation:' + self.tool.code_check(**plugin_args)

    def text_completion(self, text, history=[]):
        text = "\nQuestion:" + text
        response, his = self.model.chat(text, history, self.system_prompt)
        print("first response:\n")
        print(response)
        print("-"*100)
        plugin_name, plugin_args, response = self.parse_latest_plugin_call(response)
        if plugin_name:
            function_call_result = self.call_plugin(plugin_name, plugin_args)
            print("="*10 + "function_call_result" + "="*10)
            print(function_call_result)
            print("="*10 + "function_call_result" + "="*10)
            response += function_call_result
        response, his = self.model.chat(response, his, self.system_prompt)
        return response, his
    

