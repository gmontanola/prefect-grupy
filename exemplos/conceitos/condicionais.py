from prefect import Flow, Parameter, case, task
from prefect.tasks.control_flow import merge


@task(name="Checar condição")
def checar_par_ou_impar(result: int):
    if result % 2:
        return False
    return True


@task(name="Condição falsa")
def condicao_falsa():
    return "ÍMPAR!"


@task(name="Condição verdadeira")
def condicao_verdadeira():
    return "PAR!"


@task(name="Somar parâmetros")
def somar(a: int, b: int):
    return a + b


@task(name="Imprimir resultado", log_stdout=True)
def imprimir(valor: str):
    print(f"Sua soma é um número {valor}")


with Flow("condicionais") as flow:
    a = Parameter(name="Primeiro valor")
    b = Parameter(name="Segundo valor")
    resultado = somar(a, b)

    condicao = checar_par_ou_impar(resultado)
    with case(condicao, True):
        valor_verdadeiro = condicao_verdadeira()

    with case(condicao, False):
        valor_falso = condicao_falsa()

    valor = merge(valor_verdadeiro, valor_falso)
    imprimir(valor)

if __name__ == "__main__":
    flow.register(project_name="conceitos")
