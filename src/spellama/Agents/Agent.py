from langchain.schema import BaseMessage,SystemMessage,HumanMessage,AIMessage
from llama_cpp import Llama
from typing import Callable
class Agent:

    def __init__(self,llm: Llama, system_prompt: str, format_input: Callable[[list[BaseMessage]],str], stop_token: list[str]):
        self.llm:Llama = llm
        self.stop_token = stop_token
        if system_prompt == "":
            self.history:list[BaseMessage] = []
        else:
            self.history:list[BaseMessage] = [SystemMessage(content=system_prompt)]
        self.format_input = format_input

    def __call__(self, input:str,temperature:float=0.8) -> str:
        self.history.append(HumanMessage(content=input))
        response = self.llm(self.format_input(self.history),temperature=temperature,stop=self.stop_token,max_tokens=500)['choices'][0]['text'].strip() #type:ignore
        self.history.append(AIMessage(content=response))
        if(isinstance(response,str)):
            return response
        else:
            
            raise(Exception("This should literally never happen, if it did - panic"))

        