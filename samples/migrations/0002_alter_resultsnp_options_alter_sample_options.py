# Generated by Django 5.0.6 on 2024-12-23 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='resultsnp',
            options={'verbose_name': 'результат', 'verbose_name_plural': 'результаты'},
        ),
        migrations.AlterModelOptions(
            name='sample',
            options={'verbose_name': 'Образец ДНК', 'verbose_name_plural': 'Образцы ДНК'},
        ),
    ]