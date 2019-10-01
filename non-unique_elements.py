massive = [0]


def checkio(request):
    repetitive = []
    for element in request:
        if request.count(element) > 1:
            repetitive.append(element)
    return repetitive


while massive[0] != 'stop':
    print('Программа запущена! Для выхода из программы введите stop, а пока...'
          '\nВедите непустой массив целых чисел:')
    massive = [(i) for i in input().split()]
    print('Неуникальные элементы данного массива: ' + str(checkio(massive)))
else:
    print('Программа завершила работу.')
