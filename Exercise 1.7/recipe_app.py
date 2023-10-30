import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Load dot env
load_dotenv()

# Load environment variables
db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASS")
db_name = os.environ.get("DB_NAME")

# Connect SQLAlchemy with Database by creating engine
engine = create_engine(f"mysql://{db_user}:{db_pass}@localhost/{db_name}")

# Initiate Session for Database
Session = sessionmaker(bind=engine)
session = Session()

# Creating a Table from a Mapped Class
Base = declarative_base()

# Declare Class for Database Table
class Recipe(Base):
  __tablename__ = "recipes"

  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(50))
  ingredients = Column(String(255))
  cooking_time = Column(Integer)
  difficulty = Column(String(20))

  def __repr__(self):
    return "<Recipe ID: " + str(self.id) + "-" + self.name + ": " + self.difficulty + ">"
  
  def __str__(self):
    return f"Recipe: {self.name}\nCooking Time (mins): {self.cooking_time}\nIngredients: {self.ingredients}\nDifficulty: {self.difficulty}\n"

  def calculate_difficulty(self):
    num_ingredients = len(self.return_ingredients_as_list())
    if (self.cooking_time < 10 and num_ingredients < 4):
      self.difficulty = 'Easy'
    elif (self.cooking_time < 10 and num_ingredients >= 4):
      self.difficulty = 'Medium'
    elif (self.cooking_time >= 10 and num_ingredients < 4):
      self.difficulty = 'Intermediate'
    elif (self.cooking_time >= 10 and num_ingredients >= 4):
      self.difficulty = 'Hard'
  
  def return_ingredients_as_list(self):
    if len(self.ingredients) == 0:
      return []
    else:
      return self.ingredients.split(', ')
  
# Create Table in Database
Base.metadata.create_all(engine)

# Helper functions
## Create choice creates a string with a number for the main menu choices
def create_choice(num, string):
  return f"\t\t{str(num)}. {string}"

## Check if there are recipes in the database
def db_has_recipes():
  num_recipes = session.query(Recipe).count()
  if num_recipes == 0:
    print("There are no recipes. Make one yourself!")
  return num_recipes != 0

## Commit changes
def commit_changes(str):
  session.commit()
  print(f'\nRecipe {str} successfully!')

# Main Operations
## Create a Recipe
def create_recipe():
  # Empty variables for recipe details
  name = ''
  cooking_time = ''

  # Ask for name of recipe
  while True:
    try:
      name = str(input("\nName of the recipe: "))
    except ValueError:
      print("Sorry, I didn't understand that.")
      continue
    if len(name) > 50 or len(name) == 0:
      print("Sorry, your response must be greater than 0 and less than 50 characters")
    else:
      break

  # Ask for cooking time of recipe
  while True:
    try:
      cooking_time = input("\nCooking time (minutes): ")
    except ValueError:
      print("Sorry, I didn't understand that.")
    if cooking_time == '0':
      print("Sorry, the cooking time of a recipe cannot be 0 minutes.")
    elif cooking_time.isalpha():
      print("Sorry, the cooking time must be a number")
    elif int(cooking_time) > 0:
      cooking_time = int(cooking_time)
      break
  
  # Ask for ingredients of recipe
  ingredients = [str(ingredients) for ingredients in input('\nEnter the ingredients (separate with comma and space): ').split(', ')]

  # Convert the ingredients list into a comma separated string
  ingredients_str = ', '.join(ingredients)

  # Add entry into table
  # # Create an entry to the recipe table
  recipe_entry = Recipe(
    name = name,
    cooking_time = cooking_time,
    ingredients = ingredients_str
  )
  # # Call calculate_difficulty method
  recipe_entry.calculate_difficulty()
  # # Insert entry into table
  session.add(recipe_entry)
  session.commit('created')

## Search for a Recipe
def search_recipe():
  # Get a count of all entries: if count is 0, return
  if not db_has_recipes():
    print("There are no recipes. Make one yourself!")
    return None
  
  # Get all ingredients from all recipes into a list
  ingredients_res = session.query(Recipe.ingredients).all()

  # Initialize an empty list for ingredients
  all_ingredients = []

  # Loop ingredients_res to insert ingredients into all_ingredients without duplicates
  for ingredient in ingredients_res:
    temp = ingredient[0].split(', ')
    for ing in temp:
      if ing not in all_ingredients:
        all_ingredients.append(ing)
  
  # Index each ingredient in the list
  ingredients_list = list(enumerate(all_ingredients))

  # Print indexed ingredients list
  print("\nAll Ingredients\n" + 20*'-')
  for index, tup in enumerate(ingredients_list):
    print(str(tup[0]+1) + ". " + tup[1])

  # Initialize an empty options list
  options = []

  # Insert options with numbers from ingredients list
  for item in ingredients_list:
    num = item[0]
    options.append(num)
  
  # Ask user for ingredients they want to search
  search_for = input("\nEnter the number for the ingredient you want to search (separated with comma and space): ").split(', ')

  # Initialize empty search list
  searched_ingredients = []

  # Loop search_for to validate user inputs
  for i in search_for:
    ## Check if input is valid
    if not i.isnumeric() or int(i) not in options:
      print('\n\tError: Value is not a number and does not match any ingredients in list')
      print('\n\tPlease try again')
      return None
    else:
      i = int(i)
      searched_ingredients.append(ingredients_list[i -1][1])

  # Condition list
  condition_list = []

  # Loop searched_ingredients to fill condition_list
  for ingredient in searched_ingredients:
    ## Create like term and search to append to condition_list
    condition_list.append(Recipe.ingredients.like(str(f"%{ingredient}%")))
  
  # Using the condition_list, find all recipes that include the ingredients selected
  matched_recipes = session.query(Recipe).filter(*condition_list).all()

  # Let user know if there are or are not matches
  if len(matched_recipes) == 0:
    print("\nNo recipes were found based on your search.")
    return None
  else:
    print("\nFound Recipes Matching Your Search\n" + 20*'-')
    for recipe in matched_recipes:
      print(recipe)

## Edit Recipe
def edit_recipe():
  # Check if database has recipes
  if not db_has_recipes():
    return None
  
  # Helper function to print string for what is being edited
  def print_editing_str(edit_column, recipe):
    print(f"\nUpdating {edit_column} of {recipe.name}\n" + 20*'-')

  # Helper function to print error and return to main main
  def handle_error(e):
    print('\nUh-oh! Something went wrong.')
    print(e)
    print('Back to main menu.')
    return None
  
  # Get all recipes from the database
  recipes_results = session.query(Recipe.id, Recipe.name).all()

  # Create a list of options for user to select from
  options = []
  print('\nAll Recipes:\n' + 20*'-')
  for recipe in recipes_results:
    print(f"\n\tID: {recipe[0]} - {recipe[1]}")
    options.append(recipe[0])

  # Ask user what recipe they want to edit
  recipe_selected = input('\nSelect the recipe you would like to edit: ')
  # Verify the input is a number
  while not recipe_selected.isnumeric():
    print('\n\tError: The value must be a number')
    recipe_selected = input('\nSelect the recipe you would like to edit: ')
  
  # Change the input to an integer
  recipe_selected = int(recipe_selected)

  # Verify that the input is a valid id of a recipe
  if recipe_selected not in options:
    print('\n\tThe number you selected does not exist. Back to main menu.')
    return
  
  # Find the recipe to be edited
  recipe_to_edit = session.query(Recipe).filter(Recipe.id == recipe_selected).one()

  # Print the details of the recipe
  print('\nRecipe Selected to Edit:\n' + 20*'-')
  print(f'\n\t1.  Name: {recipe_to_edit.name}')
  print(f'\n\t2.  Cooking Time: {recipe_to_edit.cooking_time}')
  print(f'\n\t3.  Ingredients: {recipe_to_edit.ingredients}')
  print()

  # Create list of options to edit values
  edit_options = [1, 2, 3]

  # Ask user to select what they want to edit
  value_to_edit = input('\nEnter the number for the value you want to edit: ')

  # Verify the input is a number
  while not value_to_edit.isnumeric():
    print('\nError: The value must be a number')
    value_to_edit = input('\nEnter the number for the value you want to edit: ')
  
  # Change the input to an integer
  value_to_edit = int(value_to_edit)

  # Verify the value to edit exists
  if value_to_edit not in edit_options:
    print('\nYour input is not a valid option. Please try again. Back to main menu.')
    return
  
  # If editing name
  if value_to_edit == 1:
    print_editing_str('name', recipe_to_edit)
    
    # Ask for new name
    new_name = str(input('\nEnter the new name: ')).title()

    # Validate the input
    while len(new_name) > 50 or len(new_name) == 0:
      print('\nError: Name must be greater than length of 0 and less than length of 50')
      new_name = str(input('\nEnter the new name: ')).title()
    try:
      session.query(Recipe).filter(Recipe.id == recipe_selected).update({ Recipe.name: new_name })
      commit_changes()
      return
    except Exception as e:
      handle_error(e)
      return
  # If editing cooking time
  elif value_to_edit == 2:
    print_editing_str('cooking time', recipe_to_edit)

    # Ask for new time
    new_time = input('\nEnter the new cooking time (in minutes): ')

    # Validate the input
    while not new_time.isnumeric():
      print('\nError: Cooking time must be a number')
      new_time = input('\nEnter the new cooking time (in minutes): ')
    # Convert new_time to integer
    new_time = int(new_time)
    try:
      # Create temp new recipe
      temp_recipe = Recipe(
        name = recipe_to_edit.name,
        cooking_time = new_time,
        ingredients = recipe_to_edit.ingredients
      )

      # Calculate difficulty
      temp_recipe.calculate_difficulty()

      # Update the cooking time and difficulty
      session.query(Recipe).filter(Recipe.id == recipe_selected).update(
        {
          Recipe.cooking_time: new_time,
          Recipe.difficulty: temp_recipe.difficulty
        }
      )
      commit_changes('updated')
      return
    except Exception as e:
      handle_error(e)
      return
  # If editing ingredients
  else:
    print_editing_str('ingredients', recipe_to_edit)

    # Initialize empty list for ingredients
    # Ask for ingredients of recipe
    new_ingredients = [str(ingredients) for ingredients in input('\nEnter the ingredients (separate with comma and space): ').split(', ')]

    # Convert the ingredients list into a comma separated string
    ingredients_str = ', '.join(new_ingredients)

    try:
      temp_recipe = Recipe(
        name = recipe_to_edit.name,
        cooking_time = recipe_to_edit.cooking_time,
        ingredients = ingredients_str
      )

      # Calculate difficulty
      temp_recipe.calculate_difficulty()

      # Update ingredients and difficulty
      session.query(Recipe).filter(Recipe.id == recipe_selected).update(
        {
          Recipe.ingredients: ingredients_str,
          Recipe.difficulty: temp_recipe.difficulty
        }
      )

      commit_changes()
    except Exception as e:
      handle_error(e)
      return
    
## Delete Recipe
def delete_recipe():
  if not db_has_recipes():
    return None
  # Get all recipes in db
  all_recipes = session.query(Recipe.id, Recipe.name).all()
  # Create an empty list for all recipes
  recipe_options = []
  # List all recipes in db
  print('\nAll Recipes:')
  # Loop over all recipes to display and append to empty list
  for recipe in all_recipes:
    print(f"\n\tID: {recipe[0]} - {recipe[1]}")
    recipe_options.append(recipe[0])
  # Ask user to input the recipe ID they want to delete
  recipe_id_to_delete = input('\nWhat recipe would you like to delete: ')
  # Verify the ID inputed is a number
  while not recipe_id_to_delete.isnumeric():
    print('\n\tError: ID must be a number')
    recipe_id_to_delete = input('\nWhat recipe would you like to delete: ')
  # Convert ID to an integer
  recipe_id_to_delete = int(recipe_id_to_delete)
  # Verify the ID inputed is an ID for a recipe
  if recipe_id_to_delete not in recipe_options:
    print(f'\nThe id you selected, {recipe_id_to_delete}, is not a valid recipe id. Try again.')
    return
  # Find the recipe in the DB
  recipe_to_delete = session.query(Recipe).filter(Recipe.id == recipe_id_to_delete).one()
  # Ask user to verify they want to delete the recipe
  print('\nAre you sure you would like to delete this recipe:\n')
  print(recipe_to_delete)
  print(20*'-')
  # Confirmation by user
  confirm_deletion = str(input("\nEnter 'yes' to delete or 'no' to cancel: ")).lower()
  while (not confirm_deletion == 'yes') and (not confirm_deletion == 'no'):
    print("\n\tError - your input is not either 'yes' or 'no'")
    confirm_deletion = str(input("\nEnter 'yes' to delete or 'no' to cancel: ")).lower()
  
  if confirm_deletion == 'no':
    print('The recipe will NOT be deleted.')
    return
  else:
    try:
      session.delete(recipe_to_delete)
      commit_changes('deleted')
    except Exception as e:
      print('There was an error deleting the recipe:')
      print(e)
      return
  
## View all Recipes
def view_recipes():
  # Create a list of all recipes in table
  recipes_list = session.query(Recipe).all()

  # Check if length of list is 0; if TRUE then return
  if len(recipes_list) == 0:
    print("There are no recipes. Make one yourself!")
    return None
  else:  
    print("\nAll Recipes:\n" + 20*'-')
    for recipe in recipes_list:
      print(recipe)

# Main Menu for Recipe App
def main_menu():
  choice = ""
  while (choice != "quit"):
    print("\nMain Menu" + '\n' + 20*'=')
    print("Pick a choice:")
    print(create_choice(1, 'Create a new recipe'))
    print(create_choice(2, 'Search for recipes by ingredients'))
    print(create_choice(3, 'Edit a recipe'))
    print(create_choice(4, 'Delete a recipe'))
    print(create_choice(5, 'View all recipes'))
    print("\t\tType 'quit' to exit the program.")
    choice = input("Your choice: ")

    if choice.lower() == 'quit':
      session.close()
      engine.dispose()
      break
    elif choice == '1':
      create_recipe()
    elif choice == '2':
      search_recipe()
    elif choice == '3':
      edit_recipe()
    elif choice == '4':
      delete_recipe()
    elif choice == '5':
      view_recipes()
    else:
      print(f"\n'{choice}' is not valid. Try again.\n")


main_menu()