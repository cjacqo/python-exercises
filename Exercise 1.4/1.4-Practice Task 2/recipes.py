import pickle

recipes = dict()

def insert_recipe(name, cooking_time, ingredients):
  num_ingredients = len(ingredients)
  difficulty = None
  if (cooking_time < 10 and num_ingredients < 4):
    difficulty = 'Easy'
  elif (cooking_time < 10 and num_ingredients >= 4):
    difficulty = 'Medium'
  elif (cooking_time >= 10 and num_ingredients < 4):
    difficulty = 'Intermediate'
  elif (cooking_time >= 10 and num_ingredients >= 4):
    difficulty = 'Hard'
  
  recipes[name] = {
    'name': name,
    'cooking_time': cooking_time,
    'ingredients': ingredients,
    'difficulty': difficulty 
  }

insert_recipe('tea', 5, ['tea leaves', 'water', 'sugar'])

my_file = open('recipe_binary.bin', 'wb')
pickle.dump(recipes['tea'], my_file)
my_file.close()

with open('recipe_binary.bin', 'rb') as my_file:
  recipe = pickle.load(my_file)
  name = recipe['name']
  cooking_time = str(recipe['cooking_time'])
  ingredients = recipe['ingredients']
  difficulty = recipe['difficulty']
  print('Recipe details - ')
  print('Name:', name)
  print('Cooking Time:', cooking_time)
  print('Ingredients:', *ingredients, sep = '\n')
  print('Difficulty:', difficulty)