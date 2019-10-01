massive = [0]
repetitive = []
while massive[0] != 'stop':
    print('Программа запущена! Для выхода из программы введите stop, а пока...\nВедите непустой массив целых чисел:')
    massive = [(i) for i in input().split()]

    def checkio(s):
        for element in massive:
            if massive.count(element) > 1:
                repetitive.append(element)
                return repetitive

    checkio(massive)
    print('Неуникальные элементы данного массива: ' + str(repetitive))
else:
    print('Программа завершила работу.')
