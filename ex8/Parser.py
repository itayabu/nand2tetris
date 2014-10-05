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
        self.lines = [line.replace('\n', '').replace('\t', '') for line in self.lines] # removes '\n' and '\t'
        self.lines = [line.split("//")[0].strip() for line in self.lines]# if "//" in line]
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

    arithmeticCodes = {"sub", "add", "neg", "eq", "gt", "lt", "and", "or", "not"}

    def commandType(self):
        """
        Returns the type of the current command.
        C_ARITHMETIC is returned for all the
        arithmetic VM commands
        """
        if self.currCommand in self.arithmeticCodes:
            return "C_ARITHMETIC"
        elif "push" in self.currCommand:
            return "C_PUSH"
        elif "pop" in self.currCommand:
            return "C_POP"
        elif "goto" in self.currCommand:
            if "if" in self.currCommand:
                return "C_IF"
            return "C_GOTO"
        elif "function" in self.currCommand:
            return "C_FUNCTION"
        elif "call" in self.currCommand:
            return "C_CALL"
        elif "return" in self.currCommand:
            return "C_RETURN"
        elif "label" in self.currCommand:
            return "C_LABEL"
        else:
            print("error in commandType")

    def arg1(self):
        """
        Returns the first argument of the current command
        """
        return self.currCommand.split(" ")[1]

    def arg2(self):
        """
        Returns the second argument of the current command
        """
        return self.currCommand.split(" ")[2]