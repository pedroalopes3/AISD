import time
from solution_pedro import BAProblem


def main():
    # Crie uma instância do BAProblem
    problem = BAProblem()

    # Defina o caminho completo para o arquivo de entrada
    file_path = "/Users/pedro/Downloads/pythonProject/data/ex109.dat"


    # Carregue o problema usando um arquivo de entrada
    try:
        with open(file_path, 'r') as file:
            problem.load(file)  # Chama load passando self automaticamente
        print("Problema carregado com sucesso!")
    except FileNotFoundError as e:
        print(f"Erro ao carregar o arquivo: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

    # Após carregar, você pode chamar outras funções de problem que usam self
    return problem  # Retorna a instância problem para ser usada fora de main


if __name__ == "__main__":
    
    start_time = time.time()
    
    # Carregar o problema
    problem_instance = main()

    # Verificar se a instância foi criada corretamente
    if problem_instance is None:
        print("Erro ao carregar o problema. Verifique o arquivo e o caminho.")
    else:
        # Imprimir informações básicas
        print(f"\nValor de N (Número de navios): {len(problem_instance.vessels)}")
        print(f"Estado inicial: {problem_instance.initial}")
        print(f"Navios: {problem_instance.vessels}")


        # Resolver o problema (se solve estiver implementado)
        solution = problem_instance.solve()
        print(f"\nSolução encontrada: {solution}")
        
        end_time = time.time()
        print(f"Execution Time: {end_time - start_time} seconds")

