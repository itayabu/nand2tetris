__author__ = 'Itay'


class JackTokenizer:
    TokenTypes = {"KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"}
    KeywordsCodes = {"class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean",
                     "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"}
    SymbolsCodes = {'{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '<', '>', '=', '~'}
    IdentifierCodes = {}

    def __init__(self, file):
        """
        Opens the input file/stream and gets ready
        to tokenize it
        """
        self.file = open(file)
        self.lineCount = 0
        self.currentLine = ""
        self.lines = self.file.readlines() # split lines
        self.lines = [line.replace('\n', '').replace('\t', '') for line in self.lines] # removes '\n' and '\t'
        self.lines = [line.split("//")[0].strip() for line in self.lines]# if "//" in line]
        #TODO: check if need to consider other types of comments
        self.lines = [line for line in self.lines if line != ''] # removes empty lines


    def hasMoreTokens(self):
        """
        do we have more tokens in the input?
        """
        return self.lineCount < len(self.lines)



    def advance(self):
        """
        gets the next token from the input and
        makes it the current token. This method
        should only be called if hasMoreTokens()
        is true. Initially there is no current token
        """
        self.currentLine = self.lines[self.lineCount]
        self.lineCount += 1
        return self.currentLine

    def tokenType(self):
        """
        returns the type of the current token
        """
        currentToken = self.currentLine.split(" ")[0]
        if self.currentLine in self.KeywordsCodes:
            return "KEYWORD"
        elif self.currentLine in self.SymbolsCodes:
            return "SYMBOL"
        elif self.currentLine.isdigit():
            return "INT_CONST"
        elif self.currentLine.startswith("\""):
            return "STRING_CONST"
        else:
            return "IDENTIFIER"

    def keyWord(self):
        """
        returns the keyword which is the current
        token. Should be called only when
        tokenType() is KEYWORD
        """
        return self.currentLine

    def symbol(self):
        """
        returns the character which is the current
        token. Should be called only when
        tokenType() is SYMBOL
        """
        return self.currentLine

    def indentifier(self):
        """
        returns the identifier which is the current
        token. Should be called only when
        tokenType() is IDENTIFIER
        """
        return self.currentLine

    def intVal(self):
        """
        returns the integer value of the current
        token. Should be called only when
        tokenType() is INT_CONST
        """
        return self.currentLine

    def stringVal(self):
        """
        returns the string value of the current
        token, without the double quotes. Should
        be called only when tokenType() is
        STRING_CONST.
        """
        return self.currentLine