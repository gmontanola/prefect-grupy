from prefect import Flow, task
from prefect.tasks.secrets import PrefectSecret


@task(name="X9", log_stdout=True)
def imprimir_segredo(secret: str):
    print(f"O seu segredo é: {secret}")


with Flow("segredos") as flow:
    token = PrefectSecret(name="TOKEN_SECRETO")
    sem_segredos = imprimir_segredo(secret=token)

if __name__ == "__main__":
    flow.register(project_name="conceitos")
