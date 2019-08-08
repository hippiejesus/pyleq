
# Basic Subleq emulator implemented in Python 3.7.2

import sys
import re

def interpret(memory,program_counter,a,b,c):

    while program_counter >= 0 :
        a = int(memory[program_counter])
        b = int(memory[program_counter+1])
        c = int(memory[program_counter+2])
        if a < 0 or b < 0 :
            if a < 0 and b >= 0:
                try:
                    memory[b] = ord(input()[0])
                except:
                    pass
            elif b < 0 and a >= 0:
                sys.stdout.write(str(chr(int(memory[a]))))
            elif b < 0 and a < 0:
                sys.stdout.flush()
            program_counter = c
        else:
            memory[b] = int(memory[b]) - int(memory[a])
            if memory[b] > 0 :
                program_counter += 3
            else:
                program_counter = c

if __name__ == "__main__":

    memory = []
    program_counter = 0
    a = 0 ; b = 0 ; c = 0

    with open('infile.sq', 'r') as file:
        data = file.read()
        dataclean = re.sub(r"\n", " ", data)

        # android specific regex
        dataclean = re.sub(r"\r", " ", data)

        memory = dataclean.split(" ")
        filter(lambda a: a != "", memory)
    interpret(memory,program_counter,a,b,c)

