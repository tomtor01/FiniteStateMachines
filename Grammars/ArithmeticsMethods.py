import re
from nltk import CFG, ChartParser

def preprocess(sentence):
    tokens = re.findall(r'\d+|[+*()\-]', sentence)
    processed_tokens = ['NUM' if re.fullmatch(r'\d+', token) else token for token in tokens]
    return " ".join(processed_tokens)

def canGenerateByCFG(grammar_str, sentence):
    grammar = CFG.fromstring(grammar_str)
    parser = ChartParser(grammar)
    # tokenizacja i zamiana liczb na 'NUM'
    processed = preprocess(sentence)
    tokens = processed.split()
    try:
        parses = list(parser.parse(tokens))
        return bool(parses)
    except ValueError:
        return False

def readGrammar(file):
    with open(file, "r", encoding="utf-8") as f:
        return f.read()

def readSentences(file):
    with open(file, "r", encoding="utf-8") as f:
        return [sentence.strip() for sentence in f.readlines()]

def readSentence(file):
    with open(file, "r", encoding="utf-8") as f:
        return f.read()


if __name__ == '__main__':

    grammar = readGrammar("grammar_arithmetics.txt")
    sentences = readSentences("sentences_arithmetics.txt")

    iterator = 0
    for sentence in sentences:
        iterator += 1
        result = canGenerateByCFG(grammar, sentence)
        print(f"{iterator}. {result}  <->  {sentence}")
