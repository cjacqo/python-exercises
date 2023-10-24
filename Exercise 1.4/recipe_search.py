import pickle

def display_recipe(recipe):
  print('Recipe:', recipe['name'])
  print('Cooking Time (mins):', recipe['cooking_time'])
  print('Ingredients:')
  for el in recipe['ingredients']:
    print('- ', el)
  print('Difficulty:', recipe['difficulty'])
  print('\n')

def search_ingredients(data):
  all_ingredients = enumerate(data['all_ingredients'])
  numbered_list = list(all_ingredients)
  print('List of Ingredients: ')

  for el in numbered_list:
    print(el[0], el[1])
  
  try:
    num = int(input('Enter the number of the ingredients you would like to search for: '))
    ingredient_searched = numbered_list[num][1]
    print('Searching for recipes with', ingredient_searched, '...')
  except ValueError:
    print('Only numbers are allowed')
  except:
    print("Oops! Your input doesn't match any ingredients.")
  else:
    for el in data['recipes_list']:
      if ingredient_searched in el['ingredients']:
        print(el)

filename = input('Enter the name of the file you want to save to: ')

try:
  file = open(filename, 'rb')
  data = pickle.load(file)
  print('File loaded successfully!')
except FileNotFoundError:
  print('No files match that name - please try again')
except:
  print('Oops! There was an error.')
else:
  file.close()
  search_ingredients(data)