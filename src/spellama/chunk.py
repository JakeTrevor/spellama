import nltk
from typing import List, Self
from spellama.corrector import LLMBasedCorrector

corrector = LLMBasedCorrector()

class Chunk():
    contents: List[str]
    scrutinee: int
    
    # Static methods:
    @staticmethod
    def makeChunk(lst: List[str], idx: int, numBlocksBefore, numBlocksAfter) -> Self:

        lower = max(0, idx - numBlocksBefore)
        actualBlocksBefore = idx - lower
        upper = idx + numBlocksAfter + 1
        return Chunk(lst[lower:upper], actualBlocksBefore)
    
    @staticmethod
    def getSentences(text: str) -> List[str]:
        return nltk.tokenize.sent_tokenize(text)
    
    @staticmethod
    def makeChunks(text:str, numBlocksBefore=1, numBlocksAfter=1) -> List[Self]:
        sentences = Chunk.getSentences(text)

        return [
            Chunk.makeChunk(sentences, i, numBlocksBefore, numBlocksAfter)
            for i in range(len(sentences))
        ]

    # instance methods:
    def __init__(self, contents: List[str], scrutinee: int):
        self.contents = contents
        self.scrutinee = scrutinee

    def getContents(self) -> str:
        return " ".join(self.contents)
    
    def getScrutinee(self) -> str:
        return self.contents[self.scrutinee]

    def __str__(self) -> str:
        return " ".join([(s if i != self.scrutinee else f"<<{s}>>") for i,s in enumerate(self.contents)])

    def correct(self) -> Self:
        newContents = corrector.correct(self.getContents())
        sentences = self.getSentences(newContents)

        return Chunk(sentences, self.scrutinee)
        
