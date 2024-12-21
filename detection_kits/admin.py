from django.contrib import admin
from detection_kits.models import (DetectionKit, 
                                DetectionKitMarkers,
                                TwoSNPCombination,
                                TwoSNPCombinationReport,)
                                #ConclusionsForSNP)
from markers.models import SingleNucPol

from detection_kits.forms import TwoSNPCombinationForm
from django.contrib.auth import get_user_model


class DetectionKitMarkersInline(admin.TabularInline):
    model = DetectionKitMarkers
    fields = ('marker', )
    extra = 1


class DetectionKitAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'date_created',
        'created_by',
    )

    inlines = (DetectionKitMarkersInline, )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "created_by":
            kwargs["queryset"] = get_user_model().objects.filter(
                username=request.user.username
            )
        return super(DetectionKitAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    def add_view(self, request, form_url='', extra_context=None):
        data = request.GET.copy()
        data['created_by'] = request.user
        request.GET = data
        return super(DetectionKitAdmin, self).add_view(
            request, form_url='', extra_context=extra_context
        )
"""
class ConclusionsForSNPAdmin(admin.ModelAdmin):
    readonly_fields = ('det_kit_marker', 'genotype', )
    model = ConclusionsForSNP
    list_display = (
        'det_kit_marker',
        'genotype',
        'short_conclusion',
    )
    search_fields = ('conclusion',)
    search_help_text = 'search by text in conclusion'


    list_filter = ('det_kit_marker__detection_kit',
                    'det_kit_marker__marker',
                    'det_kit_marker__marker_category_in_kit')

    def has_add_permission(self, request, obj=None):
        return False
"""

   
class DetectionKitMarkersAdmin(admin.ModelAdmin):
    fields = (
        'detection_kit',
        'marker',
        'genotype_1',
        'conclusion_genotype_1_1',
        'genotype_2',
        'conclusion_genotype_1_2',
        'genotype_3',
        'conclusion_genotype_2_2',

    )
    list_display = (
        'detection_kit',
        'marker',
        'genotype_1',
        'genotype_2',
        'genotype_3',

    )
    readonly_fields = ( 'genotype_1', 'genotype_2', 'genotype_3',)
    search_fields = ('detection_kit',)
    search_help_text = 'введите название генетического теста: найти все маркеры по вхождению в определенный тест'
    list_filter = ('detection_kit',)


    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def genotype_1(self, obj):
        return obj.marker.genotype_nuc_var_1_1

    def genotype_2(self, obj):
        return obj.marker.genotype_nuc_var_1_2

    def genotype_3(self, obj):
        return obj.marker.genotype_nuc_var_2_2



class DetectionKitMarkersAdmin(admin.ModelAdmin):
    fields = (
        'detection_kit',
        'marker',
        'genotype_1',
        'conclusion_genotype_1_1',
        'genotype_2',
        'conclusion_genotype_1_2',
        'genotype_3',
        'conclusion_genotype_2_2',

    )
    list_display = (
        'detection_kit',
        'marker',
        'genotype_1',
        'genotype_2',
        'genotype_3',

    )
    readonly_fields = ( 'genotype_1', 'genotype_2', 'genotype_3',)
    search_fields = ('detection_kit',)
    search_help_text = 'введите название генетического теста: найти все маркеры по вхождению в определенный тест'
    list_filter = ('detection_kit',)


    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def genotype_1(self, obj):
        return obj.marker.genotype_nuc_var_1_1

    def genotype_2(self, obj):
        return obj.marker.genotype_nuc_var_1_2

    def genotype_3(self, obj):
        return obj.marker.genotype_nuc_var_2_2

class TwoSNPCombinationReportInline(admin.StackedInline):
    model = TwoSNPCombinationReport
    fields = ('genotype_snp_1', 'genotype_snp_2', 'report' )
    max_num = 0 # not to show add another button
    readonly_fields = ( 'genotype_snp_1', 'genotype_snp_2',)


    def has_delete_permission(self, request, obj=None):
        return False


class TwoSNPCombinationAdmin(admin.ModelAdmin):
    form = TwoSNPCombinationForm
    list_display = ('name',
                    'detection_kits',
                    'snp_1',
                    'snp_2',)
    list_filter = ('genetic_test', )
    inlines = (TwoSNPCombinationReportInline,)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "snp_1":
            kwargs["queryset"] = SingleNucPol.objects.order_by('rs')
        if db_field.name == "snp_2":
            kwargs["queryset"] = SingleNucPol.objects.order_by('rs')

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(DetectionKitMarkers, DetectionKitMarkersAdmin)
admin.site.register(DetectionKit, DetectionKitAdmin)
admin.site.register(TwoSNPCombination, TwoSNPCombinationAdmin)

