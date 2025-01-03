# Generated by Django 5.0.6 on 2024-12-07 16:15

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SingleNucPol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rs', models.CharField(max_length=20, unique=True, verbose_name='rs id')),
                ('gene_name_short', models.CharField(max_length=20, verbose_name='short gene name')),
                ('gene_name_full', models.CharField(blank=True, max_length=255, null=True, verbose_name='full gene name')),
                ('nuc_var_1', models.CharField(choices=[('A', 'A'), ('C', 'C'), ('G', 'G'), ('T', 'T'), ('5A', '5A'), ('6A', '6A'), ('_', '_')], max_length=2, verbose_name='allele 1')),
                ('nuc_var_2', models.CharField(choices=[('A', 'A'), ('C', 'C'), ('G', 'G'), ('T', 'T'), ('5A', '5A'), ('6A', '6A'), ('_', '_')], max_length=2, verbose_name='allele 2')),
                ('nuc_var_1_freq', models.FloatField(blank=True, help_text='floating point number. f.e.: 0.5', null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)], verbose_name='allele 1 frequency in European population (from dbSNP)')),
                ('nuc_var_2_freq', models.FloatField(blank=True, help_text='floating point number. f.e.: 0.5', null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)], verbose_name='allele 2 frequency in European population (from dbSNP)')),
                ('db_snp_link', models.URLField(blank=True, help_text='LINK WILL BE OPENEDIN THE SAME TAB! BE CAREFUL', max_length=255, null=True, unique=True, validators=[django.core.validators.URLValidator], verbose_name='dbSNP link')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'SNP',
                'verbose_name_plural': 'SNPs',
            },
        ),
    ]
