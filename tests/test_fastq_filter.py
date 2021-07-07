import unittest
import fastq_filter


class FastqFilterTest(unittest.TestCase):

    def test_minlen_good_seq(self):
        threshhold = 10
        seq = 'GCGCTATAGCGCTATA'
        self.assertIs(fastq_filter.minlen(threshhold, seq)[0], seq)
        self.assertIs(fastq_filter.minlen(threshhold, seq)[1], 'loser')

    def test_minlen_bad_seq(self):
        threshhold = 10
        seq = 'GCGCTATA'
        self.assertIs(fastq_filter.minlen(threshhold, seq)[0], 'loser')
        self.assertIs(fastq_filter.minlen(threshhold, seq)[1], seq)

    def test_gc_content(self):
        seq = 'GCGCTATA'
        self.assertAlmostEqual(fastq_filter.gc_content(seq), 50)

    def test_gc_bounds_one_bound_good_seq(self):
        bound = [30]
        seq = 'GCGCTATAGCGCTATA'
        self.assertIs(fastq_filter.gc_bounds(bound, seq)[0], seq)
        self.assertIs(fastq_filter.gc_bounds(bound, seq)[1], 'loser')

    def test_gc_bounds_one_bound_bad_seq(self):
        bound = [30]
        seq = 'ATATATATATATAT'
        self.assertIs(fastq_filter.gc_bounds(bound, seq)[0], 'loser')
        self.assertIs(fastq_filter.gc_bounds(bound, seq)[1], seq)

    def test_gc_bounds_two_bounds_good_seq(self):
        bounds = [30, 60]
        seq = 'GCGCTATAGCGCTATA'
        self.assertIs(fastq_filter.gc_bounds(bounds, seq)[0], seq)
        self.assertIs(fastq_filter.gc_bounds(bounds, seq)[1], 'loser')

    def test_gc_bounds_two_bounds_bad_seq(self):
        bounds = [30, 60]
        seq = 'ATATATATATATAT'
        self.assertIs(fastq_filter.gc_bounds(bounds, seq)[0], 'loser')
        self.assertIs(fastq_filter.gc_bounds(bounds, seq)[1], seq)

    def test_gc_bounds_zero_bounds(self):
        zero_bounds = []
        seq = 'GCGCTATAGCGCTATA'
        self.assertIsNone(fastq_filter.gc_bounds(zero_bounds, seq))

    def test_gc_bounds_rises(self):
        more_bounds = [20, 30, 40]
        seq = 'GCGCTATAGCGCTATA'
        # вот так можно проверить, кинет ли ошибку, когда надо ее кидать
        with self.assertRaises(ValueError):
            fastq_filter.gc_bounds(more_bounds, seq)
