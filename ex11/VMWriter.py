__author__ = 'Gil'


class VMWriter:

    def __init__(self, output):
        """Creates a new file and prepares it for writing VM commands"""
        self.outputFile = open(output, 'w')

    def writePush(self, segment, index):
        """Writes a VM push command"""
        return

    def writePop(self, segment, index):
        """Writes a VM pop command"""

    def WriteArithmetic(self, command):
        """Writes a VM arithmetic command"""
        return

    def WriteLabel(self, label):
        """Writes a VM label command"""
        return

    def WriteGoto(self, label):
        """Writes a VM goto command"""
        return

    def WriteIf(self, label):
        """Writes a VM if-goto command"""
        return

    def WriteCall(self, name, nLocals):
        """Writes a VM call command"""
        return

    def WriteFunction(self, name, nArgs):
        """Writes a VM function command"""
        return

    def writeReturn(self):
        """Writes a VM return command"""
        return

    def close(self):
        """Closes the output file"""
        self.outputFile.close()
