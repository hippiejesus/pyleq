import sys
import re
import os
import platform
path = os.path.dirname(os.path.abspath(__file__))

code = []
master_code= []
current_state = None
instruction_number = 0
current_instruction = ""
instructions = {}
workspace = []
data_store = {}
literal_buffer = ""

language = {}
with open(path+path_seperator+"subl.lang","r") as lang:
    data = lang.read()
    dataclean = re.sub(r"\n"," ",data)
    dataclean = re.sub(r"\r"," ",dataclean)

    sublang = dataclean.split(" ")
    for rule in sublang:
        splitsies = rule.split("&")
        keyword = splitsies[0]
        command = splitsies[1]
        command = re.sub(r"*"," ",command)
        language.update({str(keyword):str(command)})

compile_time_checklist = []

a = ""
b = ""
c = ""
d = ""

iterable_name = "in1"

operation = ""
buff_space = ""

windows_path_seperator = "\\"
linux_path_seperator = "/"
path_seperator = ""
system = platform.system()
if system == "Windows":
    path_seperator = windows_path_seperator
elif system == "Linux":
    path_seperator = linux_path_seperator


for file in sys.argv[1:]:
    with open(path + path_seperator + str(file),"r") as source:

        data = source.read()
        dataclean = re.sub(r"\n", " ", data)
        # android specific regex
        dataclean = re.sub(r"\r", " ", dataclean)

        code = dataclean.split(" ")
        tempcode = code[:]
        code = []
        for i in tempcode:
            if i != "":
                code.append(i)
        master_code = master_code + code
        code = []

def interpretT(token):
    global current_state,operation,data_store,language
    if token == " " or token == "": return
    if token in language.keys():
        decipher(token)
    if current_state != None:
        glossary[current_state](token)
    else:
        if token == "if":
            current_state = "if"
        elif token == "lit":
            current_state = "literal"
        elif token == "((": current_state = "comment"
        elif token in ["+","-","=","*","/"]:
            current_state = "math"
            operation = token
        elif "->" in token:
            write_instruction("Z Z " + token[2:])
        else:
            if len(token) <=1:
                pass
            elif token[0] == ".":
                value = token.split("=")[1]
                target = token.split("=")[0][1:]
                value = re.sub(r"_"," ", value)
                data_store.update({target:value})
            elif ":" in token:
                write_instruction(token)

def interpret(command,args):
    global current_state
    old_state = current_state
    current_state = None
    for token in command:
        interpretT(token)
    current_state = old_state

def decipher(token):
    global language
    command = language[token]
    references = {}
    command_parts = command.split(" ")
    for part in command_parts:
        if "^" in part:
            ref = part
            if ref not in references.keys():
                references.update({ref:iterate_name()})
                part = references[part]
            else:
                part = references[part]
    interpret(command_parts,None)


def iterate_name():
    global iterable_name
    num = int(iterable_name[2:])
    newnum = num + 1
    iterable_name = "in"+str(newnum)
    return "in"+str(num)

def if_statement(token):
    global a,b,c,d,operation,current_instruction,current_state
    A = ""
    B = ""
    C = ""
    D = ""
    if a == "":
        a = token
    elif operation == "":
        operation = token
    elif b == "":
        b = token
    elif token == ">>":
        pass
    elif c == "":
        c = token
    elif token == "!>":
        d = "!"
    elif d == "!":
        d = token
    else:
        if operation in ["<",">="]:
            A = a
            B = b
            if operation == "<":
                C = d
                D = c
            else:
                C = c
                D = d
        elif operation in [">","<="]:
            A = b
            B = a
            if operation == ">":
                C = d
                D = c
            else:
                C = c
                D = d
        compile_time_checklist.append(C+":")
        if D != "":
            compile_time_checklist.append(D+":")
            D = "Z Z " + D
        current_instruction = " ".join([A,B,C,"\n",D])
        a = ""
        b = ""
        c = ""
        d = ""
        operation = ""
        write_instruction(current_instruction)
        current_state = None

def math(token):
    global a,b,operation,current_instruction,current_state
    if a == "":
        a = token
    elif b == "":
        b = token
    else:
        if operation == "+":
            current_instruction = "Z Z\n" + a + " Z\n"
            current_instruction += "Z " + b + "\nZ Z"
        elif operation == "-":
            current_instruction = a + " " + b
        elif operation == "=":
            current_instruction = b + " " + b + "\n" + "Z Z\n"
            current_instruction += a + " Z\nZ " + b + "\nZ Z"
        a = ""
        b = ""
        operation = ""
        write_instruction(current_instruction)
        current_state = None
        
def comment(token):
    global current_state
    if token == "))": current_state = None

def literal_statement(token):
    global current_state,literal_buffer,current_instruction
    if token == "/l":
        current_state = None
        current_instruction = literal_buffer
        write_instruction(current_instruction)

        current_instruction = ""
        literal_buffer = ""
    else:
        literal_buffer += str(token)+" "

def write_instruction(instruction):
    global instructions,current_instruction,instruction_number
    instructions.update({instruction_number:instruction})
    instruction_number += 1
    current_instruction = ""

def buffer_add(token):
    global buff_space
    buff_space += token

def buffer_clear():
    global buff_space
    buff_space = ""

def get_buffer():
    global buff_space
    return buff_space

def pop_buffer():
    global buff_space
    out = buff_space
    buff_space = ""
    return out

def compilation():
    pass

def check():
    pass

def save():
    pass

glossary = {"if":if_statement,
            "math":math,
            "comment":comment,
            "literal":literal_statement}


if __name__ == "__main__":
    interpret(master_code,None)
    compilation()
    check()
    save()
    for data in data_store:
        write_instruction("."+data+": "+str(data_store[data]))
    for line in instructions:
        print(instructions[line])
    with open("out.sq","w") as out:
        for line in instructions:
            out.write(instructions[line]+"\n")
        out.write(".Z:0\n.m1:-1\n")
