from django.test import TestCase
from markers.models import SingleNucPol

class TestSingleNucPolModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.snp = SingleNucPol.objects.create(
            rs = 'rs1800012',
            gene_name_short = 'COL1A1', 
            gene_name_full = 'first type collagen',
            nuc_var_1 = 'C',
            nuc_var_2 = 'A',
            nuc_var_1_freq = 0.83,
            nuc_var_2_freq = 0.17,
            db_snp_link = 'https://www.ncbi.nlm.nih.gov/snp/rs1800012',

        )

    def test_singlenucpol_model(self):
        self.assertEqual(self.snp.rs, 'rs1800012')
        self.assertEqual(self.snp.gene_name_short, 'COL1A1')
        self.assertEqual(self.snp.gene_name_full, 'first type collagen')
        self.assertEqual(self.snp.nuc_var_1, 'C')
        self.assertEqual(self.snp.nuc_var_2, 'A')
        self.assertEqual(self.snp.nuc_var_1_freq, 0.83)
        self.assertEqual(self.snp.nuc_var_2_freq, 0.17)
        self.assertEqual(self.snp.db_snp_link, 'https://www.ncbi.nlm.nih.gov/snp/rs1800012')
