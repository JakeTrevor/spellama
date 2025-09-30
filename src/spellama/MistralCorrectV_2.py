from llama_cpp import Llama
from Correctors.BaseCorrector import BaseCorrector
from Correctors.MistralSpellchecker import MistralSpellchecker
from Agents.Agent import Agent
from Agents.MistralAgent import MistralAgent
from Helpers.formatting_helpers import is_enclosed_in_quotes,reformat_bad_emdashes,find_conjoined_words,fix_uneccessary_encoding,strip_edge_quotes,strip_punctuation,strip_whitespace_and_punctuation,space_around_em_dashes,strip_words,is_enclosed_in_specific_quotes,enclose_text_in_specific_quotes,compare_without_whitespace_and_punctuation,compare_without_punctuation
import json

class CorrectionException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)



def get_json_response(message:str,agent:Agent,temperature:float = 0.8):
    response = agent(message,temperature=temperature)
    try:
        js = json.loads(response)
        return js
    except Exception as e:
        print("//////////////////////////////////")
        print(e)
        print(response)
        extractor_agent = MistralAgent(llm=agent.llm,system_prompt="You are an agent tasked with quality control. The user will give you inputs that contain json. Return only the json. Do not chat or converse with the user.")
        new_js = extractor_agent(response)
        print(new_js)
        return json.loads(new_js)


def get_response_without_chattyness(message:str,expected_length:int,agent:Agent,temperature:float = 0.8) -> str: #needs work
    response = agent(message,temperature=temperature)
    if abs(len(response) -expected_length)>10:
        response = agent("Give me only the text. Do not format it in any way. Do not try to converse.")
        if abs(len(response) -expected_length)>10:
            extractor_agent = MistralAgent(agent.llm,system_prompt="You are an agent tasked with quality control. A user will give you a structured input that contains a long text. Return only the text without the rest of the format.")
            response = extractor_agent(response)
            #raise(Exception("ai shat self"))
    return response

           

class MistralCorrector_V2(BaseCorrector):
      
    def __init__(self):
        self.llm = Llama(
        model_path="Mistral-Nemo-Instruct-2407.Q4_K_M.gguf",
        n_gpu_layers=-1,
        n_ctx=5000,
        n_threads=8,
        verbose=False
        )
        self.spellcheck = MistralSpellchecker(self.llm)
        
    def _correct_words(self,text:str):
        return self.spellcheck.correct(text)
        



    def _correct_punctuation(self,text:str):
        # correction_agent = MistralAgent(self.llm,"You are a text correction system. Take any text given by the user and fix the punctuation only. Precisely preserve the original wording add or remove only punctuation marks. Return only the corrected text.")
        # response = correction_agent(text)
        
        correction_agent = MistralAgent(self.llm)
        response = correction_agent(f"Correct any punctuation mistakes that might be in the following text. Precisely preserve the original wording add or remove only punctuation marks. Return only text and do not converse with me. \n {text} ")

        #print(response)
        response = reformat_bad_emdashes(response.strip())
        
        # correction_agent = MistralAgent(self.llm,"You are a text analysis system. Take any text given by the user and analyze whether its punctuation could be improved. List any improvements you would make.")
        # ("==========AGENT THOUGHTS==============")
        # (correction_agent(text))
        
        # response = reformat_bad_emdashes(correction_agent("now please fix the text, correcting any punctuation mistakes you pointed out. Precisely preserve the original wording add or remove only punctuation marks."))
        
        # ("==========END THOUGHTS==============")

        words_unchanged = compare_without_whitespace_and_punctuation(response,text)


        count = 0
        while not words_unchanged:
            # print(correction_agent.format_input(correction_agent.history))
            # print("agent_response")
            # print(response)
            # print(text)
            # print("end")
            # print()
            # print()
            # print()
            if count > 5:
                # print(text)
                # print(response)
                raise(CorrectionException("Ai failed to maintain original wording"))
            count = count+1
            response = get_response_without_chattyness("This response is incorrect, you changed the wording. Put the original words back into the text, remove any additional words you may have added and do not change the punctuation anymore. As a reminder here is the original text: \n "+text,expected_length=len(text),agent=correction_agent)
            response = reformat_bad_emdashes(response)
            words_unchanged = compare_without_whitespace_and_punctuation(response,text)
            if words_unchanged:
                break
            if count == 2:
                zero_shot_bot = MistralAgent(self.llm,"You are a text processing bot tasked with combining two texts the user gives you. Text1 has the correct wording, Text2 has the correct punctuation. Combine them both into one text.")
                zero_shot_bot(f"""
                    Text1:{text}
                    Text2:{response}
                """)
                res = get_response_without_chattyness("now please give me only the text",len(text),zero_shot_bot)
                if compare_without_whitespace_and_punctuation(res,text):
                    response = res
                    break
            
            if count == 1:
                new_response = self._correct_words(response)
                if compare_without_whitespace_and_punctuation(new_response,text):
                    response = new_response
                    break

                # britbot = MistralAgent(self.llm)
                
                # zero_shot_attempt_message = f"Return the following text, enforce british spelling on any word that is spelled with an o instead of an ou. Change nothing else. Only return text." \
                #    f" {text} " 

                # newResponse = get_response_without_chattyness(zero_shot_attempt_message,expected_length=len(text),agent=britbot)
                # print(newResponse)
                # if compare_without_whitespace_and_punctuation(response,text):
                #     response = newResponse
                #     break
                # else:
                #     newResponse = get_response_without_chattyness("you changed something else. Fix this.",expected_length=len(text),agent=britbot)
                #     print(newResponse)
                #     if compare_without_whitespace_and_punctuation(response,text):
                #         response = newResponse
                #         break



        if( not compare_without_punctuation(space_around_em_dashes(response),space_around_em_dashes(text))):
            conjoined = find_conjoined_words(text,response)
            for i in conjoined:
                response = response.replace(i[0],i[1])
                            
        quotes = is_enclosed_in_quotes(text)
        if quotes[0]:
            response = enclose_text_in_specific_quotes(response,quotes[1],quotes[2])
        else:
            response = strip_edge_quotes(response)
        response = space_around_em_dashes(fix_uneccessary_encoding(response))
        
        return (response==text,response)
    
    def check(self, text:str):

        correct = self._correct_punctuation(text)
        check = correct[0]
        #if not check:
            # print("------------------")
            # print(text)
            # print(correct)
            # print(check)
            # print("------------------")
        return check

    def correct(self, text: str) -> str:
        #return self._correct(text)[1]
        check = False
        count = 10
        text = self._correct_words(text)
        ls: list[str] = []
        while not check:
            if count == 0:
                print(ls)
                raise(CorrectionException("Ai did not converge"))
            count = count -1
            try:
                res = self._correct_punctuation(text)
            except:
                res = self._correct_punctuation(text)
            check = res[0]
            text = res[1]
            ls.append(res[1])
        return text

#a = MistralCorrector_V2()

#print(a.correct("To them tese conditions felt like the embrace of an old lover something familar almost homely in its misery."))


# p = process_text("Heavy, armoured steps threw up mud in little waves, every step a personal apocalypse for the small creatures that called this field their home.")
# r = get_no_punctuation_text_from_processed_text(p)
# print(p)
# print(r)
# n = "Heavy arrr steps threw up mud in swd waves every step a asdw apocalypse for the small creatures that called this field their home."
# print(can_return_punctuation_to_text(n,p))
# print(return_punctuation_to_text(n,p))