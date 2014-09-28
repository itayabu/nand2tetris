__author__ = 'Gil'

class Parser:

    def __init__(self, file):
        self.file = file
        self.lineCount = 0
        self.currCommand = ""
        self.lines = self.file.readlines() #split lines
        self.lines = [line.replace('\n', '') for line in self.lines] #removes '\n'
        self.lines = [self.relevantLine(line, "", "//").replace(" ", "") for line in self.lines] #removes '//' and spaces
        self.lines = [line for line in self.lines if line != ''] #removes empty lines


    def relevantLine(self, line, startChar, endChar = '\n'):
        if startChar in line:
            startPos = line.index(startChar)
        else:
            startPos = 0
        if endChar in line:
            endPos = line.index(endChar)
            return line[startPos:endPos]

        return line[startPos:]


    """
    Are there more commands in the
    input?
    """
    def hasMoreCommands(self):
        return self.lineCount < len(self.lines)

    """
    Reads the next command from
    the input and makes it the current
    command. Should be called only
    if hasMoreCommands() is true.
        """
    def advance(self):
        self.currCommand = self.lines[self.lineCount]
        self.lineCount += 1
        return self.currCommand

    """
    Returns the type of the current
    command:
    A_COMMAND for @Xxx where
    Xxx is either a symbol or a
    decimal number
    C_COMMAND for
    dest=comp;jump
    L_COMMAND for (Xxx) where Xxx
    is a symbol
    """
    def commandType(self):

        if "@" in self.currCommand:
            return "A_COMMAND"
        if "(" in self.currCommand:
            return "L_COMMAND"
        if ("=" in self.currCommand) or (";" in self.currCommand):
            return "C_COMMAND"

    """
    Returns the symbol or decimal
    Xxx of the current command
    @Xxx or (Xxx)
    """
    def symbol(self):
        if "@" in self.currCommand:
            return self.currCommand.replace("@", "")
        if "(" in self.currCommand:
            return self.relevantLine(self.currCommand, "(", ")")[1:]

    """
    Returns the dest mnemonic in
    the current C-command
        """
    def dest(self):
        if "=" not in self.currCommand:
            return None
        return self.relevantLine(self.currCommand, "",  "=")


    """
    Returns the comp mnemonic in
    the current C-command
    """
    def comp(self):
        if "=" not in self.currCommand:
            return self.relevantLine(self.currCommand, "",  ";")
        return self.relevantLine(self.currCommand, "=", ";")[1:]


    """
        Returns the jump mnemonic in
        the current C-command
        """
    def jump(self):
        if ";" not in self.currCommand:
            return None
        return self.relevantLine(self.currCommand, ";")[1:]

    def resetCommands(self):
        self.lineCount = 0

    def deleteLine(self):
        del self.lines[self.lineCount - 1]
        self.lineCount -= 1