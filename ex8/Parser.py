__author__ = 'Itay'

class Parser:

    CommandTypes = {"C_ARITHMETIC", "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION", "C_CALL", "C_RETURN"}

    def __init__(self, file):
        """
        Opens the input file/stream and gets ready
        to parse it
        """
        self.file = open(file)
        self.lineCount = 0
        self.currCommand = ""
        self.lines = self.file.readlines() # split lines
        self.lines = [line.replace('\n', '') for line in self.lines] # removes '\n'
        self.lines = [line for line in self.lines if "//" not in line]
        self.lines = [line for line in self.lines if line != ''] # removes empty lines


    def hasMoreCommands(self):
        """
        Are there more commands in the input?
        """
        return self.lineCount < len(self.lines)



    def advance (self):
        """
        Reads the next command from the input and
        makes it the current command. Should be
        called only if hasMoreCommands() is
        true. Initially there is no current command.
        """
        self.currCommand = self.lines[self.lineCount]
        self.lineCount += 1
        return self.currCommand

    def commandType(self):
        """
        Returns the type of the current command.
        C_ARITHMETIC is returned for all the
        arithmetic VM commands
        """
        if ("add" or "sub" or "neg" or "eq" or "gt" or "lt" or "and" or "or" or "not") in self.currCommand:
            return "C_ARITHMETIC"
        if "push" in self.currCommand:
            return "C_PUSH"
        if "pop" in self.currCommand:
            return "C_POP"
        if "goto" in self.currCommand:
            if "if" in self.currCommand:
                return "C_IF"
            return "C_GOTO"
        if "function" in self.currCommand:
            return "C_FUNCTION"
        if "call" in self.currCommand:
            return "C_CALL"
        if "return" in self.currCommand:
            return "C_RETURN"

    #TODO: labels

    def arg1(self):
        """
        Returns the first argument of the current command
        """
        if self.commandType() is "C_PUSH" or self.commandType() is "C_POP":
            return self.currCommand.split(" ")[1]
        else:
            return self.currCommand

    def arg2(self):
        """
        Returns the second argument of the current command
        """
        return self.currCommand.split(" ")[2]