from django.db import models
from users.models import CustomUser
from markers.models import SingleNucPol
from django.template.defaultfilters import truncatewords
from django.core.exceptions import ValidationError
from .constants import MARKER_CATEGORIES_IN_KIT, ALLELE_CLIN_SIGNIF_CHOICE

class DetectionKit(models.Model):

    name = models.CharField(max_length=255, unique=True)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT,
                                   null=True, blank=True)
    linked_markers = models.ManyToManyField(
                                    SingleNucPol,
                                    through='DetectionKitMarkers',
                                    related_name='detection_kits_list')
    short_report_template = models.FileField(upload_to='media/report_templates/', max_length=255, default=None, blank=True, null=True)
    full_report_template = models.FileField(upload_to='media/report_templates/', max_length=255, default=None, blank=True, null=True)

    class Meta:
        verbose_name = 'Генетический тест'
        verbose_name_plural = '1. Генетические тесты'

    def __str__(self):
        return f'{self.name}'


    def save(self, *args, **kwargs):
        try:
            detection_kit = DetectionKit.objects.get(pk=self.pk)
            if detection_kit.short_report_template and self.short_report_template and detection_kit.short_report_template != self.short_report_template:
                detection_kit.short_report_template.delete(save=False)
            if detection_kit.full_report_template and self.full_report_template and detection_kit.full_report_template != self.full_report_template:
                detection_kit.full_report_template.delete(save=False)
        except DetectionKit.DoesNotExist:
            pass

        super(DetectionKit, self).save(*args, **kwargs)






class DetectionKitMarkers(models.Model):
    MARKER_CATEGORIES_IN_KIT = MARKER_CATEGORIES_IN_KIT
    ALLELE_CLIN_SIGNIF_CHOICE = ALLELE_CLIN_SIGNIF_CHOICE
    
    detection_kit = models.ForeignKey(DetectionKit,
                                      null=True, on_delete=models.CASCADE)
    marker = models.ForeignKey(SingleNucPol,
                               null=True, on_delete=models.CASCADE)
    nuc_var_1_clin_signif = models.CharField(
                                choices=ALLELE_CLIN_SIGNIF_CHOICE,
                                max_length=24,
                                blank=True,
                                null=True,
                                default=ALLELE_CLIN_SIGNIF_CHOICE[2][1],
                                verbose_name='интерпретация аллели 1',
                                help_text="aллель 1 находится ДО знака '/' в описании маркера слева, например: G/A: аллель 1 - G"
                                )
    nuc_var_2_clin_signif = models.CharField(
                                choices=ALLELE_CLIN_SIGNIF_CHOICE,
                                max_length=24, blank=True, null=True,
                                default=ALLELE_CLIN_SIGNIF_CHOICE[2][1],
                                verbose_name='интерпретация аллели 2', 
                                help_text="aллель 2 находится ПОСЛЕ знака '/' в описании маркера слева, например: G/A: аллель 2 - А"
                                )
    marker_category_in_kit = models.CharField(choices=MARKER_CATEGORIES_IN_KIT, max_length=255, blank=True, null=True)
    conclusion_genotype_1_1 = models.TextField(null=True, blank=True, max_length=2500, verbose_name='заключение для генотипа 1')
    conclusion_genotype_1_2 = models.TextField(null=True, blank=True, max_length=2500, verbose_name='заключение для генотипа 2')
    conclusion_genotype_2_2 = models.TextField(null=True, blank=True, max_length=2500, verbose_name='заключение для генотипа 3')


    class Meta:
        verbose_name = 'SNP'
        verbose_name_plural = '2. SNP в тестах и заключения по отдельным генотипам'
        constraints = [models.UniqueConstraint(
                        fields=['detection_kit', 'marker', ],
                        name='detection_kit_marker_constraint')]

    def __str__(self):
        return f'Генетический тест: {self.detection_kit}, маркер: {self.marker}'


class TwoSNPCombination(models.Model):

    name = models.CharField(max_length=255, unique=True)
    genetic_test = models.ForeignKey(DetectionKit, related_name='report_rule', 
                                    on_delete=models.CASCADE, default=None,
                                    null=True,
                                    blank=True)
    snp_1 = models.ForeignKey(SingleNucPol, on_delete=models.CASCADE,
                              related_name='report_rules_snp_1')
    snp_2 = models.ForeignKey(SingleNucPol, on_delete=models.CASCADE,
                              related_name='report_rules_snp_2')
    note = models.TextField(max_length=1000)


    class Meta:
        verbose_name = '3. Комбинация двух SNP'

    def __str__(self):
        return f'{self.name}'

    def detection_kits(self):
        return f'{self.genetic_test.name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        genotypes_snp_1 = [self.snp_1.genotype_nuc_var_1_1,
                            self.snp_1.genotype_nuc_var_1_2,
                            self.snp_1.genotype_nuc_var_2_2,]
        genotypes_snp_2 = [self.snp_2.genotype_nuc_var_1_1,
                            self.snp_2.genotype_nuc_var_1_2,
                            self.snp_2.genotype_nuc_var_2_2,]

        genotypes_combs_in_list = []
        for genotype_snp_1 in genotypes_snp_1:
            for genotype_snp_2 in genotypes_snp_2:
                genotypes_combs_in_list.append((genotype_snp_1, genotype_snp_2))

        report_combinations = TwoSNPCombinationReport.objects.filter(
            report_rule_two_snp=self).order_by('pk')
        if report_combinations:
            comb_counter = 0
            for report_comb in report_combinations:
                report_comb.genotype_snp_1 = genotypes_combs_in_list[
                                            comb_counter][0]
                report_comb.genotype_snp_2 = genotypes_combs_in_list[
                                            comb_counter][1]
                report_comb.save()
                comb_counter += 1
        else:
            for genotype_snp_1 in genotypes_snp_1:
                for genotype_snp_2 in genotypes_snp_2:

                    TwoSNPCombinationReport.objects.create(
                            report_rule_two_snp=self,
                            genotype_snp_1=genotype_snp_1,
                            genotype_snp_2=genotype_snp_2
                            )


class TwoSNPCombinationReport(models.Model):
    report_rule_two_snp = models.ForeignKey(TwoSNPCombination,
                                            on_delete=models.CASCADE)
    genotype_snp_1 = models.CharField(max_length=2, blank=True, null=True)
    genotype_snp_2 = models.CharField(max_length=2, blank=True, null=True)
    report = models.TextField(max_length=10000, blank=True, null=True)

    class Meta:
        verbose_name = 'заключение по двум генотипам'
        verbose_name_plural = 'заключения по двум генотипам'

    def __str__(self):
        return self.report_rule_two_snp.name

