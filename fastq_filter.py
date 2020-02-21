import argparse
import  os.path

parser = argparse.ArgumentParser(description='Process arguments from user')
parser.add_argument('-min', '--min_length', type=int, help='minimum read length to survive filtration')
parser.add_argument('-k', '--keep_filtered', action='store_true',
                    help='Save reads that do not pass filtering into a separate file')
parser.add_argument('-o', '--output_base_name', help='Specify the prefix of output files')
parser.add_argument('-gc', '--gc_bounds', type=int, nargs='*',
                    help='Number or range of GC-content in reads for surviving. '
                         'One value to indicate a lower threshold.'
                         'Two values to set the minimum and maximum percentage.')
parser.add_argument('input_file', help='Input FASTQ file')
args = parser.parse_args()


def write_records(out_file, rec):
    with open(out_file, 'a') as out_f:
        out_f.write(rec[0] + '\n')
        out_f.write(rec[1] + '\n')
        out_f.write('+' + '\n')
        out_f.write(rec[2] + '\n')


def minlen(n, sequence):
    if len(sequence) >= n:
        return sequence, 'loser'
    else:
        return 'loser', sequence


def gc_content(sequence):
    guanin_count = sequence.count("G")
    cytosine_count = sequence.count("C")
    content = ((guanin_count + cytosine_count) / len(sequence)) * 100
    return round(content)


def gc_bounds(bounds_list, sequence):
    bounds_list.sort()  # отсортируем на всякий случай, если юзер перепутает местами большее и меньшее значение
    if len(bounds_list) == 0:
        pass  # нам ведь просто с этим ничего не надо делать...
    if len(bounds_list) > 2:
        raise ValueError('The number of borders cannot be more than two')
    if len(bounds_list) == 1:
        if gc_content(sequence) >= bounds_list[0]:
            return sequence, 'loser'
        else:
            return 'loser', sequence
    if len(bounds_list) == 2:
        if (gc_content(sequence) >= bounds_list[1]) and (gc_content(sequence) <= bounds_list[0]):
            return sequence, 'loser'
        else:
            return 'loser', sequence


if not args.output_base_name:   # разбираемся с названием по умолчанию
    args.output_base_name = args.input_file.rstrip('.fastq')
    print(args.output_base_name + ' processing... Wait...')


if os.path.exists(args.output_base_name + '_passed.fq'):    # проверка предсуществующих файлов
    os.remove(args.output_base_name + '_passed.fq')
if os.path.exists(args.output_base_name + '_failed.fq'):
    os.remove(args.output_base_name + '_failed.fq')

with open(args.input_file, "r") as in_f:  # читаем наш fastq файл
    for element in in_f:
        name = element.rstrip()
        seq = next(in_f).rstrip()
        next(in_f)
        quality = next(in_f).rstrip()

        record = name, seq, quality  # пусть это будет одним рекордом, не хочу ничего потерять

        ### исполнение команд ###

        if args.min_length and args.keep_filtered:  # дли минимальной длины с сохранением
            if minlen(args.min_length, record[1])[0] != 'loser':
                write_records(f"{args.output_base_name}_passed.fq", record)
            else:
                write_records(f"{args.output_base_name}_failed.fq", record)

        if args.min_length:  # для минимальной длины
            if minlen(args.min_length, record[1])[0] != 'loser':
                write_records(f"{args.output_base_name}_passed.fq", record)

        if args.gc_bounds and args.keep_filtered:  # для ГЦ-контента с сохранинением
            if gc_bounds(args.gc_bounds, record[1])[0] != 'loser':
                write_records(f"{args.output_base_name}_passed.fq", record)
            else:
                write_records(f"{args.output_base_name}_failed.fq", record)

        if args.gc_bounds:  # для ГЦ-контента
            if gc_bounds(args.gc_bounds, record[1])[0] != 'loser':
                write_records(f"{args.output_base_name}_passed.fq", record)

        if args.min_length and args.gc_bounds:  # сувмещаем
            if (gc_bounds(args.gc_bounds, record[1])[0] != 'loser') and \
                    (minlen(args.min_length, record[1])[0] != 'loser'):
                write_records(f"{args.output_base_name}_passed.fq", record)

        if args.min_length and args.gc_bounds: # сувмещаем с сохранением
            if (gc_bounds(args.gc_bounds, record[1])[0] != 'loser') and (minlen(args.min_length, record[1])[0] != 'loser'):
                write_records(f"{args.output_base_name}_passed.fq", record)
            else:
                write_records(f"{args.output_base_name}_failed.fq", record)
