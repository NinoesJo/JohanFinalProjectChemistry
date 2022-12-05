"""
Notify the user if their equation is balanced or not and then balance the equation if it is necessary.
Author: Johan Nino Espino
Creation Date: 11/29/2022
"""
#
def lcm_array(list):
    lcm = list[0]
    for index in range(1, len(list)):
        lcm = lcm * list[index] // math.gcd(lcm, list[index])
    return lcm
#

import re
from sympy import *
from fractions import Fraction
import math

def getUserInput():
    ######################################
    #Grab number of reactants and products
    ######################################
    numReactants = input("Enter the number of reactants (Enter 1 or 2): ")
    while not numReactants.isdigit() or (int(numReactants) != 1 and int(numReactants) != 2):
        print('Invalid input, please try again\n')
        numReactants = input("Enter the number of reactants (Enter 1 or 2): ")

    numProducts = input("Enter the number of products (Enter 1 or 2): ")
    while not numProducts.isdigit() or (int(numProducts) != 1 and int(numProducts) != 2):
        print('Invalid input, please try again\n')
        numProducts = input("Enter the number of products (Enter 1 or 2): ")
    
    ################################
    #Grab reactants and products
    ################################
    position = ['first', 'second']

    reactant_list = []
    for i in range(int(numReactants)):
        reactant = str(input("Enter the " + position[i] + " reactant: "))
        reactant_list.append(reactant)
    
    product_list = []
    for i in range(int(numProducts)):
        product = str(input("Enter the " + position[i] + " product: "))
        product_list.append(product)
    
    return (reactant_list, product_list)

def grabMergeCompoundDictionary(reactant_list, product_list):
    reactant_dic_list = []
    for reactant in reactant_list:
        reactant_dic = createCompoundDictionary(reactant)
        reactant_dic_list.append(reactant_dic)
    
    merge_reactant_dic = mergeCompoundDictionary(reactant_dic_list, 0)

    product_dic_list = []
    for product in product_list:
        product_dic = createCompoundDictionary(product)
        product_dic_list.append(product_dic)
    
    merge_product_dic = mergeCompoundDictionary(product_dic_list, 0)

    return (merge_reactant_dic, merge_product_dic)

# For each reactant and product create it's own dictionary, then merge both reactants/products and compare if balance
def checkChemicalBalance(reactantList, productList):
    (reactantDictionary, productDictionary) = grabMergeCompoundDictionary(reactantList, productList)

    matchCount = 0
    for (key, reactantCount) in reactantDictionary.items():
        productCount = productDictionary[key]
        if reactantCount == productCount:
            matchCount += 1
    
    if matchCount == len(reactantDictionary):
        return True
    return False

# Merge two compounds dictionary and apply coefficient
def mergeCompoundDictionary(compound_dic, coefficient):
    if len(compound_dic) == 1:
        merge = compound_dic[0]
        if coefficient > 1:
            for key in merge:
                merge[key] *= coefficient
        return merge
    
    merge = {}
    first_compound = compound_dic[0]
    second_compound = compound_dic[1]

    for key, value in first_compound.items():
        if key in merge:
           merge[key] += value
        else:
            merge[key] = value

    for key, value in second_compound.items():
        if key in merge:
           merge[key] += value
        else:
            merge[key] = value

    if coefficient > 1:
        for key in merge:
            merge[key] *= coefficient

    return merge

#Create dictionary for a given compound
def createCompoundDictionary(compound):
    (coefficient, compound) = getCoefficient(compound)

    temp_compound = compound.replace('(', ' ')
    temp_compound = temp_compound.replace(')', ' ')
    subgroups = createSubgroups(temp_compound.split())
    subgroups_list = []

    for (subcompound, outer_subscript) in subgroups:
        subgroup_dic = grabUniqueElementsFromSubCompound(subcompound, int(outer_subscript))
        subgroups_list.append(subgroup_dic)

    return mergeCompoundDictionary(subgroups_list, int(coefficient))

#Create subgroups for a given compound to handle outer subscripts for parenthesis
# Ex: compound: (CH4)2              (CO2)4(CH4)2
#     return: [('CH4', 2)]          [('CO2', 4), ('CH4', 2)]
def createSubgroups(subcompounds_list):
    if len(subcompounds_list) == 1:
        return [(subcompounds_list[0], 1)]

    subgroups = []
    i = 1
    while i < len(subcompounds_list):
        subcompound = subcompounds_list[i-1]
        outer_subscript = subcompounds_list[i]

        if isinstance(subcompound, str) and outer_subscript.isdigit():
            subgroups.append((subcompound, outer_subscript))
            i+=2        
        else:
            subgroups.append((subcompound, 1))
            i+=1
    return subgroups

def grabUniqueElementsFromSubCompound(subcompound, outer_script):
    element_dic = {}
    element_list = [char for char in subcompound if not char.isdigit()]

    if len(element_list) == 1:
        curr_element = element_list[0]
        element_dic[element_list[0]] = 1
        index = subcompound.find(curr_element) + len(curr_element)
        subscript = grabSubscript(subcompound, index)
        
        if subscript > 0:
                element_dic[curr_element] = subscript
        return element_dic
    
    i = 1
    while i < len(element_list):
        prev_char = element_list[i-1]
        curr_char = element_list[i]

        if prev_char.isupper() and curr_char.islower():
            curr_element = prev_char + curr_char
            element_dic[curr_element] = 1

            index = subcompound.find(curr_element) + len(curr_element)
            subscript = grabSubscript(subcompound, index)

            if subscript > 0:
                element_dic[curr_element] = subscript
            
            if outer_script > 1:
                element_dic[curr_element] *= int(outer_script)
                        
        
        if prev_char.isupper() and curr_char.isupper():
            element_dic[prev_char] = 1

            index = subcompound.find(prev_char) + len(prev_char)
            subscript = grabSubscript(subcompound, index)

            if subscript > 0:
                element_dic[prev_char] = subscript
            
            if outer_script > 1:
                element_dic[prev_char] *= outer_script

        i+= 1
    
    if element_list[-1].isupper():
        curr_char = element_list[-1]
        element_dic[curr_char] = 1
        
        index = subcompound.find(curr_char) + len(curr_char)
        
        if index < len(subcompound):
            subscript = grabSubscript(subcompound, index)

            if subscript > 0:
                element_dic[curr_char] = subscript
            
        if outer_script > 1:
            element_dic[curr_char] *= outer_script


    return element_dic

def grabSubscript(compound, start_index):
    end_index = start_index
    while end_index < len(compound):
        if not compound[end_index].isdigit():
            break
        end_index += 1
    
    if start_index == end_index:
        return 1

    return int(compound[start_index: end_index])

def getCoefficient(compound):
    i = 0
    while i < len(compound):
        element = compound[i]
        if element.isdigit():
            i+=1
            continue
        break
    
    if i == 0:
        return (1, compound)
    return (compound[:i], compound[i:])

# REMOVE
def balanceChemicalEquation(reactantList, productList):
    
    reactantDictionary, productDictionary = grabMergeCompoundDictionary(reactantList, productList)
    balance = checkChemicalBalance(reactantList, productList)
    
    finalReactantList = reactantList
    finalProducList = productList

    while not balance:
        elementListNotBalance = elementsNotBalance(reactantDictionary, productDictionary)
        elementListNotBalance.sort(key = lambda x: x[1])

        sideWithMore = elementListNotBalance[0][2]

        if sideWithMore == 'reactant':
            productListUpdate= updateProducts(elementListNotBalance[0], productList)
            reactantDictionary, productDictionary = grabMergeCompoundDictionary(reactantList, productListUpdate)
            finalProducList = productListUpdate
            balance = checkChemicalBalance(reactantList, productListUpdate)

        else:
            reactantListUpdate = updateReactants(elementListNotBalance[0], reactantList)
            reactantDictionary, productDictionary = grabMergeCompoundDictionary(reactantListUpdate, productList)
            finalReactantList = reactantListUpdate
            balance = checkChemicalBalance(reactantListUpdate, productList)
                
    return (finalReactantList, finalProducList)

# REMOVE
def updateProducts(element, productList):
    elementType = element[0]
    countDifference = element[1]

    for i in range(len(productList)):
        compound = productList[i]
        (coefficient, compound) = getCoefficient(compound)
        
        if compound.find(elementType) > -1:
            index = compound.find(elementType) + len(elementType)
            subscript = grabSubscript(compound, index)

            if subscript > 1:
                targetCount = subscript*int(coefficient) + countDifference
                newCompound = compound

                if targetCount%subscript == 0:
                    newCompound = str(int(targetCount/subscript)) + compound
                else:
                    newCompound = str(int(targetCount/subscript) + 1) + compound
                productList[i] = newCompound
                break

            newCompound = str(int(coefficient) + countDifference) + compound
            productList[i] = newCompound
            break

    return productList

#REMOVE
def updateReactants(element, reactantList):
    elementType = element[0]
    countDifference = element[1]

    for i in range(len(reactantList)):
        compound = reactantList[i]
        (coefficient, compound) = getCoefficient(compound)

        if compound.find(elementType) > -1:
            index = compound.find(elementType) + len(elementType)
            subscript = grabSubscript(compound, index)

            if subscript > 1:
                targetCount = subscript*int(coefficient) + countDifference
                newCompound = compound

                if targetCount%subscript == 0:
                    newCompound = str(int(targetCount/subscript)) + compound
                else:
                    newCompound = str(int(targetCount/subscript) + 1) + compound
                reactantList[i] = newCompound
                break

            newCompound = str(int(coefficient) + countDifference) + compound
            reactantList[i] = newCompound
            break

    return reactantList

# REMOVE
def elementsNotBalance(reactantDictionary, productDictionary):

    elementListNotBalance = []

    for (element, reactantCount) in reactantDictionary.items():
        productCount = productDictionary[element]
        if reactantCount > productCount:
            elementListNotBalance.append([element, reactantCount - productCount, 'reactant'])
        if productCount > reactantCount:
            elementListNotBalance.append([element, productCount - reactantCount, 'product'])

    return elementListNotBalance


def balanceEquations(resetReactantList, resetProductList):
    equations = createSystemOfEquations(resetReactantList, resetProductList)
    (matrix, usedLetters) = createMatrix(equations)

    for subMatrix in matrix:
        if subMatrix[-2] == 0 and subMatrix != matrix[-1]:
            print('Equation cannot be balanced')

            for i in range(len(resetReactantList)):
                resetReactantList[i] = resetReactantList[i][1:]
            
            for i in range(len(resetProductList)):
                resetProductList[i] = resetProductList[i][1:]
            return (resetReactantList, resetProductList)
    
    valueForVariable = {}
    for letter in usedLetters:
        valueForVariable[letter] = 0

    valueForVariable['a'] = matrix[0][-2]
    
    if 'b' in usedLetters:
        valueForVariable['b'] = matrix[1][-2]

    if 'c' in usedLetters and 'd' in usedLetters:
        if 'b' not in usedLetters:
            valueForVariable['c'] = matrix[1][-2]
        else:
            valueForVariable['c'] = matrix[2][-2]

    # SOLVE FOR MISSING VARIABLE
    if 'd' in usedLetters:
        valueForVariable = solveForMissingVariable(equations, valueForVariable, usedLetters, 'd')
    else:
        valueForVariable = solveForMissingVariable(equations, valueForVariable, usedLetters, 'c')

    lcm = leastCommonMultiple(valueForVariable)

    for variable, value in valueForVariable.items():
        valueForVariable[variable] = value*lcm

    #UPDATE
    for i in range(len(resetReactantList)):
        reactant = resetReactantList[i][1:]
        if i == 0:
            if valueForVariable['a'] > 1:
                resetReactantList[i] = str(valueForVariable['a']) + reactant
            else:
                resetReactantList[i] = reactant

        else:
            if valueForVariable['b'] > 1:
                resetReactantList[i] = str(valueForVariable['b']) + reactant
            else:
                resetReactantList[i] = reactant

    for i in range(len(resetProductList)):
        product = resetProductList[i][1:]
        
        if i == 0:
            if valueForVariable['c'] > 1:
                resetProductList[i] = str(valueForVariable['c']) + product
            else:
                resetProductList[i] = product
        else:
            if valueForVariable['d'] > 1:
                resetProductList[i] = str(valueForVariable['d']) + product
            else:
                resetProductList[i] = product

    return (resetReactantList, resetProductList)

def solveForMissingVariable(equations, valueForVariable, usedLetters, letterTarget):
    coefficientForVariable = {}
    
    for equation in equations.values():
        if equation.find(letterTarget) > -1:
            for letter in usedLetters:
                if equation.find(letter) > -1:
                    index = equation.find(letter[0])
                    coefficient = getCoefficientEquation(equation, index)
                        
                    if letter != letterTarget:
                        coefficientForVariable[letter] = -1*coefficient
                    else:
                        coefficientForVariable[letter] = coefficient
            break
                
    numerator = 0
    denominator = 0
    for letter, coefficient in coefficientForVariable.items():
        if letter != letterTarget:
            numerator += coefficient * valueForVariable[letter]

        else:
            denominator += coefficient
        
    valueForVariable[letterTarget] = numerator/denominator
    return valueForVariable

def leastCommonMultiple(valueForVariables):
    denominatorList = []
    negative = False
    for values in valueForVariables.values():
        if values < 0:
            negative = True
        denominatorList.append(Fraction(values).denominator)
    
    lcm = 0
    if len(denominatorList) == 4:
        lcm = math.lcm(denominatorList[0], denominatorList[1], denominatorList[2], denominatorList[3])
    elif len(denominatorList) == 3:
        lcm = math.lcm(denominatorList[0], denominatorList[1], denominatorList[2])
    else:
        lcm = math.lcm(denominatorList[0], denominatorList[1])

    if negative:
        lcm *= -1
    
    return lcm


def createMatrix(equationsDictionary):
    usedLetters = {'a': False, 'b': False, 'c': False, 'd': False}
    matrix = []

    for equation in equationsDictionary.values():
        for letter in usedLetters:
            if equation.find(letter) > -1:
                usedLetters[letter] = True
    
    #Remove unused variables
    lettersToRemove = [letter for letter, used in usedLetters.items() if used == False]

    for letter in lettersToRemove:
        del usedLetters[letter]

    for equation in equationsDictionary.values():
        subMatrix = [0] * (len(usedLetters) + 1)

        i = 0
        for letter in usedLetters:
            if equation.find(letter[0]) > -1:
                index = equation.find(letter[0])
                coefficient = getCoefficientEquation(equation, index) 
                subMatrix[i] = coefficient
            
            i += 1

        matrix.append(subMatrix)

    resultMatrix = Matrix(matrix).rref()[0]
    finalMatrix = []
    
    subMatrix = [0] * (len(usedLetters) + 1)
    for i in range(len(resultMatrix)):
        if (i+1) % len(subMatrix) == 0:
            finalMatrix.append(subMatrix)
            subMatrix = [0] * (len(usedLetters) + 1)
        
        subMatrix[i % len(subMatrix)] = resultMatrix[i]
    return (finalMatrix, usedLetters)

def getCoefficientEquation(equation, index):
    if index == 0:
        return 1

    i = index - 1
    while i > -1:
        number = equation[i]
        if number.isdigit() or number == '-' or number == '+':
            i-=1
            continue
        break
    
    if equation[i+1: index] == '-':
        return -1
    
    if equation[i+1: index] == '+':
        return 1

    return int(equation[i+1: index])

def createSystemOfEquations(resetReactantList, resetProductList):

    (reactantDictionary, productDictionary) = grabMergeCompoundDictionary(reactantList, productList)
    systemOfEquationsDictionary = {}
    
    for i in range(len(resetReactantList)):
        reactant = resetReactantList[i]

        for element in reactantDictionary:            
            compoundDictionary = createCompoundDictionary(reactant)       
            
            if element in compoundDictionary:
                index = reactant.find(element) + len(element)
                subscript = grabSubscript(reactant, index)

                subgroups = createSubgroups(reactant.replace(')', ' ').replace('(', ' ').split())
                outerSubscript = [outer_subscript for (subcompound, outer_subscript) in subgroups if subcompound.find(element) > -1][0]

                if subscript*outerSubscript == 1:
                    subscript = ""
                else:
                     subscript *= outerSubscript

                if element in systemOfEquationsDictionary:
                    systemOfEquationsDictionary[element] += '+' + str(subscript) + reactant[0]
                else:
                    systemOfEquationsDictionary[element] = str(subscript) + reactant[0]

    for i in range(len(resetProductList)):
        product = resetProductList[i]

        for element in productDictionary:
            compoundDictionary = createCompoundDictionary(product)       
            
            if element in compoundDictionary:
                index = product.find(element) + len(element)
                subscript = grabSubscript(product, index)

                subgroups = createSubgroups(product.replace(')', ' ').replace('(', ' ').split())
                outerSubscript = [int(outer_subscript) for (subcompound, outer_subscript) in subgroups if subcompound.find(element) > -1][0]

                if subscript*outerSubscript == 1:
                    subscript = ""
                else:
                     subscript *= outerSubscript

                systemOfEquationsDictionary[element] += '-' + str(subscript) + product[0]

    for element in systemOfEquationsDictionary:
        systemOfEquationsDictionary[element] += ' = 0'

    return systemOfEquationsDictionary

def resetCoefficient(reactantList, productList):
    for i in range(len(reactantList)):
        compound = reactantList[i]
        compoundResult = getCoefficient(compound)
        if i == 0:
            reactantList[i] = 'a' + compoundResult[1]
        else:
            reactantList[i] = 'b' + compoundResult[1]

    for i in range(len(productList)):
        compound = productList[i]
        compoundResult = getCoefficient(compound)
        if i == 0:
            productList[i] = 'c' + compoundResult[1]
        else:
            productList[i] = 'd' + compoundResult[1]

    return (reactantList, productList)

def printBalanceEquation(finalReactantList, finalProductList):
    reactantString = finalReactantList[0]

    if len(finalReactantList) > 1:
        reactantString = reactantString + ' + ' + finalReactantList[1]

    productString = finalProductList[0]

    if len(finalProductList) > 1:
        productString = productString + ' + ' + finalProductList[1]
    
    print(reactantString + ' -> ' + productString)

if __name__ == "__main__":
    (reactantList, productList) = getUserInput()
    balance = checkChemicalBalance(reactantList, productList)
    if balance:
        print("Your chemical equation is already balanced!")
    else:
        print("Your chemical equation was not balanced. Here's the balance equation: ")
        (resetReactantList, resetProductList) = resetCoefficient(reactantList, productList)
        (finalReactantList, finalProductList) = balanceEquations(resetReactantList, resetProductList)
        #(finalReactantList, finalProductList)= balanceChemicalEquation(resetReactantList, resetProductList)
        printBalanceEquation(finalReactantList, finalProductList)
