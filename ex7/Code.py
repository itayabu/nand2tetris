__author__ = 'Itay'

class Code:
    def __init__(self, file):
        """
        Opens the output file/stream and gets ready to write into it.
        """
        self.file = open(file, 'w')

    def setFileName(self, fileName):
        """
        Informs the code writer that the translation of a new VM file is started.
        """
        self.file = open(fileName)

    def writeArithmetic(self, command):
        """
        Writes the assembly code that is the  translation of the given arithmetic command.
        """

    def writePushPop(self, command, segment, index):
        """
        Writes the assembly code that is the  translation of the given command, where
        command is one of the two enumerated values: C_PUSH or C_POP
        """

    def close(self):
        """
        Closes the output file.
        """
        self.file.close()