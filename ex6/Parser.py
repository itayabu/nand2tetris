__author__ = 'Gil'

class Parser:

    def __init__(self, file):
        self.file = file
        self.lineCount = 0
        self.lines = self.file.readlines() #split lines
        self.lines = [line.replace('\n', '') for line in self.lines] #removes '\n'
        self.lines = [line for line in self.lines if line != ''] #removes enpty lines
        self.currCommand = self.lines[self.lineCount]

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
            #check how to separate between a and l command
            return "A_COMMAND"
        if ("=" in self.currCommand) or (";" in self.currCommand):
            return "C_COMMAND"

    """
    Returns the symbol or decimal
    Xxx of the current command
    @Xxx or (Xxx)
    """
    def symbol(self):

        return self.currCommand.replace("@", "")

    """
    Returns the dest mnemonic in
    the current C-command
        """
    def dest(self):

        if "=" in self.currCommand:
            endPos = self.currCommand.index("=")
        else:
            endPos = self.currCommand.index(";")

        return self.currCommand[0:endPos].replace(" ", "")


    """
    Returns the comp mnemonic in
    the current C-command
    """
    def comp(self):

        if "=" in self.currCommand:
            startPos = self.currCommand.index("=") + 1
        else:
            startPos = 0
        if ";" in self.currCommand:
            endPos = self.currCommand.index(";")
        else:
            startPos = 0

        return self.currCommand[startPos:endPos].replace(" ", "")


    """
        Returns the jump mnemonic in
        the current C-command
        """
    def jump(self):

        if ";" in self.currCommand:
            startPos = self.currCommand.index(";") + 1
            return self.currCommand[startPos:].replace(" ", "")
        else:
            return ""