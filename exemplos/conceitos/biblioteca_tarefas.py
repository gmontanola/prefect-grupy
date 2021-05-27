from prefect import Flow
from prefect.tasks.shell import ShellTask

pwd_task = ShellTask(name="Onde estou?", command="pwd", stream_output=True)
whoami_task = ShellTask(name="Quem sou eu?", command="whoami", stream_output=True)

with Flow("biblioteca_tarefas") as flow:
    pwd = pwd_task()
    whoami = whoami_task()

if __name__ == "__main__":
    flow.register(project_name="conceitos")
