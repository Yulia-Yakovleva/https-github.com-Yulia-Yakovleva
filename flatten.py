def flat_list(request):
    result = []
    for element in request:                     # для каждого элемента в запросе
        if isinstance(element, (list, tuple)):  # если элемент - это список или кортеж,то
            # расширяет результат, добавляя в конец результат применения функции c элементом в качестве аргумента
            result.extend(flat_list(element))   # т.е. оставшиеся "нераскрытыми" списки здесь раскрываются
        else:
            result.append(element)
    return result
