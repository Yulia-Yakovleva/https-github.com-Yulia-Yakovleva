import unittest
import fastq_filter


class FastqFilterTest(unittest.TestCase):

    def test_gc_content(self):
        seq = 'GCGCTATA'
        self.assertAlmostEqual(fastq_filter.gc_content(seq), 50)