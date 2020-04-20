import argparse
import os.path


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
    # отсортируем на всякий случай, если юзер перепутает местами большее и
    # меньшее значение
    bounds_list.sort()
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
        if (gc_content(sequence) <= bounds_list[1]) and (
                gc_content(sequence) >= bounds_list[0]):
            return sequence, 'loser'
        else:
            return 'loser', sequence


# вводим правила кодировки качество ASCII->Symbol->Q-score (это phred33 кодировка)
symbols = [chr(x) for x in range(33, 74)]
q_scores = [x for x in range(0, 41)]
quality_score_encoding = dict(zip(symbols, q_scores))


def assess_qscore(quality):
    qscores_list = []
    for symbol in quality:
        qscores_list.append(quality_score_encoding[symbol])
    return qscores_list


def count_average_quality(quality):
    scores = assess_qscore(quality)
    average = sum(scores) / len(scores)
    return average


def HEADCROP(n, sequence):  # cut the specified number of bases from the start of the read
    return sequence[n:]


def CROP(n, sequence):  # cut the read to a specified length
    return sequence[:n]


def TRAILING(threshold, sequence, quality):  # cut bases off the end of a read, if below a threshold quality
    out_seq = LEADING(threshold, sequence[::-1], quality[::-1])
    return out_seq[::-1]


def LEADING(threshold, sequence, quality):  # cut bases off the start of a read, if below a threshold quality
    for letter in quality:  # пробегаемся с начала последовательности
        if assess_qscore(letter)[0] >= threshold:  # если наткнулись на значение > или = threshold
            return sequence[quality.index(letter):]  # возвращаем sequence, начиная с индекса значения


def SLIDINGWINDOW(threshold, window, sequence, quality):
    for i in range(0, len(sequence), window):
        kmer = quality[i:i + window]
        if count_average_quality(kmer) < threshold:
            return sequence[:i]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process arguments from user')
    parser.add_argument(
        '-min',
        '--min_length',
        type=int,
        help='minimum read length to survive filtration')
    parser.add_argument(
        '-k',
        '--keep_filtered',
        action='store_true',
        help='Save reads that do not pass filtering into a separate file')
    parser.add_argument(
        '-o',
        '--output_base_name',
        help='Specify the prefix of output files')
    parser.add_argument(
        '-gc',
        '--gc_bounds',
        type=int,
        nargs='*',
        help='Number or range of GC-content in reads for surviving. '
             'One value to indicate a lower threshold.'
             'Two values to set the minimum and maximum percentage')
    parser.add_argument('input_file', help='Input FASTQ file')
    parser.add_argument(
        '-crop', '--crop',
        type=int,
        help='Cut the read to a specified length')
    parser.add_argument(
        '-leading', '--leading',
        type=int,
        help='Cut bases off the start of a read, if below a threshold quality')
    parser.add_argument(
        '-trailing', '--trailing',
        type=int,
        help='Cut bases off the end of a read, if below a threshold quality')
    parser.add_argument(
        '-slidingwindow', '--slidingwindow',
        type=int,
        nargs=2,
        help='Performs a sliding window trimming approach. It starts scanning at the 5\'end and'
             'clips the read once the average quality within the window falls below a threshold')
    args = parser.parse_args()

    if not args.output_base_name:  # разбираемся с названием по умолчанию
        args.output_base_name = args.input_file.rstrip('.fastq')
        print(args.output_base_name + ' processing... Wait...')

    if os.path.exists(
            args.output_base_name +
            '_passed.fq'):  # проверка предсуществующих файлов
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

            # исполнение команд #

            if args.min_length and args.gc_bounds and not args.keep_filtered:  # сувмещаем без сохранения
                if (gc_bounds(args.gc_bounds, record[1])[0] != 'loser') and \
                        (minlen(args.min_length, record[1])[0] != 'loser'):
                    write_records(f"{args.output_base_name}_passed.fq", record)

            if args.min_length and args.gc_bounds and args.keep_filtered:  # сувмещаем с сохранением
                if (gc_bounds(args.gc_bounds, record[1])[0] != 'loser') and \
                        (minlen(args.min_length, record[1])[0] != 'loser'):
                    write_records(f"{args.output_base_name}_passed.fq", record)
                else:
                    write_records(f"{args.output_base_name}_failed.fq", record)

            if args.min_length and args.keep_filtered and not args.gc_bounds:  # дли минимальной длины с сохранением
                if minlen(args.min_length, record[1])[0] != 'loser':
                    write_records(f"{args.output_base_name}_passed.fq", record)
                else:
                    write_records(f"{args.output_base_name}_failed.fq", record)

            if args.min_length and not args.keep_filtered and not args.gc_bounds:  # для минимальной длины без сохранения
                if minlen(args.min_length, record[1])[0] != 'loser':
                    write_records(f"{args.output_base_name}_passed.fq", record)

            if args.gc_bounds and args.keep_filtered and not args.min_length:  # для ГЦ-контента с сохранинением
                if gc_bounds(args.gc_bounds, record[1])[0] != 'loser':
                    write_records(f"{args.output_base_name}_passed.fq", record)
                else:
                    write_records(f"{args.output_base_name}_failed.fq", record)

            if args.gc_bounds and not args.keep_filtered and not args.min_length:  # для ГЦ-контента без сохранения
                if gc_bounds(args.gc_bounds, record[1])[0] != 'loser':
                    write_records(f"{args.output_base_name}_passed.fq", record)