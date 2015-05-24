__author__ = 'Itay'

import re


class JackTokenizer:

    KeywordsCodes = {"class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean",
                     "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"}
    SymbolsCodes = {'{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '<', '>', '=', '~'}

    def __init__(self, file):
        """
        Opens the input file/stream and gets ready
        to tokenize it
        """
        self.file = open(file)
        self.currToken = ""
        self.lines = self.file.read()  # Read code
        self.removeComments()  # Remove comments
        self.tokens = self.tokenize()
        # print(self.tokens)
        self.tokens = self.replaceSymbols()

    def removeComments(self):
        """ Removes comments from the file string """
        currentIndex = 0
        filteredText = ''
        endIndex = 0
        while currentIndex < len(self.lines):
            currentChar = self.lines[currentIndex]
            if currentChar == "\"":
                endIndex = self.lines.find("\"", currentIndex+1)
                filteredText += self.lines[currentIndex:endIndex+1]
                currentIndex = endIndex + 1
            elif currentChar == "/":
                if self.lines[currentIndex + 1] == "/":
                    endIndex = self.lines.find("\n", currentIndex + 1)
                    currentIndex = endIndex + 1
                    filteredText += " "
                elif self.lines[currentIndex + 1] == "*":
                    endIndex = self.lines.find("*/", currentIndex + 1)
                    currentIndex = endIndex + 2
                    filteredText += " "
                else:
                    filteredText += self.lines[currentIndex]
                    currentIndex += 1
            else:
                filteredText += self.lines[currentIndex]
                currentIndex += 1
        self.lines = filteredText
        return

    def tokenize(self):
        return [self.token(word) for word in self.split(self.lines)]

    def token(self, word):
        if   re.match(self.keywordsRegex, word) != None: return ("keyword", word)
        elif re.match(self.symbolsRegex, word) != None:  return ("symbol", word)
        elif re.match(self.integerRegex, word) != None:  return ("integerConstant", word)
        elif re.match(self.stringsRegex, word) != None:  return ("stringConstant", word[1:-1])
        else:                                            return ("identifier", word)


    keywordsRegex = '(?!\w)|'.join(KeywordsCodes) + '(?!\w)'
    symbolsRegex = '[' + re.escape('|'.join(SymbolsCodes)) + ']'
    integerRegex = r'\d+'
    stringsRegex = r'"[^"\n]*"'
    identifiersRegex = r'[\w]+'
    word = re.compile(keywordsRegex + '|' + symbolsRegex + '|' + integerRegex + '|' + stringsRegex + '|' + identifiersRegex)

    def split(self, line):
        return self.word.findall(line)

    def replaceSymbols(self):
        return [self.replace(pair) for pair in self.tokens]

    def replace(self, pair):
        token, value = pair
        if   value == '<': return (token, '&lt;')
        elif value == '>': return (token, '&gt;')
        elif value == '"': return (token, '&quot;')
        elif value == '&': return (token, '&amp;')
        else:              return (token, value)

    def hasMoreTokens(self):
        """
        do we have more tokens in the input?
        """
        return self.tokens != []

    def advance(self):
        """
        gets the next token from the input and
        makes it the current token. This method
        should only be called if hasMoreTokens()
        is true. Initially there is no current token
        """
        self.currToken = self.tokens.pop(0)
        return self.currToken

    def peek(self):
        if self.hasMoreTokens():
            return self.tokens[0]
        else:
            return ("ERROR", 0)

    def getToken(self):
        """
        returns the type of the current token
        """
        return self.currToken[0]

    def getValue(self):
        """
        returns the current value
        """
        return self.currToken[1]
