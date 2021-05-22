from prefect import Flow, task
from datetime import timedelta, datetime
from prefect.schedules.schedules import IntervalSchedule


@task(name="Relógio", log_stdout=True)
def imprimir_horario():
    agora = datetime.now()
    print(f"A data e o horário de agora: {agora}")


agendamento = IntervalSchedule(interval=timedelta(minutes=5))

with Flow("agendamento", schedule=agendamento) as flow:
    imprimir_horario()

if __name__ == "__main__":
    flow.register(project_name="conceitos")
