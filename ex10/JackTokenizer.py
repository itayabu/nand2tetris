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
        self.lines = self.file.read() # Read code
        self.removeComments() # Remove comments
        self.tokens = self.tokenize()

    def removeComments(self):
        """ Removes comments from the file string """
        # Order is (technically) significant: /* Comment about comment: // comment! */
        self.lines = re.sub('\/\*(\*)+([^*\/][^*]*\*+)*\/', '', self.lines) # Remove /** */ comments
        self.lines = re.sub('(\/\*)[^*\/]*(\*\/)', '', self.lines) # Remove /* */ comments
        self.lines = re.sub(r'//.*', '', self.lines)  # Remove single line comments
        self.lines = str.strip(self.lines) # Strip
        return

    def tokenize(self):
        return [self.token(word) for word in self.split(self.lines)]

    def token(self, word):
        if   re.match(self.keywords_re, word) != None: return ("KEYWORD", word)
        elif re.match(self.symbols_re, word) != None:  return ("SYMBOL", word)
        elif re.match(self.numbers_re, word) != None:  return ("INT_CONST", word)
        elif re.match(self.strings_re, word) != None:  return ("STRING_CONST", word[1:-2])
        else:                                          return ("IDENTIFIER", word)

    keywords_re = '|'.join(KeywordsCodes)
    symbols_re = '[' + re.escape('|'.join(SymbolsCodes)) + ']'
    numbers_re = r'\d+'
    strings_re = r'"[^"\n]*"'
    ids_re = r'[\w\-]+'
    word = re.compile(keywords_re + '|' + symbols_re + '|' + numbers_re + '|' + strings_re + '|' + ids_re)

    def split(self, line):
        return self.word.findall(line)

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
        self.currToken = self.tokens.pop[0]
        return self.currToken

    def tokenType(self):
        """
        returns the type of the current token
        """
        return self.currToken[0]

    def keyWord(self):
        """
        returns the keyword which is the current
        token. Should be called only when
        tokenType() is KEYWORD
        """
        return self.currToken[1]

    def symbol(self):
        """
        returns the character which is the current
        token. Should be called only when
        tokenType() is SYMBOL
        """
        return self.currToken[1]

    def indentifier(self):
        """
        returns the identifier which is the current
        token. Should be called only when
        tokenType() is IDENTIFIER
        """
        return self.currToken[1]

    def intVal(self):
        """
        returns the integer value of the current
        token. Should be called only when
        tokenType() is INT_CONST
        """
        return self.currToken[1]

    def stringVal(self):
        """
        returns the string value of the current
        token, without the double quotes. Should
        be called only when tokenType() is
        STRING_CONST.
        """
        return self.currToken[1]