import nltk
from typing import List, Self
from spellama.MistralCorrectV_2 import CorrectionException, MistralCorrector_V2

corrector = MistralCorrector_V2()

class Chunk():
    contents: List[str]
    scrutinee: int
    whitespace: str
    
    # Static methods:
    @staticmethod
    def makeChunk(lst: List[str], idx: int, numBlocksBefore: int, numBlocksAfter: int, whitespace: str) -> Self:
        lower = max(0, idx - numBlocksBefore)
        actualBlocksBefore = idx - lower
        upper = idx + numBlocksAfter + 1
        return Chunk(lst[lower:upper], actualBlocksBefore, whitespace)
    
    @staticmethod
    def getSentences(text: str) -> List[str]:
        return nltk.tokenize.sent_tokenize(text)

    @staticmethod
    def getWhitespaces(text: str, sentences: List[str]):
        whitespaces = []
        end = 0
        for sentence in sentences:
            start = text.find(sentence, end)
            whitespaces.append(text[end:start])
            end = start + len(sentence)

        whitespaces.append(text[end:])
        return whitespaces[1:]

    
    @staticmethod
    def makeChunks(text:str, numBlocksBefore=1, numBlocksAfter=1) -> List[Self]:
        sentences = Chunk.getSentences(text)

        whitespaces = Chunk.getWhitespaces(text, sentences)

        return [
            Chunk.makeChunk(sentences, i, numBlocksBefore, numBlocksAfter, whitespaces[i])
            for i in range(len(sentences))
        ]

    # instance methods:
    def __init__(self, contents: List[str], scrutinee: int, whitespace: str):
        self.contents = contents
        self.scrutinee = scrutinee
        self.whitespace = whitespace

    def getContents(self) -> str:
        return " ".join(self.contents)
    
    def getScrutinee(self) -> str:
        return self.contents[self.scrutinee].strip() + self.whitespace

    def __str__(self) -> str:
        return " ".join([(s if i != self.scrutinee else f"<<{s}>>") for i,s in enumerate(self.contents)])

    def correct(self) -> Self:
        # return self
        try:
            newContents = corrector.correct(self.getContents())
            sentences = self.getSentences(newContents)
            return Chunk(sentences, self.scrutinee, self.whitespace)
        except CorrectionException as _:
            # Add a [!!!!] to the start of the sentence
            self.contents[self.scrutinee] =  "[!!!!]" + self.getScrutinee()
            return self
            
            

