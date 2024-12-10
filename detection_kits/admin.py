from django.contrib import admin
from detection_kits.models import (DetectionKit, 
                                DetectionKitMarkers, )
                                #ConclusionsForSNP)
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
    list_display = (
        'detection_kit',
        'marker',
    )
    search_fields = ('detection_kit',)
    search_help_text = 'введите название генетического теста: найти все маркеры по вхождению в определенный тест'
    list_filter = ('detection_kit',)


    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False




admin.site.register(DetectionKitMarkers, DetectionKitMarkersAdmin)
admin.site.register(DetectionKit, DetectionKitAdmin)
#admin.site.register(ConclusionsForSNP, ConclusionsForSNPAdmin)