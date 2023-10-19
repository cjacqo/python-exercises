a = int(input('Enter a number '))
b = int(input('Enter another number '))
operator = input('Enter either a + or - ')

if operator == '+':
  print(str(a + b))
elif operator == '-':
  print(str(a - b))
else:
  print('Error: You did not enter either a + or -')