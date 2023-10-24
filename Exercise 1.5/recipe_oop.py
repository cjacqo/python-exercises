class Recipe:
  all_ingredients = []
  
  def __init__(self, name, cooking_time, ingredients):
    self.name = name
    self.cooking_time = cooking_time
    self.ingredients = ingredients
    self.difficulty = None

  # Getters: name, cooking time, ingredients, difficulty
  def get_name(self):
    return self.name
  
  def get_cooking_time(self):
    return self.cooking_time
  
  def get_ingredients(self):
    return self.ingredients
  
  def get_difficulty(self):
    if not self.difficulty:
      self.calculate_difficulty(self)
    return self.difficulty
  
  # Setters: name, cooking time
  def set_name(self, name):
    self.name = name

  def set_cooking_time(self, cooking_time):
    self.cooking_time = cooking_time
  
  # Methods
  def add_ingredients(self, *ingredients):
    for ingredient in ingredients:
      self.ingredients.append(ingredient)
    self.update_all_ingredients()
  
  def calculate_difficulty(self):
    num_ingredients = len(self.ingredients)
    if (self.cooking_time < 10 and num_ingredients < 4):
      self.difficulty = 'Easy'
    elif (self.cooking_time < 10 and num_ingredients >= 4):
      self.difficulty = 'Medium'
    elif (self.cooking_time >= 10 and num_ingredients < 4):
      self.difficulty = 'Intermediate'
    elif (self.cooking_time >= 10 and num_ingredients >= 4):
      self.difficulty = 'Hard'

  def search_ingredient(self, ingredient):
    return ingredient in self.ingredients
  
  def update_all_ingredients(self):
    for el in self.ingredients:
      if el not in self.all_ingredients:
        Recipe.all_ingredients.append(el)

  # String method
  def __str__(self):
    return f"Recipe: {self.name}\nCooking Time (mins): {self.cooking_time}\nIngredients: {', '.join(self.ingredients)}\nDifficulty: {self.difficulty}\n"
  
def recipe_search(data, search_term):
  print(f"Recipes that container '{search_term}':\n")
  for recipe in data:
    if recipe.search_ingredient(search_term):
      print(recipe)
    else:
      print(f"No recipes contain '{search_term}'\n")
      break

# Main Code
tea = Recipe('Tea', 5, ['Tea Leaves', 'Sugar', 'Water'])
coffee = Recipe('Coffee', 5, ['Coffee Powder', 'Sugar', 'Water'])
cake = Recipe('Cake', 50, ['Sugar', 'Butter', 'Eggs', 'Vanilla Essence', 'Flour', 'Baking Powder', 'Milk'])
smootie = Recipe('Banana Smoothie', 5, ['Bananas', 'Milk', 'Peanut Butter', 'Sugar', 'Ice Cubes'])

recipes_list = [tea, coffee, cake, smootie]

for recipe in recipes_list:
  print(recipe)

for ingredient in ['Water', 'Sugar', 'Banana']:
  recipe_search(recipes_list, ingredient)