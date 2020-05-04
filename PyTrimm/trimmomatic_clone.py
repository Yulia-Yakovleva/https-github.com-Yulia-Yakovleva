import argparse
import os.path


def write_record(out_file, rec):
    with open(out_file, 'a') as out_f:
        out_f.write(rec[0] + '\n')
        out_f.write(rec[1] + '\n')
        out_f.write('+' + '\n')
        out_f.write(rec[2] + '\n')


def partition_by_length(sequence, n):
    if n is None:
        return True
    if len(sequence) >= n:
        return True
    else:
        return False


def gc_content(sequence):
    guanin_count = sequence.count("G")
    cytosine_count = sequence.count("C")
    content = ((guanin_count + cytosine_count) / len(sequence)) * 100
    return round(content)


def gc_bounds(sequence, bounds_list):
    if bounds_list is None or len(bounds_list) == 0:
        return True
    # отсортируем на всякий случай, если юзер перепутает местами большее и меньшее значение
    bounds_list.sort()
    if len(bounds_list) > 2:
        raise ValueError('The number of borders cannot be more than two')
    if len(bounds_list) == 1:
        if gc_content(sequence) >= bounds_list[0]:
            return True
        else:
            return False
    if len(bounds_list) == 2:
        if (gc_content(sequence) <= bounds_list[1]) and \
                (gc_content(sequence) >= bounds_list[0]):
            return True
        else:
            return False


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


def headcrop(n, sequence):
    if n is not None:
        return sequence[n:]
    else:
        return sequence


def crop(n, sequence):
    if n is not None:
        return sequence[:n]
    else:
        return sequence


def leading(threshold, sequence, quality):
    if threshold is not None:
        for letter in quality:  # пробегаемся с начала последовательности
            if assess_qscore(letter)[0] >= threshold:  # если наткнулись на значение > или = threshold
                return sequence[quality.index(letter):]  # возвращаем sequence, начиная с индекса значения
    else:
        return sequence


def trailing(threshold, sequence, quality):
    if threshold is not None:
        out_seq = leading(threshold, sequence[::-1], quality[::-1])
        return out_seq[::-1]
    else:
        return sequence


def sliding_window(params, sequence, quality):
    if params is not None:
        window = params[0]
        threshold = params[1]
        for i in range(0, len(sequence), window):
            kmer = quality[i:i + window]
            if count_average_quality(kmer) < threshold:
                return sequence[:i]
    else:
        return sequence


def check_gc_and_len_surviving(sequence, bounds_list, n):
    if gc_bounds(sequence, bounds_list) and partition_by_length(sequence, n):
        return True
    else:
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process arguments from user')
    parser.add_argument('-crop', '--crop', type=int,
                        help='Cut the read to a specified length.')
    parser.add_argument('-gc', '--gc_bounds', type=int, nargs='*',
                        help='Number or range of GC-content in reads for surviving. '
                             'One value to indicate a lower threshold.'
                             'Two values to set the minimum and maximum percentage.')
    parser.add_argument('-headcrop', type=int,
                        help='Cut the specified number of bases from the start of the read.')
    parser.add_argument('-k', '--keep_filtered', action='store_true',
                        help='Save reads that do not pass filtering into a separate file.')
    parser.add_argument('-leading', '--leading', type=int,
                        help='Cut bases off the start of a read, if below a threshold quality.')
    parser.add_argument('-min', '--min_length', type=int,
                        help='Minimum read length to survive filtration.')
    parser.add_argument('-o', '--output_base_name',
                        help='Specify the prefix of output files.')
    parser.add_argument('-sliding_window', '--sliding_window', type=int, nargs=2,
                        help='Performs a sliding window trimming approach. It starts scanning at the 5\' end and'
                             'clips the read once the average quality within the window falls below a threshold.'
                             'First value to set window size as the number of bases.'
                             'Second value to set quality threshold.')
    parser.add_argument('input_file', help='Input FASTQ file')
    parser.add_argument('-trailing', '--trailing', type=int,
                        help='Cut bases off the end of a read, if below a threshold quality.')
    args = parser.parse_args()

    if not args.output_base_name:  # разбираемся с названием по умолчанию
        args.output_base_name = args.input_file.rstrip('.fastq')

    if os.path.exists(args.output_base_name + '_passed.fq'):  # проверка предсуществующих файлов
        os.remove(args.output_base_name + '_passed.fq')
    if os.path.exists(args.output_base_name + '_failed.fq'):
        os.remove(args.output_base_name + '_failed.fq')
    if os.path.exists(args.output_base_name):
        os.remove(args.output_base_name)

    with open(args.input_file, "r") as in_f:  # читаем наш fastq файл
        total_reads = 0
        passed_reads = 0
        failed_reads = 0
        for element in in_f:
            total_reads += 1
            name = element.rstrip()
            seq = next(in_f).rstrip()
            next(in_f)
            qual = next(in_f).rstrip()

            # исполнение команд #
            if leading(args.leading, seq, qual) is not None:
                bases = leading(args.leading, seq, qual)
            else:
                bases = ''
            if trailing(args.trailing, bases, qual) is not None:
                bases = trailing(args.trailing, bases, qual)
            else:
                bases = ''
            if sliding_window(args.sliding_window, bases, qual) is not None:
                bases = sliding_window(args.sliding_window, bases, qual)
            else:
                bases = ''
            if headcrop(args.headcrop, bases) is not None:
                bases = headcrop(args.headcrop, bases)
            else:
                bases = ''
            if crop(args.crop, bases) is not None:
                bases = crop(args.crop, bases)
            else:
                bases = ''

            # фильтруем и записываем (в дропнутых - исходные риды без тримминга!!!)
            if len(bases) == 0:  # рид нулевой длины. либо не пишем ничего, либо пишем в дропнутые исходник
                if args.keep_filtered:
                    droped_read = name, seq, qual
                    write_record(f"{args.output_base_name}_failed.fq", droped_read)
                    failed_reads += 1
            else:  # рид ненулевой длины, проверяем, пройдет ли фильтрацию?
                if check_gc_and_len_surviving(seq, args.gc_bounds, args.min_length) is True:
                    # рид прошел фильтрацию, как сохранять?
                    surv_read = name, bases, qual
                    if not args.keep_filtered:
                        # дропнутые не пишем, просто сохраняем выживший рид без расширения .fq
                        write_record(f"{args.output_base_name}", surv_read)
                        passed_reads += 1
                    else:
                        # сохраняем выжившие как _passed.fq
                        write_record(f"{args.output_base_name}_passed.fq", surv_read)
                        passed_reads += 1
                elif check_gc_and_len_surviving(seq, args.gc_bounds, args.min_length) is False:
                    # рид не прошел фильтрацию, как сохранять?
                    droped_read = name, seq, qual
                    # сохраняем как _failed.fq
                    if args.keep_filtered:
                        write_record(f"{args.output_base_name}_failed.fq", droped_read)
                        failed_reads += 1


        print(f'Всего было обработано {total_reads} ридов. '
              f'{passed_reads} из них пережили фильтрацию. '
              f'{failed_reads} рида были отброшены.')
