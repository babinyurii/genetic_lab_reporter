# Generated by Django 5.0.6 on 2024-12-23 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detection_kits', '0007_detectionkit_short_report_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detectionkit',
            name='short_report_template',
            field=models.FileField(blank=True, default=None, max_length=255, null=True, upload_to='media/report_templates/'),
        ),
    ]
