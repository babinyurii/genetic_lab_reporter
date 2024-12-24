import shutil
from django.conf import settings
import os
from datetime import date




def copy_report_template(report_template, genetic_test_name, last_name, lab_id):
    source = report_template
    print('source: ', source)
    if not os.path.exists(f'{settings.BASE_DIR}/media/results/{genetic_test_name}'):
        os.mkdir(f'{settings.BASE_DIR}/media/results/{genetic_test_name}')
    
    results_report_name = f'{lab_id}_{last_name}_date_created_{date.today():%m_%d_%Y}.pdf'
    destination = f'{settings.BASE_DIR}/media/results/{genetic_test_name}/{results_report_name}'
    print('destination: ', destination)

    shutil.copyfile(source, destination)
