import re
import sys

#store indent
indent = 0

#store max_char per line
max_char = 80

#store mode
MODE = "off"

#store a string in a line
line_str = ""

#store words in a list
line_li = []

#track on a sum of current char
curr_char = 0

def main():
    # read file input
    file = open('input.txt', 'r')
    if file == None:
        print("file error")
        sys.exit(1)

    # loop through each line
    for line in file:
        #check for command
        is_command = get_command(line)


        #after setting the command go to next line
        if (is_command):
            continue

        #modes
        if (MODE == "off"):
            off_mode(line)
        elif (MODE == "on"):
            on_mode(line)

    #print the indent and the remaining txt
    if (line_str != "" and MODE == "on"):
        print(" "*indent + line_str.strip())

    file.close()

#get command
def get_command(text):
    global MODE
    global indent
    global max_char
    global line_str
    global curr_char
    li = text.split()

    if(len(li) == 3):
        #special case if there is a command when there is a remaining text, then print the text and reset
        if (line_str != "" and li[0] == "{{" and li[2] == "}}" and (("+" in li[1]) or ("-" in li[1])) and li[1][2:].isdigit()):
            print((" " * indent + line_str.strip()))
            line_str = ""
            curr_char = 0

        #scan for number of char in a line command
        if (li[0] == "{{" and li[2] == "}}" and li[1].isdigit()):
            MODE = "on"
            max_char = int(li[1])
            text = ""
            return True

        #scan for number of indent in a line command
        elif (li[0] == "{{" and li[2] == "}}" and (">" in li[1]) and li[1][1:].isdigit()):
            MODE = "on"
            indent = int(li[1][1:])
            text = ""
            return True

        #scan for 'on' in a line command
        elif (li[0] == "{{" and li[2] == "}}" and li[1] == "on"):
            MODE = "on"
            text = ""
            return True

        # scan for 'off' in a line command
        elif (li[0] == "{{" and li[2] == "}}" and li[1] == "off"):
            MODE = "off"
            text = ""
            return True

        #scan for number of '!' in a line command
        elif (li[0] == "{{" and li[2] == "}}" and li[1] == "!"):
            if (MODE == "on"):
                MODE = "off"
            elif (MODE == "off"):
                MODE = "on"
            text = ""
            return True

        #scan for number of + indent in a line command
        elif (li[0] == "{{" and li[2] == "}}" and ("+" in li[1]) and li[1][2:].isdigit()):
            MODE = "on"
            indent = indent + int(li[1][2:])
            text = ""
            return True

        # scan for number of - indent in a line command
        elif (li[0] == "{{" and li[2] == "}}" and ("-" in li[1]) and li[1][2:].isdigit()):
            MODE = "on"
            indent = indent - int(li[1][2:])
            if(indent < 0):
                indent = 0
            text = ""
            return True

def on_mode(text):
    global curr_char
    global line_str
    global meet_command

    #if the line is new line, print all and clear
    if (text == "\n"):
        z = line_str.strip()
        print(" " * indent + z)
        if(z !=  ""):
            print('')
        line_str = ""
        curr_char = 0
        return

    #format all whitle spaces
    text = text.strip()

    #remove white space between words
    text = re.sub(' +', ' ', text)

    #split in multi words and store in a list
    line_li = text.split()

    for i in line_li:
        # find current length
        curr_char = curr_char + len(i)

        #debug
        #print(curr_char)
        #print(i)

        #if the line have engouh space to add the current word
        if (curr_char + 1 <= max_char - indent):
            line_str = line_str + " " + i

            #add one char foor a white space between words
            curr_char = curr_char + 1
        else:
            #if the current word just fit the line
            if(curr_char == max_char - indent):
                line_str = line_str + " " + i
                continue

            #if the line reaches the maximum then print the line
            print(" "*indent + line_str.strip())

            #set current word to be a head for new line
            line_str = i

            #set curr_char to be the length of the head + an white space
            curr_char = len(i) + 1

def off_mode(text):
    #remove new line
    if(text[len(text)-1:] == '\n'):
        text = text[:len(text)-1]
    print(text)

#call main()
if __name__ == "__main__":
    main()