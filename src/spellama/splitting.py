from typing import List, Self

class Chunk():
    contents: List[str]
    scrutinee: int

    def __init__(self, contents, scrutinee):
        self.contents = contents
        self.scrutinee = scrutinee

    def getContents(self) -> str:
        " ".join(self.contents)
    
    def getScrutinee(self) -> str:
        return self.contents[self.scrutinee]

    def __str__(self) -> str:
        return " ".join([(s if i != self.scrutinee else f"<<{s}>>") for i,s in enumerate(self.contents)])

    def correct(self) -> Self:
        newContents =[" ".join([w if w != 'and' else 'OR' for w in s.split()])  for s in self.contents]

        return Chunk(newContents, self.scrutinee)
        

def makeChunk(lst:List[str], idx: int, numBlocksBefore, numBlocksAfter) -> Chunk:
    lower = max(0, idx - numBlocksBefore)
    upper = idx + numBlocksAfter + 1
    return Chunk(lst[lower:upper], numBlocksBefore)
    
def makeChunks(sentences: List[str], *, numBlocksBefore=1, numBlocksAfter=1) -> List[Chunk]:
    return [
        makeChunk(sentences, i, numBlocksBefore, numBlocksAfter)
        for i in range(len(sentences))
    ]

