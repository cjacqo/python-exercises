import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

# Load environment variables
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASS")

# Connect to mySQL user
conn = mysql.connector.connect(
  host='localhost',
  user=db_user,
  passwd=db_password
)

# Create cursor object
cursor = conn.cursor()

# Database name and table name and columns
db_name = "task_database"
table_name = "Recipes"

# SQL statements for database creation, use and table creation
sql_create_task_db = f"CREATE DATABASE IF NOT EXISTS {db_name}"
sql_use_task_db = f"USE {db_name}"
sql_create_recipe_table = f"CREATE TABLE IF NOT EXISTS {table_name} (\
id INT PRIMARY KEY AUTO_INCREMENT, \
name VARCHAR(50), \
ingredients VARCHAR(255), \
cooking_time INT, \
difficulty VARCHAR(20) \
)"

# Execute SQL statements
cursor.execute(sql_create_task_db)
cursor.execute(sql_use_task_db)
cursor.execute(sql_create_recipe_table)

# Helper functions
def create_choice(num, string):
  return f"\t\t{str(num)}. {string}"

def display_recipe(recipe):
  print("\nID:", recipe[0])
  print("Name:", recipe[1])
  print("Ingredients:", recipe[2])
  print("Cooking Time (mins):", recipe[3])
  print("Difficulty:", recipe[4])
  print('')

def calculate_difficulty(cooking_time, ingredients):
  num_ingredients = len(ingredients)
  if (cooking_time < 10 and num_ingredients < 4):
    return 'Easy'
  elif (cooking_time < 10 and num_ingredients >= 4):
    return 'Medium'
  elif (cooking_time >= 10 and num_ingredients < 4):
    return 'Intermediate'
  elif (cooking_time >= 10 and num_ingredients >= 4):
    return 'Hard'

# Main menu for user
def main_menu(conn, cursor):
  choice = ""
  while (choice != 'quit'):
    print("Main Menu" + '\n' + 20*'=')
    print("Pick a choice:")
    print(create_choice(1, 'Create a new recipe'))
    print(create_choice(2, 'Search for a recipe by ingredient'))
    print(create_choice(3, 'Update an existing recipe'))
    print(create_choice(4, 'Delete a recipe'))
    print(create_choice(5, 'View all recipes'))
    print("\t\tType 'quit' to exit the program.")
    choice = input("Your choice: ")

    if choice == '1':
      create_recipe(conn, cursor)
    elif choice == '2':
      search_recipe(conn, cursor)
    elif choice == '3':
      update_recipe(conn, cursor)
    elif choice == '4':
      delete_recipe(conn, cursor)
    elif choice == '5':
      view_recipes(conn, cursor)

# Choice operations
def create_recipe(conn, cursor):
  # Ask for name of recipe
  name = str(input("\nName of the recipe: "))

  # Ask for cooking time of recipe
  cooking_time = int(input("\nCooking time (minutes): "))

  # Ask for ingredients of recipe
  ingredients = [str(ingredients) for ingredients in input('\nEnter the ingredients (separate with comma and space): ').split(', ')]

  # Calculate difficulty
  difficulty = calculate_difficulty(cooking_time, ingredients)

  # Convert ingredients list to a string
  ingredients_str = ', '.join(ingredients)

  # SQL statement and values tuple
  sql = f"INSERT INTO {table_name} (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)"
  val = (name, ingredients_str, cooking_time, difficulty)

  # Execute SQL statement to insert recipe into table
  cursor.execute(sql, val)

  # Commit changes to table
  conn.commit()

  print(f"Recipe for {name} has been insterted into table.")

def search_recipe(conn, cursor):
  all_ingredients = []

  # Fetch ingredients from table
  cursor.execute(f"SELECT ingredients FROM {table_name}")
  results = cursor.fetchall()

  # Loop through results
  for ingredients_list in results:
    for recipe_ingredients in ingredients_list:
      recipe_ingredients_list = recipe_ingredients.split(', ')
      all_ingredients.extend(recipe_ingredients_list)

  # Remove duplicates from list
  all_ingredients = list(dict.fromkeys(all_ingredients))

  # Show available ingredients
  all_ingredients_list = list(enumerate(all_ingredients))

  print("\nAll Ingredients:\n" + 20*'-')
  for index, tup in enumerate(all_ingredients_list):
    print(str(tup[0]+1) + ". " + tup[1])
  
  try:
    ingredient_num = input("\nEnter the number corresponding to the ingredient you want to select: ")
    ingredient_index = int(ingredient_num) - 1
    ingredient_found = all_ingredients_list[ingredient_index][1]
    print('\nYou selected:', ingredient_found)
  except:
    print('An unexpected error occurred.')
  else:
    print("\nThe recipe(s) below include the selected ingredient:\n", 20*'-')

    sql = f"SELECT * FROM {table_name} WHERE ingredients LIKE %s"
    val = ('%' + ingredient_found + '%', )

    cursor.execute(sql, val)

    recipe_results = cursor.fetchall()

    for row in recipe_results:
      display_recipe(row)

def update_recipe(conn, cursor):
  view_recipes(conn, cursor)

  def update_difficulty(id):
    cursor.execute(f"SELECT * FROM {table_name} WHERE id = %s", (id, ))
    recipe_to_update = cursor.fetchall()

    name = recipe_to_update[0][1]
    ingredients = tuple(recipe_to_update[0][2].split(','))
    cooking_time = recipe_to_update[0][3]

    updated_difficulty = calculate_difficulty(cooking_time, ingredients)
    print("Updated difficulty:", updated_difficulty)
    cursor.execute(f"UPDATE {table_name} SET difficulty = %s WHERE id = %s", (updated_difficulty, id))
    
  # Ask for ID of recipe to update
  id_to_update = int((input("\nEnter the ID of the recipe you want to update: ")))

  # Ask for the column to update
  column_to_update = str(input("\nEnter the column you want to update: (name, cooking_time or ingredients): "))

  # Ask to input the new value
  updated_value = (input(f"\nEnter the new value for {column_to_update}: "))
  print("Choice:", updated_value)

  if column_to_update == 'name':
    cursor.execute(f"UPDATE {table_name} SET name = %s WHERE id = %s", (updated_value, id_to_update))
  elif column_to_update == 'cooking_time':
    cursor.execute(f"UPDATE {table_name} SET cooking_time = %s WHERE id = %s", (updated_value, id_to_update))
    update_difficulty(id_to_update)
  elif column_to_update == 'ingredients':
    cursor.execute(f"UPDATE {table_name} SET ingredients = %s WHERE id = %s", (updated_value, id_to_update))
    update_difficulty(id_to_update)
  
  print("Updated recipe successfully.")
  conn.commit()
    
def delete_recipe(conn, cursor):
  view_recipes(conn, cursor)

  # Ask for the ID of recipe to be deleted
  id_to_delete = int((input("\nEnter the ID of the recipe you want to delete: ")))

  # Delete the recipe
  cursor.execute(f"DELETE FROM {table_name} WHERE id = (%s)", (id_to_delete, ))

  # Commit changes
  conn.commit()
  print("\nRecipe was deleted successfully.")
  return

def view_recipes(conn, cursor):
  print("\nAll Recipes:\n" + 20*'-')

  # Get all recipes
  cursor.execute(f"SELECT * FROM {table_name}")
  results = cursor.fetchall()

  if len(results) == 0:
    print('\nNo recipes. Back to main menu.\n')
    return
  else:
    for row in results:
      display_recipe(row)

main_menu(conn, cursor)
print("End program.")