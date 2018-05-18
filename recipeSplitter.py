import os
import string

def capString(s):
    words = s.split()
    returnStr = ""
    for word in words:
        word = word.capitalize()
        returnStr += word + " "
    return returnStr[:-1]

def checkRecipe(sectionTitle, title, author, ingredients, directions, favorite, secondEdition):
    print()
    print(capString(sectionTitle))
    print("Title: " + title)
    print("Author: " + author)
    print(ingredients)
    print(directions)
    print("Second Edition: " + repr(secondEdition))
    print("Favorite: " + repr(favorite))
    print("Is this a good recipe?")
    resp = input()
    if resp == 'y' or resp == 'Y':
        sectionTitle = sectionTitle.translate(sectionTitle.maketrans('', '', string.punctuation))        
        newTitle = title.translate(title.maketrans('', '', string.punctuation))
        toFile = open("recipes/" + sectionTitle.replace(' ', '') + "/" + newTitle.replace(' ', ''), 'w')
        toFile.write('# ' + title + '\n')
        toFile.write('a:' + author + '\n\n')
        for ins in ingredients:
            toFile.write("* " + ins + "\n")
        toFile.write('\n')
        for d in directions: 
            toFile.write("> " + d + "\n")

def makeSection(sectionTitle):
    print('Is this a new section? (y/n)')
    print('Section Title: ' + sectionTitle)
    resp = input()
    if resp == 'y' or resp == 'Y':
        sectionTitle = sectionTitle.translate(sectionTitle.maketrans('', '', string.punctuation))
        if not os.path.exists('recipes/' + sectionTitle.replace(' ', '')):
            os.makedirs('recipes/' + sectionTitle.replace(' ', ''))

if __name__ == "__main__":
    print('Hello, world')

    book = open("book.txt", "r")
    # title = "Title: "
    # author = "Author: "
    # sectionTitle = "Section: "
    # directions = "Directions: " 
    # ingredients = []
    title = ""
    author = ""
    sectionTitle = ""
    directions = []
    ingredients = []
    favorite = False
    secondEdition = False

    for i in  range (0, 60):
        currentLine = book.readline()
        if currentLine[0] == '#':
            checkRecipe(sectionTitle, title, author, ingredients, directions, favorite, secondEdition)
            title = ""
            author = ""
            ingredients = []
            directions = []
            secondEdition = False
            favorite = False
            title += capString(currentLine.strip()[2:])
            if title[-2:] == '+':
                secondEdition = True
            elif title[-1:] == '+':
                favorite = True
        elif currentLine[0] == 'a' and currentLine[1] == ':':
            author += currentLine.strip()[3:]
        elif currentLine[0] == '*':
            ingredients.append(currentLine.strip()[2:])
        elif currentLine[0] == '>':
            directions. append(currentLine.strip()[2:])
        elif currentLine[0] != '*' and currentLine[0] != '>' and len(currentLine) > 3:
            currentLine = capString(currentLine.strip())
            makeSection(currentLine)
            sectionTitle = "" 
            sectionTitle += currentLine
    
 