"""
Notify the user if their equation is balanced or not and then utilized the balanced equation for stoichiometry.
Author: Johan Nino Espino
Creation Date: 11/29/2022
"""

numReactants = int(input("Enter the number of reactants (Enter 1 or 2): ")) #Ask the number of reactants
numProducts = int(input("Enter the number of products (Enter 1 or 2): ")) #Ask the number of products

while numReactants != 1 and numReactants != 2: #Loops when numReactants is not 1 and 2
    numReactants = int(input("Enter the number of reactants (Enter 1 or 2): "))
while numProducts != 1 and numProducts != 2: #Loops when numProducts is not 1 and 2
    numProducts = int(input("Enter the number of products (Enter 1 or 2): "))

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
if reactant1[0].isnumeric() == True: #Checks if the first element of the string is an integer
    coefficient = int(reactant1[0]) #The integer becomes the coefficient
    index += 1 #Increment the index value by 1
else: #The first element in the string is not an integer
    coefficient = 1 #Set the coefficient to 1
moles = 1 * coefficient #Initialize the moles value based on the coefficient value

while index < len(reactant1) and numReactants <= 2: #Loops until index is less than the length of reactant1
    if ord(reactant1[index]) >= 65 and ord(reactant1[index]) <= 90: #The letter is uppercase
        if len(tempElement) > 0: #Checks if the length of tempElement is greater than 0
            reactantElements.update({tempElement : moles}) #Add the new key and value pair onto the dictionary
        tempElement = "" #Reset the tempElement variable
        moles = 1 * coefficient #Reset the moles value
        tempElement += reactant1[index] #Add the letter to the tempElement string
        if index == len(reactant1) - 1: #Check if the index is the last index of the string
            reactantElements.update({tempElement: moles}) #Add the new key and value pair onto the dictionary
    elif ord(reactant1[index]) >= 97 and ord(reactant1[index]) <= 122: #The letter is lowercase
        tempElement += reactant1[index] #Add the letter to the tempElement string
        if index == len(reactant1) - 1: #Check if the index is the last index of the string
            reactantElements.update({tempElement: moles}) #Add the new key and value pair onto the dictionary
    else: #The current element is a subscript number
        moles = int(reactant1[index]) * coefficient #Multiply the subscript number with the coefficient
        if index == len(reactant1) - 1: #Check if the index is the last index of the string
            reactantElements.update({tempElement: moles}) #Add the new key and value pair onto the dictionary
    index += 1 #Increment the index value by 1

if numReactants == 2: #The code runs if numReactants is 2
    index = 0  # Initialize and reset the variable index
    tempElement = ""  # Initialize and reset the variable tempElement which stores the current element symbol
    if reactant2[0].isnumeric() == True:  # Checks if the first element of the string is an integer
        coefficient = int(reactant2[0])  # The integer becomes the coefficient
        index += 1  # Increment the index value by 1
    else:  # The first element in the string is not an integer
        coefficient = 1  # Set the coefficient to 1
    moles = 1 * coefficient  # Initialize the moles value based on the coefficient value

    while index < len(reactant2): #Loops until index is less than the length of reactant2
        if ord(reactant2[index]) >= 65 and ord(reactant2[index]) <= 90: #The letter is uppercase
            if len(tempElement) > 0: #Checks if the length of tempElement is greater than 0
                if tempElement in reactantElements.keys(): #Checks if tempElement is already a key
                    reactantElements[tempElement] += moles #Change the value by moles
                else: #The element in tempElement is not a key in the dictionary
                    reactantElements.update({tempElement: moles}) #Add the new pair onto the dictionary
            tempElement = "" #Reset the tempElement variable
            moles = 1 * coefficient #Reset the moles value
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
            moles = int(reactant2[index]) * coefficient #Multiply the subscript number with the coefficient
            if index == len(reactant2) - 1: #Check if the index is the last index of the string
                if tempElement in reactantElements.keys(): #Checks if tempElement is already a key
                    reactantElements[tempElement] += moles #Change the value by moles
                else: #The element in tempElement is not a key in the dictionary
                    reactantElements.update({tempElement: moles}) #Add the new pair onto the dictionary
        index += 1 #Increment the index value by 1
print(reactantElements)

index = 0 #Initialize the variable index
tempElement = "" #Initialize the variable tempElement which stores the current element symbol
if product1[0].isnumeric() == True: #Checks if the first element of the string is an integer
    coefficient = int(product1[0]) #The integer becomes the coefficient
    index += 1 #Increment the index value by 1
else: #The first element in the string is not an integer
    coefficient = 1 #Set the coefficient to 1
moles = 1 * coefficient #Initialize the moles value based on the coefficient value

while index < len(product1) and numProducts <= 2: #Loops until index is less than the length of product1
    if ord(product1[index]) >= 65 and ord(product1[index]) <= 90: #The letter is uppercase
        if len(tempElement) > 0: #Checks if the length of tempElement is greater than 0
            productElements.update({tempElement : moles}) #Add the new key and value pair onto the dictionary
        tempElement = "" #Reset the tempElement variable
        moles = 1 * coefficient #Reset the moles value
        tempElement += product1[index] #Add the letter to the tempElement string
        if index == len(product1) - 1: #Check if the index is the last index of the string
            productElements.update({tempElement: moles}) #Add the new key and value pair onto the dictionary
    elif ord(product1[index]) >= 97 and ord(product1[index]) <= 122: #The letter is lowercase
        tempElement += product1[index] #Add the letter to the tempElement string
        if index == len(product1) - 1: #Check if the index is the last index of the string
            productElements.update({tempElement: moles}) #Add the new key and value pair onto the dictionary
    else: #The current element is a subscript number
        moles = int(product1[index]) * coefficient #Multiply the subscript number with the coefficient
        if index == len(product1) - 1: #Check if the index is the last index of the string
            productElements.update({tempElement: moles}) #Add the new key and value pair onto the dictionary
    index += 1 #Increment the index value by 1

if numProducts == 2: #The code runs if numProducts is 2
    index = 0  # Initialize and reset the variable index
    tempElement = ""  # Initialize and reset the variable tempElement which stores the current element symbol
    if product2[0].isnumeric() == True:  # Checks if the first element of the string is an integer
        coefficient = int(product2[0])  # The integer becomes the coefficient
        index += 1  # Increment the index value by 1
    else:  # The first element in the string is not an integer
        coefficient = 1  # Set the coefficient to 1
    moles = 1 * coefficient  # Initialize the moles value based on the coefficient value

    while index < len(product2): #Loops until index is less than the length of product2
        if ord(product2[index]) >= 65 and ord(product2[index]) <= 90: #The letter is uppercase
            if len(tempElement) > 0: #Checks if the length of tempElement is greater than 0
                if tempElement in productElements.keys(): #Checks if tempElement is already a key
                    productElements[tempElement] += moles #Change the value by moles
                else: #The element in tempElement is not a key in the dictionary
                    productElements.update({tempElement: moles}) #Add the new pair onto the dictionary
            tempElement = "" #Reset the tempElement variable
            moles = 1 * coefficient #Reset the moles value
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
            moles = int(product2[index]) * coefficient #Multiply the subscript number with the coefficient
            if index == len(product2) - 1: #Check if the index is the last index of the string
                if tempElement in productElements.keys(): #Checks if tempElement is already a key
                    productElements[tempElement] += moles #Change the value by moles
                else: #The element in tempElement is not a key in the dictionary
                    productElements.update({tempElement: moles}) #Add the new pair onto the dictionary
        index += 1 #Increment the index value by 1
print(productElements)
#Need help on line 170 to line 194
needCoefficientReactants = {}
needCoefficientProducts = {}
numBalanced = 0
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


