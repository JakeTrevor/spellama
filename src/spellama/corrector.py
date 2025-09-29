from llama_cpp import Llama

class LLMBasedCorrector():
    def __init__(self):
        self.llm = Llama(
        model_path="Mistral-7B-Instruct-v0.3-Q4_K_M.gguf",
        n_gpu_layers=-1,
        n_ctx=2000,
        n_threads=8,
        verbose=False,
        )

    def correct(self, input:str) -> str:

        prompt = f"""
        <|start|>system
        You are a text correction system. Take any text given by the user and fix the punctuation. Do not change any wording. Return only the corrected text and do not converse with the user.

        <|end|>
        <|start|>user
            {input}
        <|end|>
        <|start|>model
        """

        response = self.llm(prompt, echo=False,   max_tokens=300,stop=["<|"])
        return response["choices"][0]["text"]
