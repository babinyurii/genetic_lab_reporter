
from django import forms
from samples.models import ResultSNP


class ResultSNPForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ResultSNPForm, self).__init__(*args, **kwargs)
        if ResultSNP.objects.filter(pk=self.instance.pk).exists():
        #if self.instance.exists():
        #if self.instance.snp.exists():
        #MyObject.objects.filter(someField=someValue).exists() # return True/False

            CHOICES = [(self.instance.snp.genotype_nuc_var_1_1,) * 2,
                        (self.instance.snp.genotype_nuc_var_1_2,) * 2,
                        (self.instance.snp.genotype_nuc_var_2_2,) * 2,]
            self.fields['result'] = forms.ChoiceField(
                choices=CHOICES)