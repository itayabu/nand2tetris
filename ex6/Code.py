__author__ = 'Gil'


class Code:

    destCodes = {'0': '000', 'M': '001', 'D': '010', 'MD': '011',
                 'A': '100', 'AM': '101', 'AD': '110', 'AMD': '111', None:'000'}

    def dest(self, mnemonic):
        return self.destCodes.get(mnemonic)
    """
    Returns the binary code of the
    dest mnemonic.
    """

    compCodes = {'A>>':'010000000', 'D>>':'010010000', 'A<<':'010100000',
                 'D<<':'010110000', 'M>>':'011000000', 'M<<':'011100000',
                 '0':'110101010', '1':'110111111', '-1':'110111010', 'D':'110001100',
                 'A':'110110000',  '!D':'110001101', '!A':'110110001', '-D':'110001111',
                 '-A':'110110011', 'D+1':'110011111','A+1':'110110111','D-1':'110001110',
                 'A-1':'110110010','D+A':'110000010','D-A':'110010011','A-D':'110000111',
                 'D&A':'110000000','D|A':'110010101',
                 '':'xxxxxxxxx',   '':'xxxxxxxxx',   '':'xxxxxxxxx',   '':'xxxxxxxxx',
                 'M':'111110000',  '':'xxxxxxxxx',   '!M':'111110001', '':'xxxxxxxxx',
                 '-M':'111110011', '':'xxxxxxxxx',   'M+1':'111110111','':'xxxxxxxxx',
                 'M-1':'111110010','D+M':'111000010','D-M':'111010011','M-D':'111000111',
                 'D&M':'111000000', 'D|M':'111010101'}

    def comp(self, mnemonic):
        return self.compCodes.get(mnemonic)
        """
    Returns the binary code of the
    comp mnemonic.
    """

    jumpCodes = {None: '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011',
                 'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'}

    def jump(self, mnemonic):
        return self.jumpCodes.get(mnemonic)
    """
    Returns the binary code of the
    jump mnemonic.
    """

    def binary(self, decNum):
        binNum = bin(int(decNum))[2:]
        length = 16 - len(binNum)
        for i in range(length):
            binNum = "0" + binNum
        return binNum