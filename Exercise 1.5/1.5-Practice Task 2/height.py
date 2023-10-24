class Height(object):
  def __init__(self, feet, inches):
    self.feet = feet
    self.inches = inches

  def __str__(self):
    return str(self.feet) + ' feet, ' + str(self.inches) + ' inches'
  
  def __add__(self, other):
    # Converting both objects' heights into inches
    height_A_inches = self.feet * 12 + self.inches
    height_B_inches = other.feet * 12 + other.inches

    # Adding them up
    total_height_inches = height_A_inches + height_B_inches

    # Getting the output in feet
    output_feet = total_height_inches // 12

    # Getting the output in inches
    output_inches = total_height_inches - (output_feet * 12)

    return Height(output_feet, output_inches)
  
  def __sub__(self, other):
    # Converting both objects' height into inches
    height_A_inches = self.feet * 12 + self.inches
    height_B_inches = other.feet * 12 + other.inches

    # Subtracting them
    if height_A_inches > height_B_inches:
      total_height_inches = height_A_inches - height_B_inches
    else:
      total_height_inches = height_B_inches - height_A_inches

    # Getting the output in feet
    output_feet = total_height_inches // 12

    # Getting the output in inches
    output_inches = total_height_inches - (output_feet * 12)

    return Height(output_feet, output_inches)
      
person_A_height = Height(5, 10)
person_B_height = Height(4, 10)
height_sum = person_A_height + person_B_height

print('Total height:', height_sum)

person_C_height = Height(3, 9)
person_D_height = Height(5, 10)
height_dif = person_C_height - person_D_height

print('Total height:', height_dif)