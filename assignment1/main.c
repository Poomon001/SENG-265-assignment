#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

/*max storage for char, word, line*/
#define MAX_WORDS 132
#define MAX_WORD_LEN 132
#define MAX_LINE_LEN 500

/*store width of char*/
int  width = 80;

/*store indent*/
int indent = 0;

/*store mode*/
int MODE = 0;

/*store a string in a line*/
char line_str[MAX_WORD_LEN];

/*store word in a 2d array*/
char words[MAX_WORDS][MAX_WORD_LEN];

/*track on a sum of current char*/
int num_char = 0;

/*define all functions*/
int get_comd(char *line);
int is_num(char *s);
int word_count(char *line);
void on_mode(char *line);
void off_mode(char *line);
char *strip(char* c);

/*Reference to https://stackoverflow.com/questions/352055/best-algorithm-to-strip-leading-and-trailing-spaces-in-c (User: Johannes Schaub - litb)*/
/*strip front and end white space*/
char *strip(char *c){
    char *e = c + strlen(c) - 1;

    /*remove at front*/
    while(*c && isspace(*c)){
        c++;
    }//while

    /*remove at end*/
    while(e > c && isspace(*e)){
        *e-- = '\0';
    }//while
    return c;
}//strip

/*check whether the char array a number or not*/
int is_num(char *s){

    /*return 0 is it is not a number, abd 1 is it is*/
    while (*s) {
        if (isdigit(*s++) == 0){
            return 0;
        }//if
    }//while
    return 1;
}//is_num

/*Reference to https://www.geeksforgeeks.org/count-words-in-a-given-string/*/
/*count number of words in a line*/
int word_count(char *str){

    /*store stage*/
    int state = 0;

    /*word count*/
    unsigned wc = 0;

    /*loop till end of string*/
    while (*str){
        /*If next character is a separator, set the state to 0*/
        if (*str == ' ' || *str == '\n' || *str == '\t')
            state = 0;

            /*If next character is not a word separator and
             state is 0, then set the state to 1 and
             increment word count*/
        else if (state == 0){
            state = 1;
            ++wc;
        }//else

        /*Move to next character*/
        ++str;
    }//while
    return wc;
}//word_count

/*extract the commands*/
int get_comd(char *line){
    //store 3 sections of the command
    char comd1[MAX_WORD_LEN];
    char comd2[MAX_WORD_LEN];
    char comd3[MAX_WORD_LEN];

    /*store number of word in a line*/
    int num_word = word_count(line);

    /*scan for a command*/
    sscanf(line, "%s %s %s", comd1, comd2, comd3);

    if(num_word == 3){
        /* special case if there is a command when there is a remaining text, then print the text and reset */
        if(line_str[0] != '\0' && (strcmp(comd1,"{{") == 0) && (strcmp(comd3,"}}") == 0)  && ((strstr(comd2,"+>") || (strstr(comd2,"->"))))){
            int z = 0;
            while (z < indent) {
                printf(" ");
                z++;
            }//while
            printf("%s\n", strip(line_str));

            /* set current word to be a head for new line */
            memset(line_str, 0, sizeof(line_str));
            num_char = 0;
        }//if

        /*off command*/
        if((strcmp(comd2, "off") == 0) && (strcmp(comd1, "{{") == 0) && (strcmp(comd3, "}}") == 0)){
            MODE = 0;
            line[0] = '\0';
            return 1;

            /*on command*/
        }else if ((strcmp(comd2, "on") == 0) && (strcmp(comd1, "{{") == 0) && (strcmp(comd3, "}}") == 0)){
            MODE = 1;
            line[0] = '\0';
            return 1;

            /*! command*/
        }else if ((strcmp(comd2, "!") == 0) && (strcmp(comd1, "{{") == 0) && (strcmp(comd3, "}}") == 0)){
            if(MODE == 1){
                MODE = 0;
            }else if(MODE == 0){
                MODE = 1;
            }//else
            line[0] = '\0';
            return 1;

            /*width command*/
        }else if ((strcmp(comd1,"{{") == 0 ) && (strcmp(comd3,"}}") ==0) && is_num(comd2)){
            MODE = 1;
            width = atoi(comd2);
            line[0] = '\0';
            return 1;

            /*add indent command*/
        }else if((strcmp(comd1,"{{") == 0) && (strcmp(comd3,"}}") == 0)  && (strstr(comd2,"+>"))){
            MODE = 1;

            /*remove '+>'*/
            char *new_comd2 = comd2 + 2;
            if(is_num(new_comd2)){
                indent = indent + atoi(new_comd2);
            }//if
            line[0] = '\0';
            return 1;

            /*subtract indent command*/
        }else if((strcmp(comd1,"{{") == 0) && (strcmp(comd3,"}}") == 0)  && (strstr(comd2,"->"))){
            MODE = 1;

            /*remove '->'*/
            char *new_comd2 = comd2 + 2;
            if(is_num(new_comd2)){
                indent = indent - atoi(new_comd2);
            }//if

            /*set indent to 0 when it is negative*/
            if(indent < 0){
                indent = 0;
            }//if
            line[0] = '\0';
            return 1;

            /*indent command*/
        }else if((strcmp(comd1,"{{") == 0) && (strcmp(comd3,"}}") == 0)  && (strstr(comd2,">"))) {
            MODE = 1;

            /*remove '>'*/
            char *new_comd2 = comd2 + 1;
            if (is_num(new_comd2)) {
                indent = atoi(new_comd2);
            }//if
            line[0] = '\0';
            return 1;
        }//else
    }//if
    return 0;
}//get_comd

/*no format*/
void off_mode(char *line){
    printf("%s", line);
}//off_mode

void on_mode(char *line){
    char *t;
    int  num_words = 0;
    int i;

    /*if line is empty, print all, clear and return*/
    if(line[1] == '\n') {
        int z = 0;
        while (z < indent) {
            printf(" ");
            z++;
        }//while
        printf("%s\n", strip(line_str));
        if (line_str[0] != '\0') {
            printf("\n");
        }
        /* set current word to be a head for new line */
        memset(line_str, 0, sizeof(line_str));
        num_char = 0;
        return;
    }//if

    /*no length*/
    if (strlen(line) == 0) {
        return;
    }//if

    /*replace newline to NULL*/
    if (line[strlen(line) - 1] == '\n') {
        line[strlen(line) - 1] = '\0';
    }

    /*split words in a line*/
    t = strtok(line, " ");
    while (t != NULL) {
        if (num_words >= MAX_WORDS) {
            fprintf(stderr, "Too many words!\n");
            exit(1);
        }
        strncpy(words[num_words], t, MAX_WORD_LEN);
        num_words++;

        t = strtok(NULL, " ");
    }//while
    for(i = 0; i < num_words; i++) {
        /*replace /r to NULL*/
        if (words[i][strlen(words[i]) - 1] == '\r') {
            words[i][strlen(words[i]) - 1] = '\0';
        }
        /* find current length */
        num_char = num_char + strlen(words[i]);

        /* if the line have engouh space to add the current word */
        if (num_char + 1 <= width - indent){

            /* add a curr word to the line */
            for(int x = 0; x < strlen(words[i]); x++){
                line_str[strlen(line_str)] = words[i][x];
            }//for
            /* add a white space */
            line_str[strlen(line_str)] = ' ';

            /* add one char foor a white space between words */
            num_char = num_char + 1;
        }else{
            /* if the current word just fit the line */
            if(num_char == width - indent) {
                /*add a curr word to the line*/
                for(int x = 0; x < strlen(words[i]); x++){
                    line_str[strlen(line_str)] = words[i][x];
                }//for
                continue;
            }//if

            /* if the line reaches the maximum then print the line */
            int z = 0;
            while (z < indent ) {
                printf(" ");
                z++;
            }//while
            printf("%s", strip(line_str));

            /* set current word to be a head for new line */
            memset(line_str, 0, sizeof(line_str));
            num_char = 0;
            printf("\n");
            for(int x = 0; x < strlen(words[i]); x++){
                line_str[strlen(line_str)] = words[i][x];
            }//for

            /* add one char for a white space between words */
            line_str[strlen(line_str)] = ' ';
            num_char = strlen(line_str);
        }//else
    }//for
}//on_mode

int main() {
    /*store file*/
    FILE *file;

    /*store text in a line*/
    char input_line[MAX_LINE_LEN];

    /*check for command*/
    int is_command = 0;

    /*read file input*/
    file = fopen("text.txt" , "r");

    /*file exit*/
    if(file == NULL) {
        perror("Error opening file");
        return(-1);
    }//if

    /*reads the file line-by-line from stdin. */
    while (fgets(input_line, MAX_LINE_LEN, file) != 0) {
        /*check for command*/
        is_command = get_comd(input_line);

        /*after get a command, start a new line*/
        if (is_command) {
            continue;
        }//if

        /*mode*/
        if(MODE == 0){
            off_mode(input_line);
        }else if(MODE == 1){
            on_mode(input_line);
        }//if
    }//while

    /* if the line reaches the maximum then print the line */
    int z = 0;
    while (z < indent ) {
        printf(" ");
        z++;
    }//while
    printf("%s", strip(line_str));
    fclose(file);
}//main