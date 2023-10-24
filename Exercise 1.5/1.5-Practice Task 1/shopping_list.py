class ShoppingList(object):
  def __init__(self, list_name):
    self.list_name = list_name
    self.shopping_list = []

  def item_exists(self, item):
    return item in self.shopping_list

  def add_item(self, item):
    if self.item_exists(item):
      print('Item', item, 'already exists')
      return
    else:
      self.shopping_list.append(item)
      return
    
  def remove_item(self, item):
    if self.item_exists(item):
      self.shopping_list.remove(item)
      return
    else:
      print('Item', item, 'does not exist')
      return
    
  def view_list(self):
    print('\nItems in', str(self.list_name) + '\n' + 30*'-')
    for item in self.shopping_list:
      print(' - ' + str(item))
    return
  
  def merge_lists(self, obj):
    # Creating a name for our new, merged shopping list
    merged_lists_name = 'Merged List - ' + str(self.list_name) + ' + ' + str(obj.list_name)

    # Creating an empty ShoppingList object
    merged_lists_obj = ShoppingList(merged_lists_name)

    # Adding the first shopping list's items to our new list
    merged_lists_obj.shopping_list = self.shopping_list.copy()

    # Adding the second shopping list's items to our new list -
    # we're doing this so that ther won't be any repeated items
    # in the final list, if both source lists contain common
    # items between each other
    for item in obj.shopping_list:
      if not item in merged_lists_obj.shopping_list:
        merged_lists_obj.shopping_list.append(item)
    
    # Returning our new, merged object
    return merged_lists_obj
  
pet_store_list = ShoppingList('Pet Store Shopping List')
grocery_store_list = ShoppingList('Grocery Store List')

for item in ['dog food', 'frisbee', 'bowl', 'collars', 'flea collars']:
  pet_store_list.add_item(item)

for item in ['fruits', 'vegetables', 'bowl', 'ice cream']:
  grocery_store_list.add_item(item)

merged_list = ShoppingList.merge_lists(pet_store_list, grocery_store_list)

merged_list.view_list()