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
    print(*self.shopping_list, sep = '\n')
    return
  
pet_store_list = ShoppingList('Pet Store Shopping List')

pet_store_list.add_item('dog food')
pet_store_list.add_item('frisbee')
pet_store_list.add_item('bowl')
pet_store_list.add_item('collars')
pet_store_list.add_item('flea collars')

pet_store_list.remove_item('flea collars')

pet_store_list.add_item('frisbee')

pet_store_list.view_list()