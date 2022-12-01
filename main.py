"""
Notify the user if their equation is balanced or not and then balance the equation if it is necessary.
Author: Johan Nino Espino
Creation Date: 11/29/2022
"""
import re

def getUserInput():
    ######################################
    #Grab number of reactants and products
    ######################################
    numReactants = input("Enter the number of reactants (Enter 1 or 2): ")
    while not numReactants.isdigit() and numReactants != 1 and numReactants != 2:
        print('Invalid input, please try again\n')
        numReactants = input("Enter the number of reactants (Enter 1 or 2): ")

    numProducts = input("Enter the number of products (Enter 1 or 2): ")
    while not numProducts.isdigit() and numProducts != 1 and numProducts != 2:
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
def checkChemicalBalance(reactant_list, product_list):
    (merge_reactant_dic, merge_product_dic) = grabMergeCompoundDictionary(reactant_list, product_list)

    count = 0
    for (key, reactant_count) in merge_reactant_dic.items():
        product_count = merge_product_dic[key]
        if reactant_count == product_count:
            count += 1
    
    if count == len(merge_reactant_dic):
        print("Your chemical equation is already balanced!")
        return True
    else:
        print("Your chemical equation is not balanced.")
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
        return 0

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
        return (0, compound)
    return (compound[:i], compound[i:])

if __name__ == "__main__":
    (reactant_list, product_list) = getUserInput()
    checkChemicalBalance(reactant_list, product_list)
    #print(item)


numReactants = int(input("Enter the number of reactants (Enter 1 or 2): ")) #Ask the number of reactants
numProducts = int(input("Enter the number of products (Enter 1 or 2): ")) #Ask the number of products

while numReactants != 1 and numReactants != 2: #Loops when numReactants is not 1 and 2
    numReactants = int(input("Enter the number of reactants (Enter 1 or 2): ")) #Ask the number of reactants
while numProducts != 1 and numProducts != 2: #Loops when numProducts is not 1 and 2
    numProducts = int(input("Enter the number of products (Enter 1 or 2): ")) #Ask the number of products

if numReactants == 1: #Checks if the user want to enter one reactant
    reactant1 = str(input("Enter the first reactant: ")) #Let the user enter a reactant

else: #The user want to enter two reactants
    reactant1 = str(input("Enter the first reactant: ")) #Let the user enter the first reactant
    reactant2 = str(input("Enter the second reactant: ")) #Let the user enter the second reactant

if numProducts == 1: #Checks if the user want to enter one product
    product1 = str(input("Enter the first product: ")) #Let the user enter a product
else: #The user want to enter two products
    product1 = str(input("Enter the first product: ")) #Let the user enter the first product
    product2 = str(input("Enter the second product: ")) #Let the user enter the second product

reactantElements = {} #This dictionary holds the reactant elements as keys and the number of elements as values
productElements = {} #This dictionary holds the product elements as keys and the number of elements as values

index = 0 #Initialize the variable index
tempElement = "" #Initialize the variable tempElement which stores the current element symbol
if reactant1[0].isnumeric() == True and reactant1[1].isnumeric() == True: #Coefficiant is a two-digit number
    coefficient1 = int(reactant1[0]) * 10 + int(reactant1[1]) #The integer becomes the coefficient
    index += 2 #Increment the index by 2
elif reactant1[0].isnumeric() == True: #Checks if the first element of the string is an integer
    coefficient1 = int(reactant1[0]) #The integer becomes the coefficient
    index += 1 #Increment the index value by 1
else: #The first element in the string is not an integer
    coefficient1 = 1 #Set the coefficient to 1
moles = 1 * coefficient1 #Initialize the moles value based on the coefficient value

while index < len(reactant1) and numReactants <= 2: #Loops until index is less than the length of reactant1
    if ord(reactant1[index]) >= 65 and ord(reactant1[index]) <= 90: #The letter is uppercase
        if len(tempElement) > 0: #Checks if the length of tempElement is greater than 0
            if tempElement in reactantElements.keys(): #Checks if tempElement is already a key
                reactantElements[tempElement] += moles #Change the value by moles
            else: #The element in tempElement is not a key in the dictionary
                reactantElements.update({tempElement : moles}) #Add the new pair onto the dictionary
        tempElement = "" #Reset the tempElement variable
        moles = 1 * coefficient1 #Reset the moles value
        tempElement += reactant1[index] #Add the letter to the tempElement string
        if index == len(reactant1) - 1: #Check if the index is the last index of the string
            if tempElement in reactantElements.keys(): #Checks if tempElement is already a key
                reactantElements[tempElement] += moles #Change the value by moles
            else: #The element in tempElement is not a key in the dictionary
                reactantElements.update({tempElement: moles}) #Add the new pair onto the dictionary
    elif ord(reactant1[index]) >= 97 and ord(reactant1[index]) <= 122: #The letter is lowercase
        tempElement += reactant1[index] #Add the letter to the tempElement string
        if index == len(reactant1) - 1: #Check if the index is the last index of the string
            if tempElement in reactantElements.keys(): #Checks if tempElement is already a key
                reactantElements[tempElement] += moles #Change the value by moles
            else: #The element in tempElement is not a key in the dictionary
                reactantElements.update({tempElement: moles}) #Add the new key and value pair onto the dictionary
    else: #The current element is a subscript number
        if index + 1 < len(reactant1) and reactant1[index + 1].isnumeric(): #Two-digit subscript number
            moles = (int(reactant1[index]) * 10 + int(reactant1[index + 1])) * coefficient1 #Calculate the moles
            index += 1 #Increment the index
        else: #One-digit subscript number
            moles = int(reactant1[index]) * coefficient1 #Multiply the subscript number with the coefficient
        if index == len(reactant1) - 1: #Check if the index is the last index of the string
            if tempElement in reactantElements.keys(): #Checks if tempElement is already a key
                reactantElements[tempElement] += moles #Change the value by moles
            else: #The element in tempElement is not a key in the dictionary
                reactantElements.update({tempElement: moles}) #Add the new pair onto the dictionary
    index += 1 #Increment the index value by 1

if numReactants == 2: #The code runs if numReactants is 2
    index = 0  # Initialize and reset the variable index
    tempElement = ""  # Initialize and reset the variable tempElement which stores the current element symbol
    if reactant2[0].isnumeric() == True and reactant2[1].isnumeric() == True: #Coefficient is a two-digit number
        coefficient2 = int(reactant2[0]) * 10 + int(reactant2[1]) #The integer becomes the coefficient
        index += 2  # Increment the index by 2
    elif reactant2[0].isnumeric() == True:  # Checks if the first element of the string is an integer
        coefficient2 = int(reactant2[0])  # The integer becomes the coefficient
        index += 1  # Increment the index value by 1
    else:  # The first element in the string is not an integer
        coefficient2 = 1  # Set the coefficient to 1
    moles = 1 * coefficient2  # Initialize the moles value based on the coefficient value

    while index < len(reactant2): #Loops until index is less than the length of reactant2
        if ord(reactant2[index]) >= 65 and ord(reactant2[index]) <= 90: #The letter is uppercase
            if len(tempElement) > 0: #Checks if the length of tempElement is greater than 0
                if tempElement in reactantElements.keys(): #Checks if tempElement is already a key
                    reactantElements[tempElement] += moles #Change the value by moles
                else: #The element in tempElement is not a key in the dictionary
                    reactantElements.update({tempElement: moles}) #Add the new pair onto the dictionary
            tempElement = "" #Reset the tempElement variable
            moles = 1 * coefficient2 #Reset the moles value
            tempElement += reactant2[index] #Add the letter to the tempElement string
            if index == len(reactant2) - 1: #Check if the index is the last index of the string
                if tempElement in reactantElements.keys(): #Checks if tempElement is already a key
                    reactantElements[tempElement] += moles #Change the value by moles
                else: #The element in tempElement is not a key in the dictionary
                    reactantElements.update({tempElement: moles}) #Add the new pair onto the dictionary
        elif ord(reactant2[index]) >= 97 and ord(reactant2[index]) <= 122: #The letter is lowercase
            tempElement += reactant2[index] #Add the letter to the tempElement string
            if index == len(reactant2) - 1: #Check if the index is the last index of the string
                if tempElement in reactantElements.keys(): #Checks if tempElement is already a key
                    reactantElements[tempElement] += moles #Change the value by moles
                else: #The element in tempElement is not a key in the dictionary
                    reactantElements.update({tempElement: moles}) #Add the new pair onto the dictionary
        else: #The current element is a subscript number
            if index + 1 < len(reactant2) and reactant2[index + 1].isnumeric(): #Two-digit subscript number
                moles = (int(reactant2[index]) * 10 + int(reactant2[index + 1])) * coefficient2 #Mole calculations
                index += 1 #Increment the index
            else: #One-digit subscript number
                moles = int(reactant2[index]) * coefficient2 #Multiply the subscript number with the coefficient
            if index == len(reactant2) - 1: #Check if the index is the last index of the string
                if tempElement in reactantElements.keys(): #Checks if tempElement is already a key
                    reactantElements[tempElement] += moles #Change the value by moles
                else: #The element in tempElement is not a key in the dictionary
                    reactantElements.update({tempElement: moles}) #Add the new pair onto the dictionary
        index += 1 #Increment the index value by 1
print(reactantElements)

index = 0 #Initialize the variable index
tempElement = "" #Initialize the variable tempElement which stores the current element symbol
if product1[0].isnumeric() == True and product1[1].isnumeric() == True: #Coefficient is a two-digit number
    coefficient3 = int(product1[0]) * 10 + int(product1[1]) #The integer becomes the coefficient
    index += 2  # Increment the index by 2
elif product1[0].isnumeric() == True: #Checks if the first element of the string is an integer
    coefficient3 = int(product1[0]) #The integer becomes the coefficient
    index += 1 #Increment the index value by 1
else: #The first element in the string is not an integer
    coefficient3 = 1 #Set the coefficient to 1
moles = 1 * coefficient3 #Initialize the moles value based on the coefficient value

while index < len(product1) and numProducts <= 2: #Loops until index is less than the length of product1
    if ord(product1[index]) >= 65 and ord(product1[index]) <= 90: #The letter is uppercase
        if len(tempElement) > 0: #Checks if the length of tempElement is greater than 0
            if tempElement in productElements.keys(): #Checks if tempElement is already a key
                productElements[tempElement] += moles #Change the value by moles
            else: #The element in tempElement is not a key in the dictionary
                productElements.update({tempElement : moles}) #Add the new key and value pair onto the dictionary
        tempElement = "" #Reset the tempElement variable
        moles = 1 * coefficient3 #Reset the moles value
        tempElement += product1[index] #Add the letter to the tempElement string
        if index == len(product1) - 1: #Check if the index is the last index of the string
            if tempElement in productElements.keys(): #Checks if tempElement is already a key
                productElements[tempElement] += moles #Change the value by moles
            else: #The element in tempElement is not a key in the dictionary
                productElements.update({tempElement: moles}) #Add the new key and value pair onto the dictionary
    elif ord(product1[index]) >= 97 and ord(product1[index]) <= 122: #The letter is lowercase
        tempElement += product1[index] #Add the letter to the tempElement string
        if index == len(product1) - 1: #Check if the index is the last index of the string
            if tempElement in productElements.keys(): #Checks if tempElement is already a key
                productElements[tempElement] += moles #Change the value by moles
            else: #The element in tempElement is not a key in the dictionary
                productElements.update({tempElement: moles}) #Add the new key and value pair onto the dictionary
    else: #The current element is a subscript number
        if index + 1 < len(product1) and product1[index + 1].isnumeric(): #Two-digit subscript number
            moles = (int(product1[index]) * 10 + int(product1[index + 1])) * coefficient3 #Mole calculation
            index += 1 #Increament the index
        else: #A one-digit subscript number
            moles = int(product1[index]) * coefficient3 #Multiply the subscript number with the coefficient
        if index == len(product1) - 1: #Check if the index is the last index of the string
            if tempElement in productElements.keys(): #Checks if tempElement is already a key
                productElements[tempElement] += moles #Change the value by moles
            else: #The element in tempElement is not a key in the dictionary
                productElements.update({tempElement: moles}) #Add the new key and value pair onto the dictionary
    index += 1 #Increment the index value by 1

if numProducts == 2: #The code runs if numProducts is 2
    index = 0  # Initialize and reset the variable index
    tempElement = ""  # Initialize and reset the variable tempElement which stores the current element symbol
    if product2[0].isnumeric() == True and product2[1].isnumeric() == True: #Coefficient is a two-digit number
        coefficient4 = int(product2[0]) * 10 + int(product2[1]) #The integer becomes the coefficient
        index += 2  # Increment the index by 2
    elif product2[0].isnumeric() == True:  # Checks if the first element of the string is an integer
        coefficient4 = int(product2[0])  # The integer becomes the coefficient
        index += 1  # Increment the index value by 1
    else:  # The first element in the string is not an integer
        coefficient4 = 1  # Set the coefficient to 1
    moles = 1 * coefficient4  # Initialize the moles value based on the coefficient value

    while index < len(product2): #Loops until index is less than the length of product2
        if ord(product2[index]) >= 65 and ord(product2[index]) <= 90: #The letter is uppercase
            if len(tempElement) > 0: #Checks if the length of tempElement is greater than 0
                if tempElement in productElements.keys(): #Checks if tempElement is already a key
                    productElements[tempElement] += moles #Change the value by moles
                else: #The element in tempElement is not a key in the dictionary
                    productElements.update({tempElement: moles}) #Add the new pair onto the dictionary
            tempElement = "" #Reset the tempElement variable
            moles = 1 * coefficient4 #Reset the moles value
            tempElement += product2[index] #Add the letter to the tempElement string
            if index == len(product2) - 1: #Check if the index is the last index of the string
                if tempElement in productElements.keys(): #Checks if tempElement is already a key
                    productElements[tempElement] += moles #Change the value by moles
                else: #The element in tempElement is not a key in the dictionary
                    productElements.update({tempElement: moles}) #Add the new pair onto the dictionary
        elif ord(product2[index]) >= 97 and ord(product2[index]) <= 122: #The letter is lowercase
            tempElement += product2[index] #Add the letter to the tempElement string
            if index == len(product2) - 1: #Check if the index is the last index of the string
                if tempElement in productElements.keys(): #Checks if tempElement is already a key
                    productElements[tempElement] += moles #Change the value by moles
                else: #The element in tempElement is not a key in the dictionary
                    productElements.update({tempElement: moles}) #Add the new pair onto the dictionary
        else: #The current element is a subscript number
            if index + 1 < len(product2) and product2[index + 1].isnumeric(): #A two-digit subscript number
                moles = (int(product2[index]) * 10 + int(product2[index + 1])) * coefficient4 #Calculate the mole
                index += 1 #Increment the index
            else: #A one-digit subscript number
                moles = int(product2[index]) * coefficient4 #Multiply the subscript number with the coefficient
            if index == len(product2) - 1: #Check if the index is the last index of the string
                if tempElement in productElements.keys(): #Checks if tempElement is already a key
                    productElements[tempElement] += moles #Change the value by moles
                else: #The element in tempElement is not a key in the dictionary
                    productElements.update({tempElement: moles}) #Add the new pair onto the dictionary
        index += 1 #Increment the index value by 1
print(productElements)
"""
#Need help on line 170 to line 194
needCoefficientReactants = {}
needCoefficientProducts = {}
for key, value in reactantElements.items():
    if value == productElements.get(key):
        numBalanced += 1
    else:
        if value > productElements.get(key):
            greater = value
        else:
            greater = productElements.get(key)
        while True:
            if greater % value == 0 and greater % productElements.get(key) == 0:
                lcm = greater
                break
            greater += 1
        multiplier1 = int(lcm / value)
        needCoefficientReactants.update({key : multiplier1})
        multiplier2 = int(lcm / productElements.get(key))
        needCoefficientProducts.update({key : multiplier2})

print(needCoefficientReactants)
print(needCoefficientProducts)
"""
"""
        while value != productElements.get(key):
            multiplier1 = 2
            while value < productElements.get(key):
                value *= multiplier1
                multiplier1 += 1
            multiplier2 = 2
            while productElements.get(key) < value:
                productElements[key] *= multiplier2
                multiplier2 += 1
"""

numBalanced = 0
for key, value in reactantElements.items():
    if value == productElements.get(key):
        numBalanced += 1

if numBalanced == len(reactantElements): #If the number of balanced elements are the same value as the length
    balanced = True #Balanced variable becomes true
else: #The chemical equation is not balanced
    balanced = False #Balanced variable becomes false

if balanced == True: #Runs when the chemical equation is already balanced
    print("Your chemical equation is already balanced!") #Print the statement
    if numReactants == 1 and numProducts == 2: #Runs when numReactants is 1 and numProducts is 2
        print(reactant1 + " -> " + product1 + " + " + product2) #Print the statement
    elif numReactants == 2 and numProducts == 1: #Runs when numReactants is 2 and numProducts is 1
        print(reactant1 + " + " + reactant2 + " -> " + product1) #Print the statement
    elif numReactants == 1 and numProducts == 1: #Runs when numReactants is 1 and numProducts is 1
        print(reactant1 + " -> " + product1) #Print the statement
    else: #Runs when numReactants is 2 and numProducts is 2
        print(reactant1 + " + " + reactant2 + " -> " + product1 + " + " + product2) #Print the statement

