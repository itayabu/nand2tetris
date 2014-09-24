__author__ = 'Itay'


class Parser:
    def __init__(self, file):
        self.file = file
        self.currCommand = ''
        self.lineCount = 0
        self.lines = self.file.readlines()
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


    def commandType():
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


    def symbol():
        """
Returns the symbol or decimal
Xxx of the current command
@Xxx or (Xxx)
        """


    def dest():
        """
Returns the dest mnemonic in
the current C-command

        """

    def comp():
        """
Returns the comp mnemonic in
the current C-command
        """

    def jump():
        """
Returns the jump mnemonic in
the current C-command
        """
