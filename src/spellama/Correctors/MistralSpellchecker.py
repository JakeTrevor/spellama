from llama_cpp import Llama
from Helpers.formatting_helpers import process_text,get_no_punctuation_text_from_processed_text,return_punctuation_to_text,can_return_punctuation_to_text
from Agents.MistralAgent import MistralAgent
from Correctors.BaseCorrector import BaseCorrector

class MistralSpellchecker(BaseCorrector):
    def __init__(self,llm:Llama):
        self.llm = llm
    def correct(self,text:str):
        processed_text = process_text(text)
        newtext = get_no_punctuation_text_from_processed_text(processed_text)
        
        for _ in range(0,10):
            agent = MistralAgent(self.llm,"You are a british writing assistant. A user will give you text and you will fix any spelling mistakes it may have. Maintain the original wording.")
            r = agent(newtext)
            if not can_return_punctuation_to_text(r,processed_text):
                pass
                # print(newtext)
                # print(r)
                # print(".........................")
            else:
                return return_punctuation_to_text(r,processed_text)
        return text
    #   for n,i in enumerate(processed_text[1]):
    #         if i == 1:
    #               agent = MistralAgent(llm,"You are a writing assistant. A user will give you words and you will state whether this word is spelt the same using american and british english. Answer only yes or no.")
    #               print(agent(processed_text[0][n]))
    #               word = agent("now state only the british variant of the word. If it has none just state the word.")
    #               print(word)
    #             #   judgebot = MistralAgent(llm,"You are a quality control assistant. A user will give you two words, answer yes or no whether they are both the same word with acceptable spelling.")
    #             #   print(judgebot(f"""
    #             #     word1:{processed_text[0][n]}
    #             #     word2:{word}
    #             #     """))
    #               #processed_text[0][n] = word
    #   return "".join(processed_text[0])

    #   britbot = MistralAgent(llm,"")
