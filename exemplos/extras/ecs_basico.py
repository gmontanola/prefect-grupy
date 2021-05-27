from prefect import Flow
from prefect.engine.results import S3Result
from prefect.run_configs import ECSRun
from prefect.storage.github import GitHub
from prefect.tasks.shell import ShellTask

pwd_task = ShellTask(name="Onde estou?", command="pwd", stream_output=True)
whoami_task = ShellTask(name="Quem sou eu?", command="whoami", stream_output=True)


# Definição da flow
with Flow("ecs-basico", result=S3Result(bucket="prefect-grupyrp")) as flow:
    pwd = pwd_task()
    whoami = whoami_task()


if __name__ == "__main__":
    flow.run_config = ECSRun(
        cpu=512,
        memory=512,
        task_definition={
            "networkMode": "bridge",
            "containerDefinitions": [{"name": "flow"}],
        },
    )
    flow.storage = GitHub(
        repo="gmontanola/prefect-grupy", path="/exemplos/extras/ecs_basico.py"
    )
    flow.register(project_name="extras", add_default_labels=False, labels=["ecs"])
