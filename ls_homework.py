# 1. Составить список из чисел от 1 до 1000, которые имеют в своём составе 7.

my_list = [x for x in range(1, 1001) if '7' in str(x)]

# Проверка
# print(my_list)

# 2. Взять предложение
# Would it save you a lot of time if I just gave up and went mad now?
# и сделать его же без гласных.

vowels = {'a', 'e', 'i', 'o', 'u'}
sentence = 'Would it save you a lot of time if I just gave up and went mad now?'
sentence_without_volwes = ''.join(
    [letter for letter in sentence if letter not in vowels])

# Проверка
# print(sentence_without_volwes)


# 3. Для предложения
# The ships hung in the sky in much the same way that bricks don't
# составить словарь, где слову соответствует его длина.

sentence = "The ships hung in the sky in much the same way that bricks don't"

# Решение 1 (неэлегантно)
word_length_dict_1 = dict(zip(sentence.split(' '),
                              [len(word) for word in sentence.split(' ')]))

# Решение 2 (элегантно)
word_length_dict_2 = {word: len(word) for word in sentence.split(' ')}


# Проверка
# print(word_length_dict_1 == word_length_dict_2)


# 4*. Для чисел от 1 до 1000 наибольшая цифра, на которую они делятся (1-9).
# функциональные костыли...


def check_divisibility(x, y):
    if int(y) != 0 and int(x) % int(y) == 0:
        return y


def get_max(number):
    mini_list = []
    for numeral in number:
        if check_divisibility(number, numeral):
            mini_list.append(int(check_divisibility(number, numeral)))
    if mini_list:
        return max(mini_list)


numbers = [str(i) for i in range(1, 1001)]
answer_dict = {int(num): get_max(num) for num in numbers}
# проерка
print(answer_dict)


# 5*. Список всех чисел от 1 до 1000, не имеющих делителей среди чисел от 2 до 9.
# почти как генератор простых чисел из курса Кости, только надо убрать
# простые числа из первого десятка

# Решение: костыль ты мой костыль...
def check_simple_divisibility(x):
    if x % 2 != 0 and x % 3 != 0 \
            and x % 5 != 0 and x % 7 != 0:
        return x


answer = list(
    filter(
        lambda x: check_simple_divisibility(x), [
            i for i in range(
                1, 1001)]))

# Проверка
# print(answer)
