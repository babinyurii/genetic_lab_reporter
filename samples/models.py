from django.db import models
from users.models import CustomUser
from detection_kits.models import DetectionKit
from datetime import date
from django.core.validators import MinValueValidator, MaxValueValidator
from markers.models import SingleNucPol
from detection_kits.models import DetectionKitMarkers
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from samples.constants import allowed_chars
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist
from samples.utils import copy_report_template



class Sample(models.Model):
    SAMPLE_TYPES = (
                    ('commerce', 'коммерческий заказ'),
                    ('case_study', 'для  кейсов'),
                    ('marketing', 'продвижение'),
                    ('research','исследование или разработка'),
                    ('other', 'другое (укажите в комментарии к образцу'), 
                    )

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=35)
    middle_name = models.CharField(max_length=35, blank=True, null=True)
    age = models.PositiveIntegerField(validators=[MinValueValidator(1),
                                      MaxValueValidator(122)])
    sample_clinic_id = models.CharField(max_length=255, blank=True, null=True)
    lab_id = models.CharField(max_length=255, unique=True)
    sample_type = models.CharField(choices=SAMPLE_TYPES, max_length=255)
    date_sampled = models.DateField(help_text='USE CALENDAR WIDGET')
    date_delivered = models.DateField(help_text='USE CALENDAR WIDGET')
    dna_concentration = models.FloatField(validators=[MinValueValidator(0)])
    dna_quality_260_280 = models.FloatField(
                                            validators=[MinValueValidator(0.0),
                                            MaxValueValidator(3.0)])
    dna_quality_260_230 = models.FloatField(
                                            validators=[MinValueValidator(0.0),
                                            MaxValueValidator(3.0)])
    notes = models.TextField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, null=True,
                                   blank=True, on_delete=models.PROTECT)
    genetic_tests = models.ManyToManyField(DetectionKit,
                                   through='SampleDetectionKit')
    date_created = models.DateTimeField(auto_now_add=True, editable=False, )
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    class Meta:
        verbose_name = 'Образец ДНК'
        verbose_name_plural = 'Образцы ДНК'

    def clean(self):
        if not self.date_sampled or not self.date_delivered:
            raise ValidationError('please fill in both sampling and delivery dates')
            
        if self.date_sampled > date.today():
            raise ValidationError(
                 f'check sampling date: sample can not be\
                 sampled in the future. date sampled: {self.date_sampled} '
                 )
        if self.date_delivered > date.today():
            raise ValidationError(
                f'check delivery date: sample can not be\
                 delivered in the future. date delivered:\
                 {self.date_delivered}'
                 )
        if self.date_sampled > self.date_delivered:
            raise ValidationError(
                'check sampling date: sample can not be\
                 sampled after delivery date'
                 )
        for char in self.lab_id:
            if char not in allowed_chars:
                raise ValidationError(
                    'use only english characters,\
                    numbers, underscore and hyphen for lab id'
                    )



class SampleDetectionKit(models.Model):
    sample = models.ForeignKey(Sample, null=True, on_delete=models.CASCADE)
    genetic_test = models.ForeignKey(DetectionKit, null=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        kit_markers = self.genetic_test.linked_markers.all()

        for marker in kit_markers:
            if not ResultSNP.objects.filter(
                snp=marker.pk,
                genetic_test=self.genetic_test.pk,
                sample=self.sample.pk).exists():

                ResultSNP.objects.create(sample=self.sample,
                                         genetic_test=self.genetic_test,
                                         snp=marker,
                                         result=None)

    def __str__(self):
        return f'{self.genetic_test}'

    class Meta:
        verbose_name = 'Генетический тест'
        verbose_name_plural = 'Генетические тесты'
        constraints = [models.UniqueConstraint(
                       fields=['sample', 'genetic_test',],
                       name='sample_and_genetic_test_unique_constraint')]



class ResultSNP(models.Model):

    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    genetic_test = models.ForeignKey(DetectionKit, on_delete=models.CASCADE)
    snp = models.ForeignKey(SingleNucPol, on_delete=models.CASCADE)
    result = models.CharField(
                            max_length=4, blank=True, null=True,
                            help_text="use only English characters for result.\
                            USE NUCLEOTIDE ORDER DESIGNATED ABOVE")
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_modified = models.DateTimeField(auto_now=True)
    

    class Meta:
        verbose_name = 'результат'
        verbose_name_plural = 'результаты'

    def __str__(self):
        return f'генетический тест: {self.genetic_test}.  SNP: {self.snp}.  результат: {self.result}'

    def save(self, *args, **kwargs):
        update_obj = False
        if self.pk:
            update_obj = True

        super().save(*args, **kwargs)

        # not created automatically after patient creation
        if update_obj:
            results_snp = ResultSNP.objects.filter(
                genetic_test=self.genetic_test,
                    sample=self.sample)

            results = [obj.result for obj in results_snp]

            #####################################################################################3
            # NOTE: here will go report generation call, after checking if all results are ready

            if all(results):  # look for conclusion creation only when snp results are updated,
                short_report = copy_report_template(self.genetic_test.short_report_template.name,
                                    self.genetic_test.name,
                                    self.sample.last_name,
                                    self.sample.lab_id,
                                    short_report=True)

                full_report = copy_report_template(self.genetic_test.full_report_template.name,
                                    self.genetic_test.name,
                                    self.sample.last_name,
                                    self.sample.lab_id,
                                    short_report=False)
                #two_snp_conc = self.create_two_snp_report(results_snp=results_snp)
                #one_snp_conc = self.create_one_snp_report(results_snp=results_snp)

                #text = generate_text_for_conclusion(two_snp_conc, one_snp_conc)
             
                #self.create_conclusion(text=text)
        
    """
    def clean(self):
        nuc_vars = [self.snp.nuc_var_1 + self.snp.nuc_var_1,
                    self.snp.nuc_var_2 + self.snp.nuc_var_2,
                    self.snp.nuc_var_1 + self.snp.nuc_var_2,]
        if self.result not in nuc_vars:
            raise ValidationError(
                'genotype is not correct. check: only uppercase letter,\
                     look at the order of nucleotides above')
    """