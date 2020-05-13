import unittest
import trimmomatic_clone


class FastqFilterTest(unittest.TestCase):

    def test_minlen_with_good_seq(self):
        threshold = 10
        seq = 'GCGCTATAGCGCTATA'
        self.assertTrue(trimmomatic_clone.partition_by_length(seq, threshold))

    def test_minlen_bad_seq(self):
        threshold = 10
        seq = 'GCGCTATA'
        self.assertFalse(trimmomatic_clone.partition_by_length(seq, threshold))

    def test_gc_content(self):
        seq = 'GCGCTATA'
        self.assertAlmostEqual(trimmomatic_clone.gc_content(seq), 50)

    def test_gc_content_with_zero_content(self):
        seq = 'ATATATTATA'
        self.assertAlmostEqual(trimmomatic_clone.gc_content(seq), 0)

    def test_gc_bounds_one_bound_with_good_seq(self):
        bound = [30]
        seq = 'GCGCTATAGCGCTATA'
        self.assertTrue(trimmomatic_clone.gc_bounds(seq, bound))

    def test_gc_bounds_one_bound_with_bad_seq(self):
        bound = [30]
        seq = 'ATATATATATATAT'
        self.assertFalse(trimmomatic_clone.gc_bounds(seq, bound))

    def test_gc_bounds_two_bounds_with_good_seq(self):
        bounds = [30, 60]
        seq = 'GCGCTATAGCGCTATA'
        self.assertTrue(trimmomatic_clone.gc_bounds(seq, bounds))

    def test_gc_bounds_two_bounds_with_bad_seq(self):
        bounds = [30, 60]
        seq = 'ATATATATATATAT'
        self.assertFalse(trimmomatic_clone.gc_bounds(seq, bounds))

    def test_gc_bounds_without_bounds(self):
        zero_bounds = []
        seq = 'GCGCTATAGCGCTATA'
        self.assertTrue(trimmomatic_clone.gc_bounds(seq, zero_bounds))

    def test_gc_bounds_error_rise(self):
        more_bounds = [20, 30, 40]
        seq = 'GCGCTATAGCGCTATA'
        # вот так можно проверить, кинет ли ошибку, когда надо ее кидать
        with self.assertRaises(ValueError):
            trimmomatic_clone.gc_bounds(seq, more_bounds)

    def test_quality_assessment(self):
        quality = ';;;;;;;;;;;9;7;;.7;393333'
        scores = [26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26,
                  24, 26, 22, 26, 26, 13, 22, 26, 18, 24, 18, 18, 18, 18]
        self.assertEqual(trimmomatic_clone.assess_qscore(quality), scores)

    def test_leading(self):
        # первые три нуклеотида имеют плохое качество, проверяем, чтобы они были отброшены
        sequence = 'AAAGTTGCTTCTGGCGTGGGTGGGGGGG'
        quality = '$$$;;;;;;;;;;;9;7;;.7;393333'
        self.assertEqual(trimmomatic_clone.leading(26, sequence, quality),
                         sequence[3:])

    def test_trailing(self):
        # последние три нуклеотида имеют плохое качество, проверяем, чтобы они были отброшены
        sequence = 'GTTGCTTCTGGCGTGGGTGGGGGGGAAA'
        quality = ';;;;;;;;;;;9;7;;.7;393333$$$'
        self.assertEqual(trimmomatic_clone.trailing(10, sequence, quality),
                         sequence[:-3])

    def test_sliding_window(self):
        sequence = 'GGGGGGAAAAAA'
        quality = ';;;;;;$$$$$$'
        self.assertEqual(trimmomatic_clone.sliding_window([3, 25], sequence, quality), sequence[:6])

    def test_crop(self):
        n = 3
        sequence = 'AGTCACA'
        self.assertEqual(trimmomatic_clone.crop(n, sequence), 'AGT')

    def test_headcrop(self):
        n = 3
        sequence = 'AGTCACA'
        self.assertEqual(trimmomatic_clone.headcrop(n, sequence), 'CACA')

    def test_check_gc_and_len_surviving(self):
        sequence = 'ATATATATATATATAT'
        bounds = [10, 50]
        n = 0
        self.assertFalse(trimmomatic_clone.check_gc_and_len_surviving(sequence, bounds, n))
