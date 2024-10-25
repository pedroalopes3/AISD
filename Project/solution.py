import search
from search import uniform_cost_search
class BAProblem(search.Problem):
    def __init__(self):
        """Method that initializes the class with the initial state."""
        self.initial = None  # Inicialização do estado inicial como 'None' ou conforme o valor passado
        self.S = None  # Tamanho do espaço de atracação
        self.N = None  # Número de embarcações
        self.vessels = []  # Lista para armazenar as informações das embarcações (ai, pi, si, wi)

    def result(self, state, action):
        """Returns the state that results from executing the given action
        in the given state"""
        navio_index, start_time, start_position = action
        print(f'refebeu esta ação {action}')

        # Criar uma cópia do estado atual para não modificar o original
        new_state = list(state)  # Converte para lista para permitir modificações
        new_state[navio_index] = (start_time, start_position)
        # Converter o novo estado de volta para tupla
        print(f'entregou este estado {new_state}')
        return tuple(new_state)

    def actions(self, state):
        """Gera uma lista de ações válidas considerando apenas as primeiras posições livres no cais."""
        print(f'State atual: {state}')
        all_actions = []  # Lista para armazenar as ações geradas

        # Criar a matriz de ocupação do porto (linhas = tempo, colunas = posição no cais)
        max_time = 500  # Define um valor limite de tempo para a matriz
        berth_occupation = [[0] * self.S for _ in range(max_time)]  # Matriz de ocupação inicializada a 0

        # Preencher a matriz com os navios já alocados
        for (start_time, start_position), (arrival_time, process_time, size, _) in zip(state, self.vessels):
            if start_time != -1:  # Verificar apenas navios alocados
                for t in range(start_time, start_time + process_time):
                    for p in range(start_position, start_position + size):
                        berth_occupation[t][p] = 1  # Marcar posições ocupadas no cais
                        if t < max_time and p < self.S:  # Garantir que não ultrapassamos os limites
                            berth_occupation[t][p] = 1  # Marcar posições ocupadas no cais
        print(f'Matriz (considerando apenas as primeiras posições livres): {berth_occupation}')



        # Identificar navios não alocados no estado atual (onde u == -1 e v == -1)
        not_allocated_indices = [i for i, (u, v) in enumerate(state) if u == -1]

        # b número de navios alocados
        b = self.S - len(not_allocated_indices)
        print(f'b = {b}')

        for vessel_index in not_allocated_indices:
            ai, pi, si, wi = self.vessels[vessel_index]

            if (b == -1):
                print(f'b = 0')
                if (si <= self.S):
                    all_actions.append((vessel_index, ai, 0))
            else:
                previous_occupation_row = None  # Para verificar se a linha da matriz de ocupação mudou

                # Percorrer cada instante de tempo (`t`) na matriz `berth_occupation`
                for t in range(min(max_time - pi + 1, max_time)):  # Limitar o tempo máximo para garantir que o navio caiba
                    # sem extrapolar `max_time`
                    # Verificar se a linha da matriz de ocupação mudou em relação ao tempo anterior
                    current_occupation_row = berth_occupation[t]
                    if previous_occupation_row is not None and current_occupation_row == previous_occupation_row:
                        # Pular este tempo se a ocupação não mudou assim evito colocar ações iguais mas com mais tempo
                        continue
                    previous_occupation_row = current_occupation_row

                    for start_position in range(self.S - si + 1):  # Verificar cada posição inicial no cais
                        # Verificar se a posição `start_position` está livre para todo o comprimento do navio (`si`)
                        is_valid_position = True
                        for delta in range(pi):
                            for delta_position in range(si):
                                # Check for space conflicts
                                if berth_occupation[t + delta][start_position + delta_position] == 1:
                                    is_valid_position = False
                                    break
                                # Check if it's out of the matrix boundaries
                                if t + delta >= max_time or start_position + delta_position >= self.S:
                                    is_valid_position = False
                                    break

                        # Se a posição for válida, vamos verificar se a posição à esquerda ou à direita tem um navio
                        # Se está no início do porto ou no fim
                        if is_valid_position:
                            if start_position == 0:  # Colado ao início do porto
                                all_actions.append((vessel_index, t, start_position))
                                break
                            elif berth_occupation[t][start_position - 1] == 1:  # Colado à esquerda a um navio já alocado
                                all_actions.append((vessel_index, t, start_position))
                                break
                            elif(start_position + si +1 < self.S):
                                if berth_occupation[t][start_position + si +1] == 1:
                                    all_actions.append((vessel_index, t, start_position))
                                    break
                            elif ((start_position + si) == self.S):
                                all_actions.append((vessel_index, t, start_position))
                                break



                    # Se já encontrou um espaço válido, não precisa verificar outros instantes de tempo
                    if len(all_actions) > 0 and all_actions[-1][0] == vessel_index:
                        break

        print(f'na função actions{all_actions}')
        # Ordenar as ações pelo start_time para manter uma ordem crescente de tempo
        all_actions.sort(key=lambda x: x[1])  # x[1] é start_time

        return all_actions

    def goal_test(self, state):
        """Verifies that all vessels are correctly allocated without conflicts."""
        if len(state) != self.N:
            print(f"Erro: o número de navios no estado ({len(state)}) é diferente de self.N ({self.N})")
            return False

        for i, (ui, vi) in enumerate(state):
            ai, pi, si, wi = self.vessels[i]

            # Early rejection of invalid states
            if ui == -1 or vi == -1 or ai > ui or vi + si > self.S:
                return False

            # Check for conflicts with other vessels
            for j in range(i + 1, len(state)):
                uj, vj = state[j]
                aj, pj, sj, wj = self.vessels[j]

                # Skip unallocated vessels
                if uj == -1:
                    continue

                # Check for spatial and temporal overlap
                if not (vi + si <= vj or vj + sj <= vi):
                    if not (ui + pi <= uj or uj + pj <= ui):
                        return False

        return True

    def path_cost(self, c, state1, action, state2):
        """Returns the cost of a path that arrives at state2 from state1
        via action, assuming cost c to get up to state1"""
        print(f'dentro do path cost state1  {state1}  --state2 {state2}')

        # Descompactar a ação (índice do navio, tempo de início, posição inicial)
        navio_index, start_time, start_position = action

        # Obter as informações do navio a partir de self.vessels
        arrival_time, processing_time, vessel_size, weight = self.vessels[navio_index]

        # Calcular o tempo de espera para o navio
        # Tempo de espera é o tempo entre a chegada e o início do processamento

        flow_time = (start_time + processing_time) - arrival_time
        additional_cost = flow_time * weight

        # Custo total acumulado é o custo atual + custo adicional
        total_cost = c + additional_cost

        print(f'dentro do path cost add {additional_cost} - total {total_cost}')
        return total_cost


    def solve(self):
        solution_node = uniform_cost_search(self)
        if solution_node:
            print(f"Nó da solução encontrado: {solution_node}")
            actions = solution_node.solution()
            print(f"Ações da solução: {actions}")
            final_state = list(self.initial)
            for action in actions:
                navio_index, start_time, start_position = action
                final_state[navio_index] = (start_time, start_position)
            print(f"Estado final após aplicar as ações: {final_state}")
            if self.goal_test(tuple(final_state)):
                print(f"Solução encontrada e válida: {final_state}")
                return [(start_time, start_position) for (start_time, start_position) in final_state]
            else:
                print("Solução encontrada, mas não é válida.")
                return []
        else:
            print("Nenhuma solução encontrada.")
            return []

    def load(self, fh):
        """Loads a BAP problem from the file object fh and initializes self.initial."""
        try:
            lines = fh.readlines()

            # Para retirar as primeiras linhas de comentário se existirem
            config_lines = [line.strip() for line in lines if line.strip() and not line.startswith('#')]

            if len(config_lines) == 0:
                print("File is empty or contains only comments.")  # Mensagem de erro se o ficheiro estiver vazio
                return

            # A primeira linha tem S (berth space size) e N (number of vessels)
            self.S, self.N = map(int, config_lines[0].split())

            # Passar a informação de cada navio para o self (ai, pi, si, wi)
            for i in range(1, self.N + 1):
                ai, pi, si, wi = map(int, config_lines[i].split())
                self.vessels.append((ai, pi, si, wi))

        except Exception as e:
            raise ValueError(f"An error occurred: {e}")

        # Inicializar o estado inicial como uma lista de (None, None) para cada navio
        self.initial = tuple([(-1, -1) for _ in range(self.N)])