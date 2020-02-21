class Dna(str):

    def __init__(self, user_seq, nucleotides='ATGCNatgcn'):
        if len(user_seq) == 0:
            raise ValueError('The sequence is empty')
        else:
            for letter in set(user_seq):
                if letter not in nucleotides:
                    raise ValueError(
                        'The sequence contains invalid characters')
                else:
                    self.seq = user_seq.upper()

    def gc_content(self):
        guanin_count = self.seq.count("G")
        cytosine_count = self.seq.count("C")
        content = (guanin_count + cytosine_count) / len(self.seq)
        return round(content, 2)

    def reverse_complement(self, complementarity_rule={'A': 'T',
                                                       'C': 'G',
                                                       'G': 'C',
                                                       'T': 'A',
                                                       'U': 'A',
                                                       'N': 'N'}):
        reversed_seq = self.seq[::-1]  # ATGCACA -> ACACGTA
        revcomplement_seq = ''.join(
            complementarity_rule[base] for base in reversed_seq)  # УРА
        return revcomplement_seq

    def transcribe(self, transcription_rule={'A': 'U',
                                             'C': 'G',
                                             'G': 'C',
                                             'T': 'A',
                                             'N': 'N'}):
        if isinstance(self, Rna):
            raise ValueError('The RNA sequence cannot be transcribed')
        mRNA = ''.join(transcription_rule[base] for base in self.seq)
        return Rna(mRNA)


class Rna(Dna):

    def __init__(self, user_seq, ribonucleotides='AUGCNaugcn'):
        if len(user_seq) == 0:
            raise ValueError('The sequence is empty')
        else:
            for letter in set(user_seq):
                if letter not in ribonucleotides:
                    raise ValueError(
                        'The sequence contains invalid characters')
                else:
                    self.seq = user_seq.upper()
