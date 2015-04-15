__author__ = 'Gil'


import sys
import os
import JackTokenizer


def main():
    userInput = sys.argv[1]

    if os.path.isdir(userInput):
        if not userInput.endswith("/"):
            userInput += "/"
        files = os.listdir(userInput)
        for file in files:
            if file.endswith('.jack'):
                fileName = file.split(".")[0]
                parseFile(userInput + file, userInput + fileName + ".vm")
    #Case input is file, just parse it
    elif os.path.isfile(userInput):
        #userInput = userInput.split(".")[0]
        tok = JackTokenizer.JackTokenizer(userInput)
        #parseFile(userInput + ".jack", userInput + ".vm")
    #Raise an exception
    else:
        raise Exception("The input is not valid, please try again")

def parseFile(input, output):
    return True


if __name__ == "__main__":
    main()