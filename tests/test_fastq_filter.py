import unittest
import fastq_filter


class FastqFilterTest(unittest.TestCase):

    def test_minlen(self):
        threshhold = 10
        good_seq = 'GCGCTATAGCGCTATA'
        bad_seq = 'GCGCTATA'
        self.assertIsNot(fastq_filter.minlen(threshhold, good_seq)[1], 'looser')
        self.assertIsNot(fastq_filter.minlen(threshhold, bad_seq)[0], 'looser')
        self.assertIs(fastq_filter.minlen(threshhold, good_seq)[0], good_seq)
        self.assertIs(fastq_filter.minlen(threshhold, bad_seq)[1], bad_seq)

    def test_gc_content(self):
        seq = 'GCGCTATA'
        self.assertAlmostEqual(fastq_filter.gc_content(seq), 50)