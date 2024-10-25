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

    def actions2(self, state):
        """Gera uma lista de ações válidas considerando apenas as primeiras posições livres no cais."""
        print(f'State atual: {state}')
        all_actions = []  # Lista para armazenar as ações geradas

        # Identificar navios não alocados no estado atual (onde u == -1 e v == -1)
        not_allocated_indices = [i for i, (u, v) in enumerate(state) if u == -1]

        # Lista de navios já alocados para verificação de conflitos
        allocated_vessels = [(uj, vj, self.vessels[j]) for j, (uj, vj) in enumerate(state) if uj != -1]

        # Calcular a primeira posição livre no cais (se houver navios alocados)
        if allocated_vessels:
            # Encontrar a posição mais à direita dos navios alocados
            last_position = max(vj + sj for (uj, vj, (aj, pj, sj, wj)) in allocated_vessels)
        else:
            last_position = 0  # Se não há navios alocados, começar do início (posição 0)

        # Definir as posições de início como um conjunto para garantir valores únicos
        start_positions = [0]
        if last_position != 0:
            start_positions.append(last_position)  # Adiciona last_position apenas se for diferente de 0

        # Para cada navio não alocado, gerar ações possíveis
        for vessel_index in not_allocated_indices:
            ai, pi, si, wi = self.vessels[vessel_index]

            # Tentar encontrar três tempos de início válidos para a primeira posição livre
            valid_times = 0  # Contador de tempos válidos encontrados

            # Testar diferentes instantes de tempo para a primeira posição livre e a posição 0
            for start_position in start_positions:  # Considera apenas a posição 0 ou a primeira livre
                for start_time in range(ai, ai + 50):  # Use um range maior, mas só adiciona os 3 primeiros válidos
                    # Verificar se o tempo de início causa conflitos
                    conflito = any(
                        not (start_position + si <= vj or vj + sj <= start_position) and
                        not (start_time + pi <= uj or uj + pj <= start_time)
                        for (uj, vj, (aj, pj, sj, wj)) in allocated_vessels
                    )

                    if not conflito:
                        # Se não há conflito, adiciona a ação
                        all_actions.append((vessel_index, start_time, start_position))
                        valid_times += 1

                    # Se b == 0 e encontrou uma ação válida, parar imediatamente (inicio do processo)
                    if (len(allocated_vessels) == 0) and valid_times == 1:
                        break

                    # Parar de procurar após encontrar os três primeiros tempos válidos
                    if valid_times >= 1:
                        break


        # Ordenar as ações pelo start_time para manter uma ordem crescente de tempo
        all_actions.sort(key=lambda x: x[1])  # x[1] é start_time

        print(f'Ações geradas (considerando apenas as primeiras posições livres): {all_actions}')
        return all_actions


    def actions(self, state):
        
        # calculo dos intervalos para barcos disponiveis
        def calculate_intervals(self,berth_slots,berth_occupation,min_time,max_time):
            for t in range(min_time,max_time):
                for size in range(self.S):
                    berth_slots[size][t][0] = 0
                in_interval_prev = False
                interval_size = 0
                interval_start = 0
                interval_finish = 0
                # print(f'\ntime: {t}')
                for i in range (self.S):
                    # print(f'\nindex: {i}')
                    if berth_occupation[t][i] == 0:
                        if in_interval_prev:
                            interval_size += 1
                            # espaço de tamanho 1 há sempre
                            berth_slots[0][t][0] += 1
                            berth_slots[0][t][berth_slots[0][t][0]] = i
                            # preenche os restantes espaços disponiveis para restantes tamanhos de barco
                            for size_boat in range(2 , interval_size + 1):
                                #print(f'size_boat: {size_boat}')
                                rest = (i+1) - size_boat 
                                #print(f'rest: {rest, i, size_boat}')
                                if rest >= 0:
                                    berth_slots[size_boat-1][t][0] += 1
                                    berth_slots[size_boat-1][t][berth_slots[size_boat-1][t][0]] = rest
                        else:
                            # condição fechada
                            interval_start = i
                            in_interval_prev = True
                            interval_size += 1
                            # como o espaço é novo só tem tamanho basta alterar na matriz de tamanho 1
                            #print(f'berth: {t, i, berth_slots[0][t][0]}')
                            berth_slots[0][t][0] += 1
                            berth_slots[0][t][berth_slots[0][t][0]] = i
                    else:
                        in_interval_prev = False
                        interval_size = 0
            return berth_slots               
                        

        # # calculo dos intervalos para barcos disponiveis
        # def calculate_intervals(self,berth_slots,berth_occupation,min_time,max_time):
        #     for t in range(min_time,max_time):
        #         in_interval_prev = False
        #         interval_size = 0
        #         interval_start = 0
        #         interval_finish = 0
        #         for i in range (self.S):
        #             if berth_occupation[t][i] == 0:
        #                 if in_interval_prev:
        #                     interval_size += 1
        #                     berth_slots[t][(berth_slots[t][0]) * 2] = i    
                            
        #                     # | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 1 | 1 |
                            
        #                     # intervalo acaba
        #                     if i == self.S - 1:
        #                         interval_finish = i
        #                         for :
                                
        #                 else:
        #                     interval_start = i
        #                     in_interval_prev = True
        #                     berth_slots[t][0] = berth_slots[t][0] + 1
        #                     berth_slots[t][((berth_slots[t][0])*2)-1] = i
        #                     berth_slots[t][(berth_slots[t][0])*2] = i
                    
        #             elif in_interval_prev:
        #                 interval_finish = i - 1
        #                 in_interval_prev = False
        #     return berth_slots               
        
        # Gera uma lista de ações válidas considerando apenas as primeiras posições livres no cais
        
        
        all_actions = []  # Lista para armazenar as ações geradas
        
        # Criar a matriz de ocupação do porto (linhas = tempo, colunas = posição no cais)
        # Define um valor limite de tempo para a matriz
        sum_processing_times = sum(vessel[1] for vessel in self.vessels)
        vessel_with_max_ai = max(self.vessels, key=lambda v: v[0])
        max_ai_plus_pi = vessel_with_max_ai[0] + vessel_with_max_ai[1]
        max_time = max(sum_processing_times, max_ai_plus_pi)
 
        free_berth_sections = [self.S] * max_time  
        print(f'\n\nIn Actions\nmax time: {max_time}')
        berth_occupation = [[0] * self.S for _ in range(max_time)]  # Matriz de ocupação inicializada a 0
        berth_slots = [[[0 for _ in range((self.S * 1) + 1)] for _ in range(max_time)] for _ in range(self.S)]

        
        for vessel_index, ((start_time, start_position), (arrival_time, process_time, size, _)) in enumerate(zip(state, self.vessels)):
            if start_time != -1:  # Consider only allocated vessels
                for t in range(start_time, start_time + process_time):
                    for p in range(start_position, start_position + size):
                        berth_occupation[t][p] = vessel_index + 1  # Mark berth positions with vessel index + 1
                        free_berth_sections[t] = free_berth_sections[t] - size
                        
        berth_slots = calculate_intervals(self,berth_slots, berth_occupation, 0, max_time)
        
        # print das matrizes para debug
        
        for row in berth_occupation:  # Iterate over the 2D matrix (rows) at the current z layer
             print("  ".join(map(str, row)))  # Join the elements in each row and print without brackets or commas
        print()  # Add a blank line between layers for better readability    
        
        # for z in range(len(berth_slots)):  # Iterate over the z-axis (depth)
        #     print(f"z = {z+1}")  # Print the current z value
        #     for row in berth_slots[z]:  # Iterate over the 2D matrix (rows) at the current z layer
        #         print(" ".join(map(str, row)))  # Join the elements in each row and print without brackets or commas
        #     print()  # Add a blank line between layers for better readability

        # Identificar navios não alocados no estado atual (onde u == -1 e v == -1)
        not_allocated_indices = [i for i, (u, v) in enumerate(state) if u == -1]
        print(f'indices nao alocados: {not_allocated_indices}')

        # b número de navios alocados
        b = self.N - len(not_allocated_indices)
        b_relative = b # b relativo para correr dentro do actions
        
        
        # alocações barco a barco
        for vessel_index in not_allocated_indices:
            ai, pi, si, wi = self.vessels[vessel_index]


            # se estiver vazio navio é alocado diretamente na posição 0
            if (b_relative == 0):
                    if (si <= self.S):
                        #print(f'indice alocado na doca vazio (B = 0): {vessel_index}')
                        free_berth_sections = self.S - si
                        all_actions.append((vessel_index, ai, 0))
                        # Atualizar a matriz `berth_occupation` com a noa alocação para futuras verificações
                        # for delta in range(pi):
                        #     for delta_position in range(si):
                        #         berth_occupation[delta][delta_position] = vessel_index + 1
                        # berth_slots = calculate_intervals(self,berth_slots, berth_occupation, 0, pi)  
                        b_relative += 1 
                    # Pedro: pode-se meter clausula caso seja maior
                    
            else:
                for t in range(ai,max_time - pi + 1):  # Limitar o tempo máximo para garantir que o navio caiba sem extrapolar `max_time`
                   if berth_slots[si-1][t][0] > 0:
                       for available_slot in range(berth_slots[si-1][t][0]):
                           slot_start = berth_slots[si-1][t][available_slot + 1]
                           slot_duration = 0
                           is_valid_position = False
                           slot_dead = False
                           for slot_time in range (ai,max_time - pi):
                               slot_dead = True
                               for slot_start_rel in range(1,berth_slots[si-1][t][0] + 1):
                                   if slot_start_rel == slot_start:
                                       slot_duration += 1
                                       slot_dead = False
                                       break
                               if slot_dead:
                                   break 
                               if slot_duration == pi:
                                   is_valid_position = True                                       
                            # Se não há conflito e a posição é válida, adicionar a ação à lista
                           print(f'antes de poder ser alocado na doca (index, tempo, slot_start): {vessel_index,t,slot_start}')
                           if is_valid_position:
                               
                               all_actions.append((vessel_index, t, slot_start))
                               print(f'possivel indice alocado na doca (index, tempo, slot_start): {vessel_index}')
                                # Atualizar a matriz `berth_occupation` com a noa alocação para futuras verificações
                               for delta in range(pi):
                                 for delta_position in range(si):
                                    berth_occupation[t + delta][slot_start + delta_position] = vessel_index + 1
                               berth_slots = calculate_intervals(self,berth_slots, berth_occupation, 0, pi)     
                               b_relative += 1                                              
                           break  # Parar após encontrar um espaço válido para o navio atual
                   break
                
                    # Se já encontrou um espaço válido, não precisa verificar outros instantes de tempo
                   if len(all_actions) > 0 and all_actions[-1][0] == vessel_index:
                       break

        # Ordenar as ações pelo start_time para manter uma ordem crescente de tempo
        all_actions.sort(key=lambda x: x[1])  # x[1] é start_time

        print(f'Ações geradas (considerando apenas as primeiras posições livres): {all_actions}')
        i = False
        if not all_actions and i:
            for row in berth_occupation:  # Iterate over the 2D matrix (rows) at the current z layer
                print("  ".join(map(str, row)))  # Join the elements in each row and print without brackets or commas
            print()  # Add a blank line between layers for better readability    
        
            # for z in range(len(berth_slots)):  # Iterate over the z-axis (depth)
            #     print(f"z = {z+1}")  # Print the current z value
            #     for row in berth_slots[z]:  # Iterate over the 2D matrix (rows) at the current z layer
            #         print(" ".join(map(str, row)))  # Join the elements in each row and print without brackets or commas
            #     print()  # Add a blank line between layers for better readability

        return all_actions

    def goal_test(self, state):
        """Verifies that all vessels are correctly allocated without conflicts."""
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