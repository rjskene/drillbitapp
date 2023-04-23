from celery import shared_task

from .serializers import ProjectStatementSerializer

"""
WARNING!!!!

watchmedo has an error with python 3.9 that prevents it from reloading celery properly
if changes are made here, celery must be manually restarted
"""

@shared_task()
def create_statement_for_given_frequency(sim_id, frequency):
    data = {
        'sim': sim_id, 
        'frequency': frequency
    }
    ser = ProjectStatementSerializer(data=data)
    ser.is_valid()
    ser.save()

def create_statements_for_given_project(sim_id):
    frequencies = ['H', 'D', 'M', 'Q', 'A']
    tasks = []
    for frequency in frequencies:
        task = create_statement_for_given_frequency.delay(sim_id, frequency)
        tasks.append(task)

    return {f: t.id for f, t in zip(frequencies, tasks)}