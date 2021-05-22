import prefect
from prefect import Flow, task


@task(name="Enviar salve")
def dar_um_salve():
    logger = prefect.context.get("logger")
    logger.info("Salve pessoal!")


with Flow("primeira-flow") as flow:
    dar_um_salve()

if __name__ == "__main__":
    flow.register(project_name="grupy-rp-básico")
