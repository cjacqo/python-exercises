import pickle

def take_recipe():
  # Ask the name of the recipe
  name = input('Name of recipe: ')
  # Ask the cooking time of the recipe
  cooking_time = int(input('Cooking time in minutes: '))
  # Ask the ingredients of the recipe
  ingredients = [str(ingredients) for ingredients in input('Enter the ingredients (separate with commas): ').split(',')]
  # Get the difficulty
  difficulty = calc_difficulty(cooking_time, ingredients)
  # Return the recipe as an object
  return {
    'name': name,
    'cooking_time': cooking_time,
    'ingredients': ingredients
  }

def calc_difficulty(cooking_time, ingredients):
  num_ingredients = len(ingredients)
  if (cooking_time < 10 and num_ingredients < 4):
    return 'Easy'
  elif (cooking_time < 10 and num_ingredients >= 4):
    return 'Medium'
  elif (cooking_time >= 10 and num_ingredients < 4):
    return 'Intermediate'
  elif (cooking_time >= 10 and num_ingredients >= 4):
    return 'Hard'

def create_dict():
  return { 'recipes_list': [], 'all_ingredients': [] }

# Main Code
filename = input("Enter the filename where you've stored your recipes: ")
try:
  file = open(filename, 'wb')
  data = pickle.load(file)
  print('File loaded successfully!')
except FileNotFoundError:
  print('File does not exist - exiting')
  data = create_dict()
except:
  print('Oops! Something wen wrong. Try again.')
  data = create_dict()
else:
  file.close()
finally:
  recipes_list = data['recipes_list']
  all_ingredients = data['all_ingredients']

# Ask user how many recipes they want to create
num_recipes = int(input('How many recipes would you like to create? '))

for i in range(0, num_recipes):
  recipe = take_recipe()
  for el in recipe['ingredients']:
    if el not in all_ingredients:
      all_ingredients.append(el)
  recipes_list.append(recipe)
  print('Recipe added')

# Create new dictionary with updated data
data = { 'recipes_list': recipes_list, 'all_ingredients': all_ingredients }

# Open file and save data to it
recipes_file = open(filename, 'wb')
pickle.dump(data, recipes_file)

# Close the file
recipes_file.close()
print('Recipes file has been updated!')