#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TP TL1: implémentation des automates
"""

import sys

###############
# Cadre général

V = set(('.', 'e', 'E', '+', '-')
        + tuple(str(i) for i in range(10)))

class Error(Exception):
    pass

INPUT_STREAM = sys.stdin
END = '\n' # WARNING: test_tp modifies the value of END.

# Initialisation: on vérifie que END n'est pas dans V
def init_char():
    if END in V:
        raise Error('character ' + repr(END) + ' in V')

# Accès au caractère suivant dans l'entrée
def next_char():
    global INPUT_STREAM
    ch = INPUT_STREAM.read(1)
    # print("@", repr(ch))  # decommenting this line may help debugging
    if ch in V or ch == END:
        return ch
    raise Error('character ' + repr(ch) + ' unsupported')


############
# Question 1 : fonctions nonzerodigit et digit

def nonzerodigit(char):
    assert (len(char) <= 1)
    return '1' <= char <= '9'

def digit(char):
    assert (len(char) <= 1)
    return '0' <= char <= '9'


# Ces deux fonctions vérifient que le caractère en entré soit respectivement un entier entre 1 et 9 inclus ou un entier entre 0 et 9 inclus.

# next_char vérifie que le caractère est soit un mot du vocabulaire soit le caractère END.


############
# Question 2 : integer et pointfloat sans valeur

def integer_Q2():
    init_char()
    return integer_Q2_state_0()


def integer_Q2_state_0():
    ch = next_char()
    if ch == END:
        return False
    if nonzerodigit(ch):
        return integer_Q2_state_2()
    if ch == "0":
        return integer_Q2_state_1()
    return False


def integer_Q2_state_1():
    ch = next_char()
    if ch == END:
        return True
    if ch == "0":
        return integer_Q2_state_1()
    return False
    


def integer_Q2_state_2():
    ch = next_char()
    if ch == END:
        return True
    if digit(ch):
        return integer_Q2_state_2()
    return False


def pointfloat_Q2():
    init_char()
    return pointfloat_Q2_state_0()


def pointfloat_Q2_state_0():
    ch = next_char()
    if ch == END:
        return False
    if ch == ".":
        return pointfloat_Q2_state_1()
    if digit(ch):
        return pointfloat_Q2_state_2()
    return False


def pointfloat_Q2_state_1():
    ch = next_char()
    if ch == END:
        return False
    if digit(ch):
        return pointfloat_Q2_state_3()
    return False


def pointfloat_Q2_state_2():
    ch = next_char()
    if ch == END:
        return False
    if digit(ch):
        return pointfloat_Q2_state_2()
    if ch == ".":
        return pointfloat_Q2_state_3()
    return False


def pointfloat_Q2_state_3():
    ch = next_char()
    if ch == END:
        return True
    if digit(ch):
        return pointfloat_Q2_state_3()
    return False


############
# Question 5 : integer avec calcul de la valeur
# si mot accepté, renvoyer (True, valeur)
# si mot refusé, renvoyer (False, None)

def integer():
    # Variable globale pour se transmettre les valeurs entre états
    global int_value
    int_value = 0
    init_char()
    return integer_state_0()


def integer_state_0():
    global int_value
    ch = next_char()
    if ch == END:
        return (False, None)
    if nonzerodigit(ch):
        int_value = int(ch)
        return integer_state_2()
    if ch == "0":
        int_value = 0
        return integer_state_1()
    return (False, None)


def integer_state_1():
    global int_value
    ch = next_char()
    if ch == END:
        return (True, int_value)
    if ch == '0':
        return integer_state_1()
    else:
        return (False, None)


def integer_state_2():
    global int_value
    ch = next_char()
    if ch == END:
        return (True, int_value)
    if digit(ch):
        int_value = 10 * int_value + int(ch)
        return integer_state_2()
    return (False, None)


############
# Question 7 : pointfloat avec calcul de la valeur

def pointfloat():
    global int_value
    global exp_value
    init_char()
    int_value = 0.
    exp_value = 0
    return pointfloat_state_0()


def pointfloat_state_0():
    global int_value
    global exp_value
    ch = next_char()
    if ch == END:
        return (False, None)
    if ch == ".":
        return pointfloat_state_1()
    if digit(ch):
        int_value = int(ch)
        return pointfloat_state_2()
    return (False, None)


def pointfloat_state_1():
    global int_value
    global exp_value
    ch = next_char()
    if ch == END:
        return (False, None)
    if digit(ch):
        exp_value += 1
        int_value = int(ch)
        return pointfloat_state_3()
    return (False, None)


def pointfloat_state_2():
    global int_value
    global exp_value
    ch = next_char()
    if ch == END:
        return (False, None)
    if digit(ch):
        int_value = int_value * 10 + int(ch)
        return pointfloat_state_2()
    if ch == ".":
        return pointfloat_state_3()
    return (False, None)


def pointfloat_state_3():
    global int_value
    global exp_value
    ch = next_char()
    if ch == END:
        return (True, int_value * (10 ** (- exp_value)))
    if digit(ch):
        exp_value += 1
        int_value = int_value * 10 + int(ch)
        return pointfloat_state_3()
    return (False, None)



############
# Question 8 : exponent, exponentfloat et number

# La valeur du signe de l'exposant : 1 si +, -1 si -


def exponent():
    global exp_value
    global sign_value
    sign_value = 0
    exp_value = 0
    init_char()
    return exponent_state_0()


def exponent_state_0():
    global exp_value
    global sign_value
    ch = next_char()
    if ch == END:
        return (False, None)
    if ch == "E" or ch == "e":
        return exponent_state_1()
    return (False, None)


def exponent_state_1():
    global exp_value
    global sign_value
    ch = next_char()
    if ch == END:
        return (False, None)
    if ch == "+" or ch == "-":
        if ch == "+":
            sign_value = 1
        else:
            sign_value = -1
        return exponent_state_2()
    if digit(ch):
        sign_value = 1
        exp_value = int(ch)
        return exponent_state_3()
    return (False, None)

def exponent_state_2():
    global exp_value
    global sign_value
    ch = next_char()
    if ch == END:
        return (False, None)
    if digit(ch):
        exp_value = int(ch)
        return exponent_state_3()
    return (False, None)


def exponent_state_3():
    global exp_value
    global sign_value
    ch = next_char()
    if ch == END:
        return (True, sign_value * exp_value)
    if digit(ch):
        exp_value = exp_value * 10 + int(ch)
        return exponent_state_3()
    return (False, None)



def exponentfloat():
    global int_value
    global floatexp_value
    global exp_value
    global sign_value
    int_value = 0
    floatexp_value = 0
    exp_value = 0
    sign_value = 0
    init_char()
    return exponentfloat_state_0()

# Partie "pointfloat ou digit⁺"
#################################
def exponentfloat_state_0():
    global int_value
    global floatexp_value
    ch = next_char()
    if ch == END or ch == "E" or ch == "e":
        return (False, None)
    if ch == ".":
        return exponentfloat_state_1()
    if digit(ch):
        int_value = int(ch)
        return exponentfloat_state_2()
    return (False, None)


def exponentfloat_state_1():
    global int_value
    global floatexp_value
    ch = next_char()
    if ch == END or ch == "E" or ch == "e":
        return (False, None)
    if digit(ch):
        floatexp_value += 1
        int_value = int(ch)
        return exponentfloat_state_3()
    return (False, None)


def exponentfloat_state_2():
    global int_value
    global floatexp_value
    ch = next_char()
    if ch == END:
        return (False, None)
    if ch == "E" or ch == "e":
        return exponentfloat_state_4()
    if digit(ch):
        int_value = int_value * 10 + int(ch)
        return exponentfloat_state_2()
    if ch == ".":
        return exponentfloat_state_3()
    return (False, None)


def exponentfloat_state_3():
    global int_value
    global floatexp_value
    ch = next_char()
    if ch == END:
        return (False, None)
    if ch == "E" or ch == "e":
        return exponentfloat_state_4()
    if digit(ch):
        floatexp_value += 1
        int_value = int_value * 10 + int(ch)
        return exponentfloat_state_3()
    return (False, None)


# Partie exponent
###########################
def exponentfloat_state_4():
    global exp_value
    global sign_value
    ch = next_char()
    if ch == END:
        return (False, None)
    if ch == "+" or ch == "-":
        if ch == "+":
            sign_value = 1
        else:
            sign_value = -1
        return exponentfloat_state_5()
    if digit(ch):
        sign_value = 1
        exp_value = int(ch)
        return exponentfloat_state_6()
    return (False, None)

def exponentfloat_state_5():
    global exp_value
    global sign_value
    ch = next_char()
    if ch == END:
        return (False, None)
    if digit(ch):
        exp_value = int(ch)
        return exponentfloat_state_6()
    return (False, None)


def exponentfloat_state_6():
    global exp_value
    global sign_value
    global int_value
    global floatexp_value
    ch = next_char()
    if ch == END:
        return (True, int_value * (10 ** (-floatexp_value + sign_value * exp_value)))
    if digit(ch):
        exp_value = exp_value * 10 + int(ch)
        return exponentfloat_state_6()
    return (False, None)
    

def number():
    global exp_value
    global int_value
    global floatexp_value
    global sign_value
    exp_value = 0
    int_value = 0
    floatexp_value = 0
    sign_value = 0
    init_char()
    return number_0()


def number_0():
    global exp_value
    global int_value
    global floatexp_value
    global sign_value
    ch = next_char()
    if ch == END or ch == " ":
        return (False, None)
    if ch == "0":
        return number_1()
    if nonzerodigit(ch):
        int_value = int(ch)
        return number_2()
    if ch == ".":
        return number_3()
    return (False, None)


def number_1():
    global exp_value
    global int_value
    global floatexp_value
    global sign_value
    ch = next_char()
    if ch == END or ch == " ":
        return (True, 0)
    if ch == "E" or ch == "e":
        return number_6()
    if nonzerodigit(ch):
        int_value += int(ch)
        return number_5()
    if ch == ".":
        return number_4()
    if ch == "0":
        return number_1()
    return (False, None)


def number_2():
    global exp_value
    global int_value
    global floatexp_value
    global sign_value
    ch = next_char()
    if ch == END or ch == " ":
        return (True, int_value)
    if digit(ch):
        int_value = int_value * 10 + int(ch)
        return number_2()
    if ch == ".":
        return number_4()
    if ch == "E" or ch == "e":
        return number_6()
    return (False, None)


def number_3():
    global exp_value
    global int_value
    global floatexp_value
    global sign_value
    ch = next_char()
    if ch == END or ch == " ":
        return (False, None)
    if digit(ch):
        int_value = int(ch)
        floatexp_value += 1
        return number_4()
    return (False, None)


def number_4():
    global exp_value
    global int_value
    global floatexp_value
    global sign_value
    ch = next_char()
    if ch == END or ch == " ":
        return (True, int_value * (10 ** - floatexp_value))
    if digit(ch):
        int_value = int_value * 10 + int(ch)
        floatexp_value += 1
        return number_4()
    if ch == "E" or ch == "e":
        return number_6()
    return (False, None)


def number_5():
    global exp_value
    global int_value
    global floatexp_value
    global sign_value
    ch = next_char()
    if ch == END or ch == " ":
        return (False, None)
    if digit(ch):
        int_value = int_value * 10 + int(ch)
        return number_5()
    if ch == ".":
        return number_4()
    if ch == "E" or ch == "e":
        return number_4()
    return (False, None)


def number_6():
    global exp_value
    global int_value
    global floatexp_value
    global sign_value
    ch = next_char()
    if ch == END or ch == " ":
        return (False, None)
    if ch == "+" or ch == "-":
        if ch == "+":
            sign_value = 1
        else:
            sign_value = -1
        return number_7()
    if digit(ch):
        sign_value = 1
        exp_value = int(ch)
        return number_8()
    return (False, None)


def number_7():
    global exp_value
    global int_value
    global floatexp_value
    global sign_value
    ch = next_char()
    if ch == END or ch == " ":
        return (False, None)
    if digit(ch):
        exp_value = int(ch)
        return number_8()
    return (False, None)


def number_8():
    global exp_value
    global int_value
    global floatexp_value
    global sign_value
    ch = next_char()
    if ch == END or ch == " ":
        return (True, int_value * 10 ** (sign_value * exp_value - floatexp_value))
    if digit(ch):
        exp_value = exp_value * 10 + int(ch)
        return number_8()
    return (False, None)



########################
#####    Projet    #####
########################


V = set(('.', 'e', 'E', '+', '-', '*', '/', '(', ')', ' ')
        + tuple(str(i) for i in range(10)))


############
# Question 10 : eval_exp

def eval_exp():
    ch = next_char()
    if ch == '+':
        n1 = eval_exp()
        n2 = eval_exp()
        return n1 + n2
    if ch == '-':
        n1 = eval_exp()
        n2 = eval_exp()
        return n1 - n2
    if ch == '*':
        n1 = eval_exp()
        n2 = eval_exp()
        return n1 * n2
    if ch == '/':
        n1 = eval_exp()
        n2 = eval_exp()
        return n1 / n2
    val = number()
    return val[1]
    

############
# Question 12 : eval_exp corrigé

current_char = ''

# Accès au caractère suivant de l'entrée sans avancer
def peek_char():
    global current_char
    if current_char == '':
        current_char = INPUT_STREAM.read(1)
    ch = current_char
    # print("@", repr(ch))  # decommenting this line may help debugging
    if ch in V or ch in END:
        return ch
    raise Error('character ' + repr(ch) + ' unsupported')

def consume_char():
    global current_char
    current_char = ''


def number_v2():
    global exp_value
    global int_value
    global floatexp_value
    global sign_value
    exp_value = 0
    int_value = 0
    floatexp_value = 0
    sign_value = 0
    init_char()
    return number_v2_0()


def number_v2_0():
    global exp_value
    global int_value
    global floatexp_value
    global sign_value
    ch = peek_char()
    if ch == END or ch == " ":
        return (False, None)
    consume_char()
    if ch == "0":
        return number_v2_1()
    if nonzerodigit(ch):
        int_value = int(ch)
        return number_v2_2()
    if ch == ".":
        return number_v2_3()
    return (False, None)


def number_v2_1():
    global exp_value
    global int_value
    global floatexp_value
    global sign_value
    ch = peek_char()
    if ch == END or ch == " ":
        return (True, 0)
    consume_char()
    if ch == "E" or ch == "e":
        return number_v2_6()
    if nonzerodigit(ch):
        int_value += int(ch)
        return number_5()
    if ch == ".":
        return number_4()
    if ch == "0":
        return number_1()
    return (False, None)


def number_v2_2():
    global exp_value
    global int_value
    global floatexp_value
    global sign_value
    ch = peek_char()
    if ch == END or ch == " ":
        return (True, int_value)
    consume_char()
    if digit(ch):
        int_value = int_value * 10 + int(ch)
        return number_v2_2()
    if ch == ".":
        return number_v2_4()
    if ch == "E" or ch == "e":
        return number_v2_6()
    return (False, None)


def number_v2_3():
    global exp_value
    global int_value
    global floatexp_value
    global sign_value
    ch = peek_char()
    if ch == END or ch == " ":
        return (False, None)
    consume_char()
    if digit(ch):
        int_value = int(ch)
        floatexp_value += 1
        return number_v2_4()
    return (False, None)


def number_v2_4():
    global exp_value
    global int_value
    global floatexp_value
    global sign_value
    ch = peek_char()
    if ch == END or ch == " ":
        return (True, int_value * (10 ** - floatexp_value))
    consume_char()
    if digit(ch):
        int_value = int_value * 10 + int(ch)
        floatexp_value += 1
        return number_v2_4()
    if ch == "E" or ch == "e":
        return number_v2_6()
    return (False, None)


def number_v2_5():
    global exp_value
    global int_value
    global floatexp_value
    global sign_value
    ch = peek_char()
    if ch == END or ch == " ":
        return (False, None)
    consume_char()
    if digit(ch):
        int_value = int_value * 10 + int(ch)
        return number_v2_5()
    if ch == ".":
        return number_v2_4()
    if ch == "E" or ch == "e":
        return number_v2_4()
    return (False, None)


def number_v2_6():
    global exp_value
    global int_value
    global floatexp_value
    global sign_value
    ch = peek_char()
    if ch == END or ch == " ":
        return (False, None)
    consume_char()
    if ch == "+" or ch == "-":
        if ch == "+":
            sign_value = 1
        else:
            sign_value = -1
        return number_v2_7()
    if digit(ch):
        sign_value = 1
        exp_value = int(ch)
        return number_v2_8()
    return (False, None)


def number_v2_7():
    global exp_value
    global int_value
    global floatexp_value
    global sign_value
    ch = peek_char()
    if ch == END or ch == " ":
        return (False, None)
    consume_char()
    if digit(ch):
        exp_value = int(ch)
        return number_v2_8()
    return (False, None)


def number_v2_8():
    global exp_value
    global int_value
    global floatexp_value
    global sign_value
    ch = peek_char()
    if ch == END or ch == " ":
        return (True, int_value * 10 ** (sign_value * exp_value - floatexp_value))
    consume_char()
    if digit(ch):
        exp_value = exp_value * 10 + int(ch)
        return number_8()
    return (False, None)


def eval_exp_v2():
    ch = peek_char()
    consume_char()
    if ch == '+':
        n1 = eval_exp_v2()
        n2 = eval_exp_v2()
        print(n2)
        return n1 + n2
    if ch == '-':
        n1 = eval_exp_v2()
        n2 = eval_exp_v2()
        return n1 - n2
    if ch == '*':
        n1 = eval_exp_v2()
        n2 = eval_exp_v2()
        return n1 * n2
    if ch == '/':
        n1 = eval_exp_v2()
        n2 = eval_exp_v2()
        return n1 / n2
    val = number_v2()
    return val[1]

############
# Question 14 : automate pour Lex

operator = set(['+', '-', '*', '/'])
criterefin=set(['+', '-', '*', '/',' ',END])

def numberq14():
    init_char()
    return( number_state_0q14()) 

def number_state_0q14():
    c = next_char()
    initvalue=0
    if c=='0':
        return (number_state_1q14(initvalue))
    elif nonzerodigit(c):
        initvalue=initvalue*10+int(c)
        return (number_state_2q14(initvalue))
    elif c=='.':
        exp_value =0
        test=True
        return (number_state_3q14(initvalue,test,exp_value))
    else:
        return (False,None)

def number_state_1q14(initvalue):
    c=next_char()
    exp_value=0
    if c=='0':
        return (number_state_1q14(initvalue))
    elif nonzerodigit(c):
        initvalue=initvalue*10+int(c)
        return (number_state_5q14(initvalue))
    elif c=='.':
        exp_value =0
        test=True
        return (number_state_4q14(initvalue,test,exp_value)) 
    elif c=='E' or c=='e':
        signvaleur=1 
        aftersign=0
        return (number_state_6q14(initvalue,signvaleur,aftersign,exp_value))
    elif c in criterefin:
        return (True,initvalue)
    else:
        return (False,None)
def number_state_2q14(initvalue):
    c=next_char()
    exp_value=0
    if digit(c):
        initvalue=initvalue*10+int(c)
        return (number_state_2q14(initvalue))
    elif c=='.':
        exp_value =0
        test=True
        return (number_state_4q14(initvalue,test,exp_value))
    elif c=='E' or c=='e':
        signvaleur=1 
        aftersign=0
        return (number_state_6q14(initvalue,signvaleur,aftersign,exp_value))
    elif c in criterefin:
        return (True,initvalue)
    else:
        return (False,None)
def number_state_3q14(initvalue,test,exp_value): 
    c=next_char()
    if test:
        exp_value+=1
    if digit(c):
        initvalue=initvalue*10+int(c)
        return (number_state_4q14(initvalue,test,exp_value))
    elif c== END:
        return (False,None)
    else:
        return (False,None)
def number_state_4q14(initvalue,test,exp_value):
    c=next_char()
    if digit(c):
        if test:
            exp_value+=1
        initvalue=initvalue*10+int(c)
        return (number_state_4q14(initvalue,test,exp_value))
    elif c=='E' or c=='e':
        signvaleur=1
        aftersign=0
        return (number_state_6q14(initvalue,signvaleur,aftersign,exp_value))
    elif c in criterefin:
        return (True,initvalue*10**(-1*exp_value))
    else:
        return (False,None)
def number_state_5q14(initvalue):
    c=next_char()
    if digit(c):
        initvalue=initvalue*10+int(c)
        return (number_state_5q14(initvalue))
    elif c=='.':
        exp_value =0
        test=True
        return (number_state_4q14(initvalue,test,exp_value))
    elif c=='E' or c=='e':
        exp_value =0
        signvaleur=1 
        aftersign=0
        return (number_state_6q14(initvalue,signvaleur,aftersign,exp_value))
    elif c== END:
        return (False,None)
    else:
        return (False,None)
def number_state_6q14(initvalue,signvaleur,aftersign,exp_value):
    c=next_char()
    if digit(c):
        aftersign=int(c)+aftersign*10
        return (number_state_8q14(initvalue,signvaleur,aftersign,exp_value))
    elif c=='+' or c=='-':
        if c=='-':
            signvaleur=-1
        else:
             signvaleur=1
        return (number_state_7q14(initvalue,signvaleur,aftersign,exp_value))    
    elif c== END:
        return (False,None)
    else:
        return (False,None)
def number_state_7q14(initvalue,signvaleur,aftersign,exp_value):
    c=next_char()
    if digit(c):
        aftersign=int(c)+aftersign*10
        return (number_state_8q14(initvalue,signvaleur,aftersign,exp_value))
    elif c== END:
        return (False,None)
    else:
        return (False,None)
def number_state_8q14(initvalue,signvaleur,aftersign,exp_value):
    c=next_char()
    if digit(c):
        aftersign=int(c)+aftersign*10
        return (number_state_8q14(initvalue,signvaleur,aftersign,exp_value))
    elif c in criterefin:
        return (True,initvalue*10**(-1*exp_value)*10**(aftersign*signvaleur))
    else:
        return (False,None)

def FA_Lex():
    init_char()
    c=next_char()
    if c in operator:
        return(True)
    elif c==')' or c=='(':
        return(True)
    else:
        initvalue=0
        if c=='0':
            return (number_state_1(initvalue))
        elif nonzerodigit(c):
            initvalue=initvalue*10+int(c)
            return (number_state_2(initvalue))
        elif c=='.':
            exp_value =0
            test=True
            return (number_state_3(initvalue,test,exp_value))
        else:
            return (False,None)



############
# Question 15 : automate pour Lex avec token

# Token
NUM, ADD, SOUS, MUL, DIV, OPAR, FPAR = range(7)
token_value = 0

def numberq15():
    init_char()
    return( number_state_0q15()) 

def number_state_0q15():
    c = next_char()
    initvalue=0
    if c=='0':
        return (number_state_1q15(initvalue))
    elif nonzerodigit(c):
        initvalue=initvalue*10+int(c)
        return (number_state_2q15(initvalue))
    elif c=='.':
        exp_value =0
        test=True
        return (number_state_3q15(initvalue,test,exp_value))
    else:
        return (False,None)

def number_state_1q15(initvalue):
    c=next_char()
    exp_value=0
    if c=='0':
        return (number_state_1q15(initvalue))
    elif nonzerodigit(c):
        initvalue=initvalue*10+int(c)
        return (number_state_5q15(initvalue))
    elif c=='.':
        exp_value =0
        test=True
        return (number_state_4q15(initvalue,test,exp_value)) 
    elif c=='E' or c=='e':
        signvaleur=1 
        aftersign=0
        return (number_state_6q15(initvalue,signvaleur,aftersign,exp_value))
    elif c in criterefin:
        return (True,initvalue,'NUM')
    else:
        return (False,None)
def number_state_2q15(initvalue):
    c=next_char()
    exp_value=0
    if digit(c):
        initvalue=initvalue*10+int(c)
        return (number_state_2q15(initvalue))
    elif c=='.':
        exp_value =0
        test=True
        return (number_state_4q15(initvalue,test,exp_value))
    elif c=='E' or c=='e':
        signvaleur=1 
        aftersign=0
        return (number_state_6q15(initvalue,signvaleur,aftersign,exp_value))
    elif c in criterefin:
        return (True,initvalue,'NUM')
    else:
        return (False,None)
def number_state_3q15(initvalue,test,exp_value): 
    c=next_char()
    if test:
        exp_value+=1
    if digit(c):
        initvalue=initvalue*10+int(c)
        return (number_state_4q15(initvalue,test,exp_value))
    elif c== END:
        return (False,None)
    else:
        return (False,None)
def number_state_4q15(initvalue,test,exp_value):
    c=next_char()
    if digit(c):
        if test:
            exp_value+=1
        initvalue=initvalue*10+int(c)
        return (number_state_4q15(initvalue,test,exp_value))
    elif c=='E' or c=='e':
        signvaleur=1
        aftersign=0
        return (number_state_6q15(initvalue,signvaleur,aftersign,exp_value))
    elif c in criterefin:
        return (True,initvalue*10**(-1*exp_value),'NUM')
    else:
        return (False,None)
def number_state_5q15(initvalue):
    c=next_char()
    if digit(c):
        initvalue=initvalue*10+int(c)
        return (number_state_5q15(initvalue))
    elif c=='.':
        exp_value =0
        test=True
        return (number_state_4q15(initvalue,test,exp_value))
    elif c=='E' or c=='e':
        exp_value =0
        signvaleur=1 
        aftersign=0
        return (number_state_6q15(initvalue,signvaleur,aftersign,exp_value))
    elif c== END:
        return (False,None)
    else:
        return (False,None)
def number_state_6q15(initvalue,signvaleur,aftersign,exp_value):
    c=next_char()
    if digit(c):
        aftersign=int(c)+aftersign*10
        return (number_state_8q15(initvalue,signvaleur,aftersign,exp_value))
    elif c=='+' or c=='-':
        if c=='-':
            signvaleur=-1
        else:
             signvaleur=1
        return (number_state_7q15(initvalue,signvaleur,aftersign,exp_value))    
    elif c== END:
        return (False,None)
    else:
        return (False,None)
def number_state_7q15(initvalue,signvaleur,aftersign,exp_value):
    c=next_char()
    if digit(c):
        aftersign=int(c)+aftersign*10
        return (number_state_8q15(initvalue,signvaleur,aftersign,exp_value))
    elif c== END:
        return (False,None)
    else:
        return (False,None)
def number_state_8q15(initvalue,signvaleur,aftersign,exp_value):
    c=next_char()
    if digit(c):
        aftersign=int(c)+aftersign*10
        return (number_state_8q15(initvalue,signvaleur,aftersign,exp_value))
    elif c in criterefin:
        return (True,initvalue*10**(-1*exp_value)*10**(aftersign*signvaleur),'NUM')
    else:
        return (False,None)

def FA_Lex_w_token():
    init_char()
    c=next_char()
    if c in LISTE:
        i=index(LISTE)+1
        return(True,i)
    else:
        initvalue=0
        if c=='0':
            return (number_state_1q15(initvalue))
        elif nonzerodigit(c):
            initvalue=initvalue*10+int(c)
            return (number_state_2q15(initvalue))
        elif c=='.':
            exp_value =0
            test=True
            return (number_state_3q15(initvalue,test,exp_value))
        else:
            return (False,None)



# Fonction de test
if __name__ == "__main__":
    print("@ Test interactif de l'automate")
    print("@ Vous pouvez changer l'automate testé en modifiant la fonction appelée à la ligne 'ok = ... '.")
    print("@ Tapez une entrée:")
    try:
        # ok = pointfloat_Q2() # changer ici pour tester un autre automate sans valeur
        # ok, val = pointfloat() # changer ici pour tester un autre automate avec valeur
        ok, val = True, eval_exp_v2() # changer ici pour tester eval_exp et eval_exp_v2
        if ok:
            print("Accepted!")
            print("value:", val) # décommenter ici pour afficher la valeur (question 4 et +)
        else:
            print("Rejected!")
            print("value so far:", int_value) # décommenter ici pour afficher la valeur en cas de rejet
    except Error as e:
        print("Error:", e)
