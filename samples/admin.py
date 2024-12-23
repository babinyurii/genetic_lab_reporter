from django.contrib import admin
from django.contrib.auth import get_user_model
from samples.models import (Sample,
                             SampleDetectionKit,
                             ResultSNP,)

from samples.forms import ResultSNPForm
from markers.models import SingleNucPol


class ResultSNPInline(admin.StackedInline):
    model = ResultSNP
    form = ResultSNPForm
    fields = ('result', )
    max_num = 0 # not to show add another button

    def has_delete_permission(self, request, obj=None):
        return False


class SampleDetectionKitInline(admin.TabularInline):
    model = SampleDetectionKit
    extra = 1


class SampleAdmin(admin.ModelAdmin):
    list_display = ('lab_id',
                    'last_name',
                    'first_name',
                    'date_sampled',
                    'date_delivered',
                    'dna_concentration',
                    'dna_quality_260_280',
                    'dna_quality_260_230',
                    'notes',
                    'created_by')
    list_display_links = ('lab_id', )
    inlines = (SampleDetectionKitInline, ResultSNPInline  )
    search_fields = ('lab_id', 'last_name',)
    search_help_text = 'Search by lab_id or last name. Case sensitive. \
        f.e. use "Иванов", not "иванов"'
    list_filter = ('genetic_tests', )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "created_by":
            kwargs["queryset"] = get_user_model().objects.filter(
                username=request.user.username
            )
        return super(SampleAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    def add_view(self, request, form_url='', extra_context=None):
        data = request.GET.copy()
        data['created_by'] = request.user
        request.GET = data
        return super(SampleAdmin, self).add_view(
            request, form_url='', extra_context=extra_context
        )



admin.site.register(Sample, SampleAdmin)
