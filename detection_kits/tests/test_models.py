import datetime
from django.test import TestCase
from detection_kits.models import (DetectionKit, 
                                   DetectionKitMarkers,
                                   TwoSNPCombination,
                                   TwoSNPCombinationReport)
from markers.models import SingleNucPol


class TestDetectionKitModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.snp_1 = SingleNucPol.objects.create(
            rs = 'rs1800012',
            gene_name_short = 'COL1A1', 
            gene_name_full = 'first type collagen',
            nuc_var_1 = 'C',
            nuc_var_2 = 'A',
            nuc_var_1_freq = 0.83,
            nuc_var_2_freq = 0.17,
            db_snp_link = 'https://www.ncbi.nlm.nih.gov/snp/rs1800012',

        )
       
        cls.snp_2 = SingleNucPol.objects.create(
            rs='rs2', gene_name_short='GENE2',
            nuc_var_1='C', nuc_var_2='T')

        cls.detection_kit = DetectionKit.objects.create(
            name='GeneKit',
            created_by=None,
        )
        cls.detection_kit.linked_markers.add(cls.snp_1) 
        cls.detection_kit.linked_markers.add(cls.snp_2) 

        cls.two_snp_comb = TwoSNPCombination.objects.create(
            name='COL1 and MMP1 report rule',
            snp_1=cls.snp_1,
            snp_2=cls.snp_2,
            note='test rule',
            genetic_test = cls.detection_kit)

        two_snp_comb_reports = TwoSNPCombinationReport.objects.filter(
            report_rule_two_snp=cls.detection_kit.report_rule.all()[0].pk
        )

        for report_comb in two_snp_comb_reports:
            report_comb.report = f'report: {report_comb.genotype_snp_1} and {report_comb.genotype_snp_2}'
            report_comb.save()



    def test_detectionkit_model(self):
        self.assertEqual(self.detection_kit.name, 'GeneKit')
        self.assertEqual(self.detection_kit.created_by, None)
        self.assertEqual(self.detection_kit.linked_markers.get(pk=self.snp_1.pk), self.snp_1)

    def test_two_snp_combination_model(self):
        self.assertEqual(self.two_snp_comb.name, 'COL1 and MMP1 report rule')
        self.assertEqual(self.two_snp_comb.snp_1.rs, 'rs1800012')
        self.assertEqual(self.two_snp_comb.snp_2.rs, 'rs2')
        self.assertEqual(self.two_snp_comb.note, 'test rule')


    def test_two_snp_combination_report_model(self):
        two_snp_comb = self.detection_kit.report_rule.all()[0]
        two_snp_comb_reports = TwoSNPCombinationReport.objects.filter(report_rule_two_snp=two_snp_comb.pk)
        self.assertEqual(len(two_snp_comb_reports), 9)

        genotypes_snp_1 = [self.snp_1.genotype_nuc_var_1_1,
                            self.snp_1.genotype_nuc_var_1_2,
                            self.snp_1.genotype_nuc_var_2_2,]
        genotypes_snp_2 = [self.snp_2.genotype_nuc_var_1_1,
                            self.snp_2.genotype_nuc_var_1_2,
                            self.snp_2.genotype_nuc_var_2_2,]

        # collect genotypes combinations from report combs objects
        genotypes_combinations = []
        for two_snp_comb_report in two_snp_comb_reports:
            genotypes_combinations.append((two_snp_comb_report.genotype_snp_1,
                                            two_snp_comb_report.genotype_snp_2,),)

        for genotype_snp_1 in genotypes_snp_1:
            for genotype_snp_2 in genotypes_snp_2:
                self.assertIn((genotype_snp_1, genotype_snp_2,), genotypes_combinations)