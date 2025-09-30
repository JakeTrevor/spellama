import string
import re





def process_text(text:str):
    newText:list[str] = []
    newTextTypes:list[int] = []
    inWord = False
    for char in text:
        if char in string.ascii_letters:
            if not inWord:
                inWord = True
                newText.append(str(char))
                newTextTypes.append(1)
            else:
                newText[-1] = newText[-1] + str(char)
        elif char == "-":
            if not inWord:
                newText.append(char)
                newTextTypes.append(0)
            else:
                newText[-1] = newText[-1] + str(char)
        elif char in string.whitespace:
            inWord = False
            newTextTypes.append(2)
            newText.append(char)
        elif inWord and (char == "'" or char == "`"):
            newText[-1] = newText[-1] + str(char)
        elif char == ".":
            inWord = False
            newTextTypes.append(3)
            newText.append(char)
        else:
            inWord = False
            newTextTypes.append(0)
            newText.append(char)
    return (newText,newTextTypes)



def strip_whitespace_and_punctuation(sentence:str):
    processed_text = process_text(sentence)

    return ''.join(
        [x for x,y in zip(processed_text[0],processed_text[1]) if y == 1]
    ) 

    # return ''.join(
    #     char for char in sentence
    #     if char not in string.whitespace and char not in string.punctuation and not char ==  "—"
    # )

def strip_punctuation(sentence:str):
    processed_text = process_text(sentence)

    return ''.join(
        [x for x,y in zip(processed_text[0],processed_text[1]) if y == 1 or y==2]
    ) 
    return ''.join(
        char for char in sentence
        if char not in string.punctuation and not char ==  "—"
    )

def compare_without_whitespace_and_punctuation(text1:str,text2:str):
    return strip_whitespace_and_punctuation(text1.lower()) == strip_whitespace_and_punctuation(text2.lower())
def compare_without_punctuation(text1:str,text2:str):
    return strip_punctuation(text1.lower()) == strip_punctuation(text2.lower())

def strip_words(text:str):
    return ''.join(
        char for char in text 
        if char in string.punctuation or char =="—"
    )

def space_around_em_dashes(text:str):
    # Replace any em dash with optional surrounding spaces with a properly spaced em dash
    text =  re.sub(r'\s*—\s*', ' — ', text).strip()
    return text.replace(" - "," — ")


def strip_edge_quotes(text:str):
    if text.startswith('"'):
        text = text[1:]
    if text.endswith('"'):
        text = text[:-1]
    return text

def find_conjoined_words(text1:str,text2:str):
    words1 = strip_punctuation(text1.lower().replace("-","")).split(" ")
    words2 = strip_punctuation(text2.lower().replace("-","")).split(" ")
    words:list[tuple[str,str]] = []
    for i in range(0,len(words2)-1):
        new_word = words2[i]+words2[i+1]
        if new_word in words1:
            words.append((words2[i]+" "+words2[i+1],new_word))
    return words

def add_quotes(text:str) ->str:
    return f'"{text}"'


def is_enclosed_in_quotes(text:str):
    # Strip whitespace
    text = text.strip()
    
    # Define sets of valid quote pairs
    quote_pairs = [
        ('"', '"'),     # double straight quotes
        ("'", "'"),     # single straight quotes
        ('“', '”'),     # double curly quotes
        ('‘', '’')      # single curly quotes
    ]
    
    # Check if the text starts and ends with any of the quote pairs
    ret = (False,"","")
    for open_quote, close_quote in quote_pairs:
        
        if text.startswith(open_quote):
            ret =  (True,open_quote,ret[2])
        if text.endswith(close_quote):
            ret = (True,ret[1],close_quote)
    return ret

def is_enclosed_in_specific_quotes(text:str,open_quote:str,close_quote:str):
    return text.startswith(open_quote) and text.endswith(close_quote)

def enclose_text_in_specific_quotes(text:str,open_quote:str,close_quote:str):
    if not text.startswith(open_quote):
        text = open_quote+text
    if not text.endswith(close_quote):
        text = text+close_quote
    return text

def fix_uneccessary_encoding(text:str)->str:
    return text.replace("\\","")

def reformat_bad_emdashes(text:str)->str:

    return text.replace("-- ","—").replace(" - "," — ")



def get_no_punctuation_text_from_processed_text(text:tuple[list[str],list[int]]):
    return "".join([i for n,i in enumerate(text[0]) if text[1][n] != 0])

def can_return_punctuation_to_text(text:str,processed:tuple[list[str],list[int]]):
    return len( strip_punctuation(text).split(" ")) == len([i for n,i in enumerate(processed[0]) if processed[1][n] ==1]) and text.count(".") == processed[1].count(3)

def return_punctuation_to_text(text:str,processed:tuple[list[str],list[int]]):
    textlist = strip_punctuation(text).split(" ")
    for n,i in enumerate(processed[1]):
        if i == 1:
            next = textlist.pop(0)
            processed[0][n] = next
    return "".join(processed[0])