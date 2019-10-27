# create_intervals({1, 2, 3, 4, 5, 7, 8, 12}) == [(1, 5), (7, 8), (12, 12)]
# create_intervals({1, 2, 3, 6, 7, 8, 4, 5}) == [(1, 8)]


def create_intervals(input_set):
    input_list = sorted(list(input_set))
    # print(input_list)
    answ = [[input_list[0]]]
    # print(answ[-1][-1])
    for element in range(1, len(input_list)):
        if input_list[element] == (answ[-1][-1] + 1):
            answ[-1].append(input_list[element])
        else:
            answ.append([input_list[element]])
    final = []
    for sublist in answ:
        final_answer = (sublist[0], sublist[-1])
        final.append(final_answer)
    return final


print(create_intervals({1, 20, -1, -3, 2, 3, 4, 5, 6, 7, 8, 12}))
