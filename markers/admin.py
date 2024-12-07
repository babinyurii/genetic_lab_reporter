from django.contrib import admin
from django.contrib.auth import get_user_model
from markers.models import SingleNucPol


class SingleNucPolAdmin(admin.ModelAdmin):
    list_display = ('rs',
                    'gene_name_short',
                    'nuc_var_1',
                    'nuc_var_2',
                    'gene_name_full',
                    'created_by')
    list_display_links = ()
    search_fields = ('rs', 'gene_name_short', 'gene_name_full', )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "created_by":
            kwargs["queryset"] = get_user_model().objects.filter(
                username=request.user.username
            )
        return super(SingleNucPolAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    def add_view(self, request, form_url='', extra_context=None):
        data = request.GET.copy()
        data['created_by'] = request.user
        request.GET = data
        return super(SingleNucPolAdmin, self).add_view(
            request, form_url='', extra_context=extra_context
        )


admin.site.register(SingleNucPol, SingleNucPolAdmin)
