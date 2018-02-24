from __future__ import division
from math import sqrt
import sys

def check_valid_expo(expo):
    ret = expo.split()
    elements = []
    for elem in ret:
        if '^' in elem:
            elements.append(elem)
        flag = ['0', '1', '2']
        for elel in elements:
            res = elel.split('^')
            if res[1] not in flag:
                print("On ne gere pas les puissance de " + res[1])
                exit()

def separate_side(dico):
    equal = 0
    new_dico = {'left':[], 'right':[]}
    for elem in dico:
        if elem == '=':
            equal = 1
            continue
        if equal == 0:
            new_dico['left'].append(elem)
        else:
            new_dico['right'].append(elem)
    return new_dico

def is_positiv(elem):
    if elem[0] == '-':
        return False
    return True

def put_same_side(dico):
    for elem in dico['right']:
        if is_positiv(elem) == True:
            dico['left'].append('-' + elem)
        else:
            dico['left'].append(elem.replace('-', ''))
    dico['right'] = 0
    return dico['left']

def separate_by_expo(expo, equation):
    find = []
    for elem in equation:
        if expo is None:
            if '^' not in elem and 'X' in elem:
                find.append(elem)
        elif expo is 'simple':
            if '^' not in elem and 'X' not in elem:
                find.append(elem)
        else:
            search = '^' + str(expo)
            if search in elem:
                find.append(elem)
    return find

def get_simple_terms(lst1, lst2):
    value = 0
    for elem in lst1:
        if elem == 'X^0':
            value = value + 1
        elif '*X^0' in elem:
            calcul = elem.replace('X^0', '1').split('*')
            value = value + float(calcul[0]) * float(calcul[1])
        else:
            calcul = elem.replace('X^0', '*1').split('*')
            value = value + float(calcul[0]) * float(calcul[1])

    for elem in lst2:
        if '*' in elem:
            val = elem.split('*')
            value = value + float(val[0]) * float(val[1])
        else:
            value = value + float(elem)
    return value

def get_expo_one_terms(lst1, lst2):
    value = 0 
    for elem in lst1:
        if elem == 'X^1':
            value = value + 1
        else:
            value = value + float(elem.replace('*X^1', ''))

    for elem in lst2:
        if elem == 'X':
            value = value + 1
        else:
           value = value + float(elem.replace('*X', ''))
    return value


def print_reduced_equation(equation):
    str = ''
    for elem in equation:
        if str == '':
            str = '(' + elem + ')'
        else:
            str = str + ' + (' + elem + ')'
    str = str + ' = 0'
    print('Reduced form: ' + str)

def change_state(elem):
    if is_positiv(elem):
        return '-' + elem
    return elem.replace('-', '')



def solve_equation_one(expo1, simple):
    right = change_state(str(simple))
    print('X = ' + str(right) + '/' + str(expo1))
    res = float(right) / float(expo1)
    print('X = ' + str(round(res, 3)))


def get_expo_two_terms(lst):
    value = 0
    for elem in lst:
        if elem == 'X^2':
            value = value + 1
        else:
            value = value + float(elem.replace('*X^2', ''))
    return value


def get_determinant(a, b, c):
    res = b**2-4*a*c
    return res

def  first_solution(delta, a, b):
    #(-b-Vdelta)/2a
    print(round((float(-b)-sqrt(delta))/(2*a), 6))

def  second_solution(delta, a, b):
    #(-b+Vdelta)/2a
    print(round((float(-b)+sqrt(delta))/(2*a), 6))

def solve_equation_two(delta, a, b, c):
    if delta > 0:
        print('Discriminant is strictly positive, the two solutions are:')
        first_solution(delta, a, b)
        second_solution(delta, a, b)
    elif delta == 0:
        print('Discriminant is equal to zero, the only one solution is:')
        print(round((float(-b))/(2*a), 6))
    else:
        print('Discriminant is strictly negative, no solution possible in R')
        print('(' + str(a) + 'X^2) + (' + str(b) + 'X) + (' + str(c) + ') = 0')

def number_of_x(liste):
    count = 0
    for elem in liste:
        ret =  elem.replace('X', '1')
        if '*' in ret:
            res = ret.split('*')
            count += (float(res[0]) * float(res[1]))
        else:
            count += float(ret)
    return count

def calculate_simple(x, simple):
    if is_positiv(str(simple)) is True:
        right = float('-' + str(simple))
    else:
        right = float(str(simple).replace('-', ''))
    if x != 0 and x != -1:
        equat = 'X = ' + str(right) + '/' + str(x)
        print(equat)
        result = (right / x)
        return str(result)
    else:
        return None


def launch_prog(equat):
    print('Equation: ' + equat)
    check_valid_expo(equat)
    equat = equat.replace(' * ', '*').replace(' - ', ' -').replace(' + ', ' ').replace('--', '')
    dico = separate_side(equat.split(' '))
    equation = put_same_side(dico)
    level_dico = {}
    level_dico['a'] = separate_by_expo(2, equation)
    level_dico['b'] = separate_by_expo(1, equation)
    level_dico['c'] = separate_by_expo(0, equation)
    level_dico['d'] = separate_by_expo(None, equation)
    level_dico['e'] = separate_by_expo('simple', equation)

    if level_dico['a']:
        print('C\'est une equation du 2nd degres')
        expo2 = get_expo_two_terms(level_dico['a'])
        expo1 = get_expo_one_terms(level_dico['b'], level_dico['d'])
        simple = get_simple_terms(level_dico['c'], level_dico['e'])

        print("Reduced equation: (" + str(expo2) + 'x^2) + (' + str(expo1) + 'x) + (' + str(simple) + ') = 0')
        determinant = get_determinant(expo2, expo1, simple)
        solve_equation_two(determinant, expo2, expo1, simple)
    elif level_dico['b']:
        print('C\'est une equation du 1er degres')
        expo1 = get_expo_one_terms(level_dico['b'], level_dico['d'])
        simple = get_simple_terms(level_dico['c'], level_dico['e'])

        if expo1 == 0:
            print(str(expo1) + ' = ' + str(simple))
            print("Pas de solution")
        else:
            print("Reduced equation: (" + str(expo1) + 'X) + (' + str(simple) + ') = 0')
            print("The solution is:")
            solve_equation_one(expo1, simple)
    else:
        print('Polynomial degree: 0')
        simple_val = get_simple_terms(level_dico['c'], level_dico['e'])
        x = number_of_x(level_dico['d'])
        result = calculate_simple(x, simple_val)
        if result is None:
            print('vrai pour tout les X')
        else:
            print('The solution is:\nX = ' + result)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("The only argument must be an equation")
        exit()
    try:
        launch_prog(sys.argv[1])
    except:
        print("The is an error with the parameter sent")
        exit()
