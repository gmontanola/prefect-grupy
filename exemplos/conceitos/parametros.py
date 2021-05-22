import requests
from prefect import Flow, Parameter, task


@task(name="Buscar nome", log_stdout=True)
def nome_pokemon(id: str):
    print("Quem é esse Pokémon?")
    r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{id}")
    try:
        r.raise_for_status()
        response = r.json()
        poke_name = response["name"].upper()
        print(f"É o {poke_name}!")
    except requests.exceptions.HTTPError:
        print("ID inválida")
        raise


with Flow("parametros") as flow:
    poke_id = Parameter("ID Pokémon", required=True)
    pokemon = nome_pokemon(id=poke_id)

if __name__ == "__main__":
    flow.register(project_name="conceitos")
