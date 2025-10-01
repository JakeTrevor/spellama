from langchain.schema import BaseMessage,SystemMessage,HumanMessage,AIMessage
from llama_cpp import Llama
from spellama.Agents.Agent import Agent
START_TURN="<|start|>"
END_TURN="<|end|>"
def format_messages_mistral(messages: list[BaseMessage]) -> str:
    formatted = ""

    for msg in messages:
        if isinstance(msg, SystemMessage):
            formatted += f"{START_TURN}system\n{msg.content}{END_TURN}\n"
        elif isinstance(msg, HumanMessage):
            formatted += f"{START_TURN}user\n{msg.content}{END_TURN}\n"
        elif isinstance(msg, AIMessage):
            formatted += f"{START_TURN}model\n{msg.content}{END_TURN}\n"
        else:
            raise ValueError(f"Unknown message type: {type(msg)}")

    formatted += f"{START_TURN}model\n"

    return formatted


class MistralAgent(Agent):

    def __init__(self, llm:Llama, system_prompt:str = ""):
        super().__init__(llm, system_prompt, format_messages_mistral,stop_token=["<|"])