s = [0]
while s[0] != 'stop':
    print('Программа запущена! Для выхода из программы введите stop, а пока...\nВедите непустой массив целых чисел:')
    s = [(i) for i in input().split()]


    def checkio(s):
        repetitive = []
        for n in s:
            if s.count(n) > 1:
                repetitive.append(n)
        print('Неуникальные элементы данного массива: ' + str(repetitive))


    checkio(s)
else:
    print('Программа завершила работу.')
