import psycopg2
import os

def buildRecipe(recipeFile, sectionDir, section):
    readFile = open("recipes/" + sectionDir + "/" + recipeFile)
    recipe = {}
    ingredients = []
    directions = []
    recipe['section'] = section
    recipe['favorite'] = False
    recipe['second_ed'] = False
    for line in readFile:
        if line[0] == '#':
            recipe['title'] = line.strip()[2:]
        elif line[0] == '*':
            ingredients.append(line.strip()[2:])
        elif line[0] == '>':
            directions.append(line.strip()[2:])
        elif line[0] == 'a' and line[1] == ':':
            recipe['author'] = line.strip()[2:]
        elif line[0] == '+':
            recipe['favorite'] = True
        elif line[0] == '@':
            recipe['second_ed'] = True
    recipe['directions'] = directions
    recipe['ingredients'] = ingredients
    return recipe

if __name__ == "__main__":
    print("Hello, World");

    sections = {
        "AppetizersDipsDressingsAndSpreads" : "Appetizers, Dips, Dressings, and Spreads",
        "BreadsRollsAndGriddleCakes" : "Breads, Rolls, and Griddle Cakes",
        "CakesFillingsAndFrostings" : "Cakes, Fillings, and Frostings",
        "Candy" : "Candy",
        "CanningAndPreserving" : "Canning And Preserving",
        "Cookies" : "Cookies",
        "CreativeChildrensRecipes" : "Creative Childrens Recipes",
        "Drinks" : "Drinks",
        "FishAndSeafood" : "Fish and Seafood",
        "IceCreamPuddingsAndDesserts" : "Ice Creams, Puddings, and Desserts",
        "MeatDishesAndCasseroles" : "Meat Dishes and Casseroles",
        "PiesAndDoughnuts" : "Pies and Doughnuts",
        "PoultryAndEggDishes" : "Poultry and Egg Dishes",
        "Salads" : "Salads",
        "SoupAndVegetables" : "Soup and Vegetables"
    }


    conn = psycopg2.connect("dbname=rodgersfamily user=postgres password=postgres")
    
    cur = conn.cursor()
    for sectionDir in (os.listdir('recipes')):
        for recipeFile in os.listdir("recipes/" + sectionDir):
            recipe = buildRecipe(recipeFile, sectionDir, sections[sectionDir])
            cur.execute("INSERT INTO recipes (title, author, favorite, second_ed, section) VALUES (%s, %s, %s, %s, %s);", (recipe["title"], recipe["author"], recipe["favorite"], recipe["second_ed"], recipe["section"]))
            print(recipe['title'])
            cur.execute("SELECT recipe_id FROM recipes WHERE title = %s", (recipe['title'],))
            recipe_id = cur.fetchone()

            for ingredient in recipe['ingredients']:
                cur.execute("INSERT INTO recipe_ingredients (recipe, ingredient) values (%s, %s);", (recipe_id, ingredient))

            for index, direction in enumerate(recipe['directions']):
                cur.execute("INSERT INTO recipe_instructions (recipe, instruction, step_no) values (%s, %s, %s);", (recipe_id, direction, index))
    conn.commit()
    cur.close()
    conn.close()
