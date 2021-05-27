from datetime import timedelta

import pendulum
from prefect import Flow, Parameter, task
from prefect.schedules import Schedule
from prefect.schedules.clocks import IntervalClock
from prefect.schedules.filters import between_times, is_weekday


@task(name="Relógio", log_stdout=True)
def imprimir_agendamento(alterado: bool = False):
    print(f"Essa execução ocorre a cada {4 if alterado else 13} minutos")


relogio_padrao = IntervalClock(
    start_date=pendulum.datetime(2021, 5, 27, 19, 30, tz="America/Sao_Paulo"),
    interval=timedelta(minutes=11),
)

relogio_alterado = IntervalClock(
    start_date=pendulum.datetime(2021, 5, 27, 19, 30, tz="America/Sao_Paulo"),
    interval=timedelta(minutes=3),
    parameter_defaults={"Alterado": True},
)

agendamento = Schedule(
    clocks=[relogio_padrao, relogio_alterado],
    filters=[is_weekday, between_times(pendulum.time(19), pendulum.time(23))],
)

with Flow("agendamento-avançado", schedule=agendamento) as flow:
    alterado = Parameter("Alterado", default=False, required=False)
    imprimir_agendamento(alterado)

if __name__ == "__main__":
    flow.register(project_name="extras")
