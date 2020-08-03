import sys
import re

class SENJIFY:

    ''' declare a class attrobutes '''
    dict = {'MODE':'off', 'indent':0, 'max_char':80, 'curr_char':0, 'line_str':""}

    def __init__(self, input_stream):
        self.input_stream = input_stream

    def format(self):

        ''' store returned string from a mode '''
        return_result = ""

        ''' store words in a list result to return '''
        result = []

        ''' get pattern using regex '''
        pattern = re.compile(r"^{{ (.+) }}?")

        ''' loop through and get each line of a text from input_stream '''
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

            ''' if it is a command, skip it and go to next line '''
            if (is_command):
                continue

            #modes
            if (self.__class__.dict['MODE'] == "off"):
                ''' add text to the list line by line '''
                return_result = self.__off_mode(line)
                result.append(return_result)
            elif (self.__class__.dict['MODE'] == "on"):
                self.__on_mode(line, result)[:]

        ''' add the indent and the remaining txt to the list '''
        if (self.__class__.dict['line_str'] != "" and self.__class__.dict['MODE'] == "on"):
            result.append(" " * self.__class__.dict['indent'] + self.__class__.dict['line_str'].strip())

        #print(result)
        return result

    #example of private method
    #def __test(self):
        #self.__class__.MODE = "on"

    ''' check and extract command from a line '''
    def __get_command(self, line, pattern, result):

        ''' search for command using regex '''
        m = pattern.search(line)

        ''' if command is found, extract the command value '''
        if m:
            command = m.group(1)

            ''' special case: if there is a command when there is a remaining text, then add the text to the list and reset '''
            if (self.__class__.dict['line_str'] != "" and (("+" in command) or ("-" in command)) and command[2:].isdigit()):
                result.append(" " * self.__class__.dict['indent'] + self.__class__.dict['line_str'].strip())
                self.__class__.dict['line_str'] = ""
                self.__class__.dict['curr_char'] = 0

            ''' scan for number of char in a line command '''
            if command.isdigit():
                self.__class__.dict['MODE'] = "on"
                self.__class__.dict['max_char'] = int(command)
                line = ""
                return True

            ''' scan for number of indent in a line command '''
            if (">" in command) and command[1:].isdigit():
                self.__class__.dict['MODE'] = "on"
                self.__class__.dict['indent'] = int(command[1:])
                line = ""
                return True

            ''' scan for 'on' in a line command '''
            if command == "on":
                self.__class__.dict['MODE'] = "on"
                line = ""
                return True

            ''' scan for 'off' in a line command '''
            if command == "off":
                self.__class__.dict['MODE'] = "off"
                line= ""
                return True

            ''' scan for number of '!' in a line command '''
            if command == "!":
                if (self.__class__.dict['MODE'] == "on"):
                    self.__class__.dict['MODE'] = "off"
                elif (self.__class__.dict['MODE'] == "off"):
                    self.__class__.dict['MODE'] = "on"
                text = ""
                return True

            ''' scan for number of + indent in a line command '''
            if "+>" in command and command[2:].isdigit():
                self.__class__.dict['MODE'] = "on"
                self.__class__.dict['indent'] += int(command[2:])
                text = ""
                return True

            ''' scan for number of - indent in a line command '''
            if "->" in command and command[2:].isdigit():
                self.__class__.dict['MODE'] = "on"
                self.__class__.dict['indent'] -= int(command[2:])
                if (self.__class__.dict['indent'] < 0):
                    self.__class__.dict['indent'] = 0
                text = ""
                return True
            return False

    ''' add text to the list without formatting '''
    def __off_mode(self, text):

        ''' if there is newline at the end of line, remove it '''
        if (text[len(text) - 1:] == '\n'):
            text = text[:len(text) - 1]
        return text

    ''' add text tot the list with formatting '''
    def __on_mode(self, text, result):

        ''' store words after split '''
        line_li = []

        ''' special case: if the line is new line, store all line to the list and reset '''
        if (text == "\n"):
            z = self.__class__.dict['line_str'].strip()
            result.append(" " * self.__class__.dict['indent'] + z)

            ''' add an empty space (line) to the list '''
            if (z != ""):
                result.append('')

            self.__class__.dict['line_str'] = ""
            self.__class__.dict['curr_char'] = 0
            return result

        ''' remove all white spaces '''
        text = text.strip()

        ''' split by white space using regex '''
        line_li = re.split(' +', text)

        ''' loop though each word in a line '''
        for i in line_li:

            ''' find current length '''
            self.__class__.dict['curr_char'] = self.__class__.dict['curr_char'] + len(i)

            ''' if the line have enough space to add the current word to line_str '''
            if (self.__class__.dict['curr_char'] + 1 <= self.__class__.dict['max_char'] - self.__class__.dict['indent']):
                self.__class__.dict['line_str'] = self.__class__.dict['line_str'] + " " + i

                ''' add one char for a white space between words '''
                self.__class__.dict['curr_char'] = self.__class__.dict['curr_char'] + 1
            else:

                ''' if the current word just fit the line, add it to line_str '''
                if (self.__class__.dict['curr_char'] == self.__class__.dict['max_char'] - self.__class__.dict['indent']):
                    self.__class__.dict['line_str'] = self.__class__.dict['line_str'] + " " + i
                    continue

                ''' if the line reaches the maximum then add the line_str to the list '''
                result.append(" " * self.__class__.dict['indent'] + self.__class__.dict['line_str'].strip())

                ''' set current word to be a head for new line '''
                self.__class__.dict['line_str'] = i

                ''' set curr_char to be the length of the head + an white space '''
                self.__class__.dict['curr_char'] = len(i) + 1

        return result