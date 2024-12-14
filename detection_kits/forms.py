from django import forms
from django.core.exceptions import ValidationError
from detection_kits.models import TwoSNPCombination


class TwoSNPCombinationForm(forms.ModelForm):

    class Meta:
        model = TwoSNPCombination
        fields = ('name', 'snp_1', 'snp_2', 'genetic_test')
        widgets = {
            'genetic_test': forms.RadioSelect(),
        }

    def clean(self):
        data = self.cleaned_data
        snp_1 = data.get('snp_1')
        snp_2 = data.get('snp_2')
        snps = [snp_1, snp_2]
        genetic_test = data.get('genetic_test')

        if snp_1 == snp_2:
            raise ValidationError(f'field snp_1 {snp_1} and field snp_2 \
                {snp_2} are the same. Choose different markers')
        if not genetic_test:
            raise ValidationError('choose genetic test')
        if not self.instance.pk:
            if TwoSNPCombination.objects.filter(
                snp_1=snp_1, snp_2=snp_2, genetic_test=genetic_test).exists() or \
                TwoSNPCombination.objects.filter(
                    snp_1=snp_2, snp_2=snp_1, genetic_test=genetic_test).exists():
                raise ValidationError(
                    f'the database already has the record with the kit:\
                            "{genetic_test}",  snp 1:  "{snp_1}",  snp 2:  "{snp_2}"')

            for snp in snps:
                if not genetic_test.linked_markers.filter(rs=snp.rs).exists():
                    raise ValidationError(
                        f'snp : "{snp}" is not in the kit: "{genetic_test}"')

        return data