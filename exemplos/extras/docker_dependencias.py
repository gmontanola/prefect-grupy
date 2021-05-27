from io import StringIO
from typing import Any, Dict, List

import pandas as pd
import pendulum
import requests
from prefect import Flow, Parameter, task
from prefect.engine.results import S3Result
from prefect.run_configs.docker import DockerRun
from prefect.storage.github import GitHub
from prefect.tasks.aws.s3 import S3Upload
from prefect.tasks.secrets import PrefectSecret

# Data para nome do arquivo
data = pendulum.now(tz="UTC").strftime("%Y%m%d_%H%M%S")

# Criando tarefas personalizadas
@task(name="Buscar personagens")
def fetch_characters() -> List[Dict[str, Any]]:
    characters = []
    page = "https://rickandmortyapi.com/api/character"
    with requests.Session() as session:
        while page:
            r = session.get(page)
            content = r.json()
            characters.append(content["results"])
            page = content["info"]["next"]

    return characters


@task(name="Criar CSV")
def build_csv(source: List[Dict]) -> str:
    source_df = pd.concat([pd.json_normalize(page) for page in source])
    str_buffer = StringIO()

    df = (
        source_df.loc[:, ~source_df.columns.str.contains("url")]
        .drop(["image", "episode"], axis="columns")
        .set_index("id")
    )

    df.to_csv(str_buffer)
    csv_string = str_buffer.getvalue()

    return csv_string


# Instanciar tarefas da biblioteca do Prefect
s3_upload = S3Upload(name="Upload")

# Definição da flow
with Flow("docker-dependencias", result=S3Result(bucket="prefect-grupyrp")) as flow:
    bucket = Parameter("Nome do bucket", required=True)
    credenciais_aws = PrefectSecret("AWS_CREDENTIALS")
    personagens = fetch_characters()
    dados = build_csv(source=personagens)
    csv_upload = s3_upload(
        data=dados,
        bucket=bucket,
        credentials=credenciais_aws,
        key=f"rick_and_morty/{data}_characters.csv",
    )

if __name__ == "__main__":
    flow.run_config = DockerRun(
        env={"EXTRA_PIP_PACKAGES": "pandas requests prefect[aws]"}
    )
    flow.storage = GitHub(
        repo="gmontanola/prefect-grupy", path="/exemplos/extras/docker_dependencias.py"
    )
    flow.register(project_name="extras", add_default_labels=False, labels=["docker"])
