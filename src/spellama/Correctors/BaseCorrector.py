from abc import ABC,abstractmethod
from dataclasses import dataclass
from llama_cpp import Llama
@dataclass
class BaseCorrector(ABC):
    llm: Llama

    def __init__(self):
        pass

    @abstractmethod
    def correct(self,text:str) ->str:
        pass
