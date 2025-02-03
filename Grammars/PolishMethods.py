from nltk import CFG, ChartParser

def canGenerateByCFG(grammar_str, sentence):
    grammar = CFG.fromstring(grammar_str)
    parser = ChartParser(grammar)
    sentence = sentence.split()
    try:
        parses = list(parser.parse(sentence))
        return bool(parses)
    except ValueError:
        return False

def readGrammar(file):
    with open(file, "r", encoding="utf-8") as f:
        return f.read()

def readSentences(file):
    with open(file, "r", encoding="utf-8") as f:
        return [sentence.strip() for sentence in f.readlines()]


if __name__ == '__main__':
    grammar = readGrammar("grammar_polish.txt")
    sentences = readSentences("sentences_polish.txt")
    iterator = 0
    for sentence in sentences:
        iterator += 1
        print(f"{iterator}. {canGenerateByCFG(grammar, sentence)}  <->  {sentence}")
