__author__ = 'Gil'

import sys
import os
import CompilationEngine


def main():
    userInput = sys.argv[1]

    if os.path.isdir(userInput):
        if not userInput.endswith("/"):
            userInput += "/"
        files = os.listdir(userInput)
        for file in files:
            if file.endswith('.jack'):
                fileName = file.split(".")[0]
                comp = CompilationEngine.CompilationEngine(userInput + file, userInput + fileName + ".xmla")
                comp.compileClass()
    #Case input is file, just parse it
    elif os.path.isfile(userInput):
        userInput = userInput.split(".")[0]
        comp = CompilationEngine.CompilationEngine(userInput + ".jack", userInput + ".xmla")
        comp.compileClass()
    #Raise an exception
    else:
        raise Exception("The input is not valid, please try again")

if __name__ == "__main__":
    main()
