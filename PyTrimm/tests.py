import unittest
import trimmomatic_clone


class FastqFilterTest(unittest.TestCase):

    def test_minlen_good_seq(self):
        threshhold = 10
        seq = 'GCGCTATAGCGCTATA'
        self.assertIs(trimmomatic_clone.minlen(threshhold, seq)[0], seq)
        self.assertIs(trimmomatic_clone.minlen(threshhold, seq)[1], 'loser')

    def test_minlen_bad_seq(self):
        threshhold = 10
        seq = 'GCGCTATA'
        self.assertIs(trimmomatic_clone.minlen(threshhold, seq)[0], 'loser')
        self.assertIs(trimmomatic_clone.minlen(threshhold, seq)[1], seq)

    def test_gc_content(self):
        seq = 'GCGCTATA'
        self.assertAlmostEqual(trimmomatic_clone.gc_content(seq), 50)

    def test_gc_bounds_one_bound_good_seq(self):
        bound = [30]
        seq = 'GCGCTATAGCGCTATA'
        self.assertIs(trimmomatic_clone.gc_bounds(bound, seq)[0], seq)
        self.assertIs(trimmomatic_clone.gc_bounds(bound, seq)[1], 'loser')

    def test_gc_bounds_one_bound_bad_seq(self):
        bound = [30]
        seq = 'ATATATATATATAT'
        self.assertIs(trimmomatic_clone.gc_bounds(bound, seq)[0], 'loser')
        self.assertIs(trimmomatic_clone.gc_bounds(bound, seq)[1], seq)

    def test_gc_bounds_two_bounds_good_seq(self):
        bounds = [30, 60]
        seq = 'GCGCTATAGCGCTATA'
        self.assertIs(trimmomatic_clone.gc_bounds(bounds, seq)[0], seq)
        self.assertIs(trimmomatic_clone.gc_bounds(bounds, seq)[1], 'loser')

    def test_gc_bounds_two_bounds_bad_seq(self):
        bounds = [30, 60]
        seq = 'ATATATATATATAT'
        self.assertIs(trimmomatic_clone.gc_bounds(bounds, seq)[0], 'loser')
        self.assertIs(trimmomatic_clone.gc_bounds(bounds, seq)[1], seq)

    def test_gc_bounds_zero_bounds(self):
        zero_bounds = []
        seq = 'GCGCTATAGCGCTATA'
        self.assertIsNone(trimmomatic_clone.gc_bounds(zero_bounds, seq))

    def test_gc_bounds_rises(self):
        more_bounds = [20, 30, 40]
        seq = 'GCGCTATAGCGCTATA'
        # вот так можно проверить, кинет ли ошибку, когда надо ее кидать
        with self.assertRaises(ValueError):
            trimmomatic_clone.gc_bounds(more_bounds, seq)

    def test_quality_assessment(self):
        quality = ';;;;;;;;;;;9;7;;.7;393333'
        scores = [26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26,
                  24, 26, 22, 26, 26, 13, 22, 26, 18, 24, 18, 18, 18, 18]
        self.assertEqual(trimmomatic_clone.assess_qscore(quality), scores)

    def test_leading(self):
        # первые три нуклеотида имеют плохое качество, проверяем, чтобы они были отброшены
        sequence = 'AAAGTTGCTTCTGGCGTGGGTGGGGGGG'
        quality = '$$$;;;;;;;;;;;9;7;;.7;393333'
        self.assertEqual(trimmomatic_clone.LEADING(26, sequence, quality),
                         sequence[3:])

    def test_trailing(self):
        # последние три нуклеотида имеют плохое качество, проверяем, чтобы они были отброшены
        sequence = 'GTTGCTTCTGGCGTGGGTGGGGGGGAAA'
        quality = ';;;;;;;;;;;9;7;;.7;393333$$$'
        self.assertEqual(trimmomatic_clone.TRAILING(10, sequence, quality),
                         sequence[:-3])

    def test_slidingwindow(self):
        sequence = 'GGGGGGAAAAAA'
        quality = ';;;;;;$$$$$$'
        self.assertEqual(trimmomatic_clone.SLIDINGWINDOW(25, 3, sequence, quality), sequence[:6])