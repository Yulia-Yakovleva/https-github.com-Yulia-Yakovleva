def group_equal(input_list):
    if len(input_list) < 1:
        return input_list
    elif len(input_list) == 1:
        return [input_list]
    else:
        answ = [[input_list[0]]]
        for element in input_list:
            if element == answ[-1][-1]:  # если элемент равен последнему элементу списка в списке
                # ГЕНИАЛЬНО
                answ[-1].append(element)
            else:
                answ.append([element])
        return answ


# print(group_equal([1, 1, 4, 4, 4, "hello", "hello", 4]))
# print(group_equal([1, 2, 3, 4]))
# print(group_equal([1]))
# print(group_equal([]))
