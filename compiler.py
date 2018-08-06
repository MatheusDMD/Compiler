command = (str(input("Calculator: "))).replace(" ", "")
error = 0
numbers = []
operators = []
number = ""
for item in command:
    if item.isdigit():
        number += item
    elif item == '+' or item == '-':
        numbers.append(int(number))
        operators.append(item)
        number = ""
    else:
        error = 1
        print("ERRO")
        break

numbers.append(int(number))

i = 0
while len(numbers) > 1:
    a = numbers.pop(0)
    b = numbers.pop(0)
    op = operators.pop(0)
    if op == '+':
        res = a + b
    elif op == '-':
        res = a - b
    numbers.insert(0, res)

print(numbers[0])