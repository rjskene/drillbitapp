from celery import shared_task

from .serializers import ProjectStatementSerializer

@shared_task()
def create_statement_for_given_frequency(environment, project, frequency):
    data = {
        'environment': environment, 
        'project': project, 
        'frequency': frequency
    }
    ser = ProjectStatementSerializer(data=data)
    ser.is_valid()
    ser.save()

def create_statements_for_given_project(environment, project):
    frequencies = ['M', 'Q', 'A']
    tasks = []
    for frequency in frequencies:
        task = create_statement_for_given_frequency.delay(environment, project, frequency)
        tasks.append(task)

    return {f: t.id for f, t in zip(frequencies, tasks)}