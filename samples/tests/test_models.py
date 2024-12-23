import datetime
from django.test import TestCase
from detection_kits.models import DetectionKit, DetectionKitMarkers
from markers.models import SingleNucPol
from samples.models import (Sample,
                            SampleDetectionKit,
                             ResultSNP,)


class TestSamplesAndResults(TestCase):
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
        
        cls.sample = Sample.objects.create(
            first_name='test_first_name',
            last_name='test_last_name',
            middle_name='test_middle_name',
            age=42,
            sample_clinic_id='sample 404',
            lab_id='aa67',
            date_sampled=datetime.date(2023, 12, 31),
            date_delivered=datetime.date(2024, 1, 1),
            dna_concentration=70,
            dna_quality_260_280=1.8,
            dna_quality_260_230=2.0,
            notes='sample is not frozen',
            created_by=None,
        )


        cls.sample.genetic_tests.add(cls.detection_kit)
        cls.sample_detectionkit = SampleDetectionKit.objects.get(sample=cls.sample)
        cls.sample_detectionkit.save() # call explicitly to trigger results records generating and saving


    def test_patientsamplemodel(self):
        self.assertEqual(self.sample.first_name, 'test_first_name')
        self.assertEqual(self.sample.last_name, 'test_last_name')
        self.assertEqual(self.sample.middle_name, 'test_middle_name')
        self.assertEqual(self.sample.age, 42)
        self.assertEqual(self.sample.sample_clinic_id, 'sample 404')
        self.assertEqual(self.sample.lab_id, 'aa67')
        self.assertEqual(self.sample.date_sampled, datetime.date(2023, 12, 31))
        self.assertEqual(self.sample.date_delivered, datetime.date(2024, 1, 1))
        self.assertEqual(self.sample.dna_concentration, 70)
        self.assertEqual(self.sample.dna_quality_260_280, 1.8)
        self.assertEqual(self.sample.dna_quality_260_230, 2.0)
        self.assertEqual(self.sample.notes, 'sample is not frozen')
        self.assertEqual(self.sample.created_by, None)
        self.assertEqual(self.sample.genetic_tests.get(pk=self.sample.pk), self.detection_kit)


    
    def test_sampledetectionkit_model(self):
        detection_kit = DetectionKit.objects.get(pk=self.sample_detectionkit.genetic_test.pk)
        markers = detection_kit.linked_markers.all()

        rs_ids = []
        for marker in markers:
            rs_ids.append(marker.rs)
        # добавлять маркеры в другой список: сравнить после длину
        result_records = ResultSNP.objects.filter(sample=self.sample.pk, genetic_test=self.detection_kit.pk)
        rs_from_results_table = []
        for record in result_records:
            self.assertEqual(record.genetic_test, self.detection_kit)
            self.assertEqual(record.sample, self.sample)
            self.assertIn(record.snp.rs, rs_ids)
            rs_from_results_table.append(record.snp)
        self.assertEqual(len(rs_ids), len(rs_from_results_table))

        

