print('Введите значения:')
a = float(input())
c = input()
b = float(input())
if c == '+':
    print(a + b)
elif c == '-':
    print(a - b)
elif c == '*':
    print(a * b)
elif c == '/':
    if b == 0.0:
        print('Деление на 0!')
    if b != 0.0:
        print(a / b)
elif c == 'mod':
    if b == 0.0:
        print('Деление на 0!')
    if b != 0.0:
        print(a % b)
elif c == 'pow':
    print(a ** b)
elif c == 'div':
    if b == 0.0:
        print('Деление на 0!')
    if b != 0.0:
        print(a // b)
