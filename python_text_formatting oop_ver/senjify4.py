import sys
import re

class SENJIFY:

    ''' declare all class attrobutes '''
    # store indent
    indent = 0

    # store max_char per line
    max_char = 80

    # store mode
    MODE = "off"

    # track on a sum of current char
    curr_char = 0

    # store a string in a line
    line_str = ""

    def __init__(self, input_stream):
        self.input_stream = input_stream
        #print(input_stream.read())

    def format(self):

        #result = [self.input_stream.read()

        # store returned string from each mode
        return_result = ""

        # store words in a list result
        result = []

        ''' get pattern using regex '''
        pattern = re.compile(r"^{{ (.+) }}?")

        ''' loop through and get each line of text from input_stream '''
        for line in self.input_stream:
            if line != "\n":
                line = line.strip('\n')

            ''' ---------------------------------- '''
            #example of input
            #x = x.strip()
            #print(x)

            #example how to use class attribute
            #print(self.__class__.MODE)

            #example of private method call
            #self.__test()
            ''' ---------------------------------- '''

            ''' check for command '''
            is_command = self.__get_command(line, pattern, result)

            ''' after setting the command go to next line '''
            if (is_command):
                continue

            ''' modes '''
            if (self.__class__.MODE == "off"):
                ''' add text to the list 'result' line by line '''
                return_result = self.__off_mode(line)
                result.append(return_result)

            elif (self.__class__.MODE == "on"):
                return_result = self.__on_mode(line, result)[:]

        # print the indent and the remaining txt
        if (self.__class__.line_str != "" and self.__class__.MODE == "on"):
            result.append(" " * self.__class__.indent + self.__class__.line_str.strip())

        #print(result)
        return result

    #example of private method
    #def __test(self):
        #self.__class__.MODE = "on"


    def __get_command(self, line, pattern, result):

        ''' search for command using regex '''
        m = pattern.search(line)
        if m:
            command = m.group(1)

            ''' special case if there is a command when there is a remaining text, then print the text and reset '''
            if (self.__class__.line_str != "" and (("+" in command) or ("-" in command)) and command[2:].isdigit()):
                result.append(" " * self.__class__.indent + self.__class__.line_str.strip())
                self.__class__.line_str = ""
                self.__class__.curr_char = 0

            ''' scan for number of char in a line command '''
            if command.isdigit():
                self.__class__.MODE = "on"
                self.__class__.max_char = int(command)
                line = ""
                return True

            ''' scan for number of indent in a line command '''
            if (">" in command) and command[1:].isdigit():
                self.__class__.MODE = "on"
                self.__class__.indent = int(command[1:])
                line = ""
                return True

            ''' scan for 'on' in a line command '''
            if command == "on":
                self.__class__.MODE = "on"
                line = ""
                return True

            ''' scan for 'off' in a line command '''
            if command == "off":
                self.__class__.MODE = "off"
                line= ""
                return True

            ''' scan for number of '!' in a line command '''
            if command == "!":
                if (self.__class__.MODE == "on"):
                    self.__class__.MODE = "off"
                elif (self.__class__.MODE == "off"):
                    self.__class__.MODE = "on"
                text = ""
                return True

            ''' scan for number of + indent in a line command '''
            if "+>" in command and command[2:].isdigit():
                self.__class__.MODE = "on"
                self.__class__.indent += int(command[2:])
                text = ""
                return True

            ''' scan for number of - indent in a line command '''
            if "->" in command and command[2:].isdigit():
                self.__class__.MODE = "on"
                self.__class__.indent -= int(command[2:])
                if (self.__class__.indent < 0):
                    self.__class__.indent = 0
                text = ""
                return True
            return False

    def __off_mode(self, text):
        if (text[len(text) - 1:] == '\n'):
            text = text[:len(text) - 1]
        return text

    def __on_mode(self, text, result):

        # if the line is new line, print all and clear
        if (text == "\n"):
            z = self.__class__.line_str.strip()
            result.append(" " * self.__class__.indent + z)
            if (z != ""):
                result.append('')
            self.__class__.line_str = ""
            self.__class__.curr_char = 0
            return result

        ''' store words after split '''
        line_li = []

        ''' format all white spaces '''
        text = text.strip()

        ''' split by white space using regex '''
        line_li = re.split(' +', text)

        for i in line_li:
            # find cur  rent length
            self.__class__.curr_char = self.__class__.curr_char + len(i)

            # if the line have engouh space to add the current word
            if (self.__class__.curr_char + 1 <= self.__class__.max_char - self.__class__.indent):
                self.__class__.line_str = self.__class__.line_str + " " + i

                # add one char foor a white space between words
                self.__class__.curr_char = self.__class__.curr_char + 1
            else:
                # if the current word just fit the line
                if (self.__class__.curr_char == self.__class__.max_char - self.__class__.indent):
                    self.__class__.line_str = self.__class__.line_str + " " + i
                    continue

                # if the line reaches the maximum then print the line
                result.append(" " * self.__class__.indent + self.__class__.line_str.strip())

                # set current word to be a head for new line
                self.__class__.line_str = i

                # set curr_char to be the length of the head + an white space
                self.__class__.curr_char = len(i) + 1

        return result