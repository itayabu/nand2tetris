__author__ = 'Gil'


class VMWriter:

    def __init__(self, output):
        """Creates a new file and prepares it for writing VM commands"""
        self.outputFile = open(output, 'w')

    def writePush(self, segment, index):
        """Writes a VM push command"""
        self.outputFile.write('push ' + segment + ' ' + str(index) + '\n')

    def writePop(self, segment, index):
        """Writes a VM pop command"""
        self.outputFile.write('pop ' + segment + ' ' + str(index) + '\n')

    def writeArithmetic(self, command):
        """Writes a VM arithmetic command"""
        self.outputFile.write(command + '\n')

    def writeLabel(self, label):
        """Writes a VM label command"""
        self.outputFile.write('label ' + label + '\n')

    def writeGoto(self, label):
        """Writes a VM goto command"""
        self.outputFile.write('goto ' + label + '\n')

    def writeIf(self, label):
        """Writes a VM if-goto command"""
        self.outputFile.write('if-goto ' + label + '\n')

    def writeCall(self, name, nLocals):
        """Writes a VM call command"""
        self.outputFile.write('call ' + name + ' ' + str(nLocals) + '\n')

    def writeFunction(self, name, nArgs):
        """Writes a VM function command"""
        self.outputFile.write('function ' + name + ' ' + str(nArgs) + '\n')

    def writeReturn(self):
        """Writes a VM return command"""
        self.outputFile.write('return\n')

    def close(self):
        """Closes the output file"""
        self.outputFile.close()
