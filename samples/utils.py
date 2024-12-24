import shutil
from django.conf import settings
import os
from datetime import date




def copy_report_template(report_template, genetic_test_name, last_name, lab_id, short_report):

    source = report_template
    if not os.path.exists(f'{settings.BASE_DIR}/media/results/{genetic_test_name}'):
        os.mkdir(f'{settings.BASE_DIR}/media/results/{genetic_test_name}')
    if short_report:
        report_type = 'short_report'
    else:
        report_type = 'full_report'
        
    results_report_name = f'{lab_id}_{last_name}_{report_type}_created_{date.today():%m_%d_%Y}.pdf'
    destination = f'{settings.BASE_DIR}/media/results/{genetic_test_name}/{results_report_name}'

    return shutil.copyfile(source, destination)
