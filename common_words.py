# checkio("hello,world", "hello,earth") == "hello"
# checkio("one,two,three", "four,five,six") == ""
# checkio("one,two,three", "four,five,one,two,six,three") == "one,three,two"


# def chekio(a = input().split(','), b = input().split(',')):
def chekio(a, b):
    a = list(a.split(','))
    b = list(b.split(','))
    out_list = []
    for element in a:
        if element in b:
            out_list.append(element)
    out_list.sort()
    out_string = ','.join(out_list)
    return out_string


print('"' + chekio("one,two,three", "four,five,one,two,six,three") + '"')
