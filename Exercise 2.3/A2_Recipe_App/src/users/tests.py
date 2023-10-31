from django.test import TestCase
from .models import User

# Create your tests here.
class UserModelTest(TestCase):
  def setUpTestData():
    User.objects.create(
      name='Test Testington'
    )
  
  def test_name_max_length(self):
    # Get a user object to test
    recipe = User.objects.get(id=1)

    # Get the metadata for the 'name' field and use it to query its max_length
    max_length = recipe._meta.get_field('name').max_length

    # Compare the value to the expected result i.e. 50
    self.assertEqual(max_length, 50)