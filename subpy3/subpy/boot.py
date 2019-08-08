
import re
import cpu

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
    cpu.interpret(memory,program_counter,a,b,c)
