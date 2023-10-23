recipes_list = dict()
ingredients_list = []

def take_recipe():
  # Ask the name of the recipe
  name = input('Name of recipe: ')
  # Ask the cooking time of the recipe
  cooking_time = int(input('Cooking time in minutes: '))
  # Ask the ingredients of the recipe
  ingredients = [str(ingredients) for ingredients in input('Enter the ingredients: ').split(' ')]
  # Return the recipe as an object
  return {
    "name": name,
    "cooking_time": cooking_time,
    "ingredients": ingredients
  }

def insert_recipe(recipe):
  # Inserting recipe with key as name of recipe
  recipes_list[str(recipe['name'])] = {
    "name": recipe['name'],
    "cooking_time": recipe['cooking_time'],
    "ingredients": recipe['ingredients']
  }
  # Alert to user that the recipe has been inserted
  print('Recipe has been inserted\n')

def print_recipes():
  # Loop over each recipe to print
  for key, value in recipes_list.items():
    name = key.capitalize()
    cooking_time = value['cooking_time']
    ingredients = value['ingredients']
    num_ingredients = len(ingredients)
    difficulty = determine_difficulty(cooking_time, num_ingredients)

    print('Recipe:', name)
    print('Cooking Time (min):', cooking_time)
    print('Ingredients:', *ingredients, sep = '\n')
    print('Difficulty:', difficulty)
    print('\n')

def determine_difficulty(cooking_time, num_ingredients):
  if (cooking_time < 10 and num_ingredients < 4):
    return 'Easy'
  elif (cooking_time < 10 and num_ingredients >= 4):
    return 'Medium'
  elif (cooking_time >= 10 and num_ingredients < 4):
    return 'Intermediate'
  elif (cooking_time >= 10 and num_ingredients >= 4):
    return 'Hard'

def print_ingredients():
  print('Ingredients Available Across All Recipes')
  print('----------------------------------------')
  ingredients_list.sort()
  for i in range(0, len(ingredients_list), 1):
    print(ingredients_list[i])

# Main section of code: ask how many recipes the user would like to enter
num_recipes = int(input('How many recipes would you like to enter? '))

# Create recipes in a loop based on how many recipes user wants to input
for i in range(0, num_recipes, 1):
  # Set the recipe object to a variable
  recipe = take_recipe()
  # For loop to insert ingredients into global ingredients_list
  for i in range(0, len(recipe['ingredients']), 1):
    ingredient = recipe['ingredients'][i]
    if (ingredient not in ingredients_list):
      ingredients_list.append(ingredient)
  # Insert recipe into dictionary
  insert_recipe(recipe)

# Call function to print recipes
print_recipes()

# Call function to print all ingredients
print_ingredients()