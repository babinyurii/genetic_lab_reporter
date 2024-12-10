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
    price = models.PositiveIntegerField(null=True, blank=True, verbose_name='цена за тест для клиники')
    #report_template = models.FileField(upload_to='report_templates/', max_length=100, default=None, blank=True, null=True)

    class Meta:
        verbose_name = 'Генетический тест'
        verbose_name_plural = '1. Генетические тесты'

    def __str__(self):
        return f'{self.name}'




class DetectionKitMarkers(models.Model):
    MARKER_CATEGORIES_IN_KIT = MARKER_CATEGORIES_IN_KIT
    ALLELE_CLIN_SIGNIF_CHOICE = ALLELE_CLIN_SIGNIF_CHOICE
    
    detection_kit = models.ForeignKey(DetectionKit,
                                      null=True, on_delete=models.SET_NULL)
    marker = models.ForeignKey(SingleNucPol,
                               null=True, on_delete=models.SET_NULL)
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
        verbose_name = 'маркеры'
        verbose_name_plural = 'Маркеры, интерпретация, заключения'
        constraints = [models.UniqueConstraint(
                        fields=['detection_kit', 'marker', ],
                        name='detection_kit_marker_constraint')]

    def __str__(self):
        return f'Генетический тест: {self.detection_kit}, маркер: {self.marker}'

