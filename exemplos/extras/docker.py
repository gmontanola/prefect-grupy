import os
from prefect import Flow, task
from prefect.run_configs.docker import DockerRun
from prefect.storage.github import GitHub


@task(name="Imprimir ENNVAR", log_stdout=True)
def imprimir_variavel():
    var = os.getenv("DOCKER")
    print(f"Estou usando Docker? {var}!")


with Flow("docker", run_config=DockerRun(env={"DOCKER": "SIM"})) as flow:
    imprimir_variavel()


if __name__ == "__main__":
    flow.storage = GitHub(
        repo="gmontanola/prefect-grupy", path="/exemplos/extras/docker.py"
    )
    flow.register(project_name="extras", add_default_labels=False, labels=["docker"])
