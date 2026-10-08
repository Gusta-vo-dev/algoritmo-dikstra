"""
=============================================================================
ALGORITMO DE DIJKSTRA EM PYTHON
Referência: Tutorial DataCamp (Implementando o algoritmo Dijkstra em Python)
Disciplina: Estrutura de Dados II
=============================================================================

O que é o Algoritmo de Dijkstra?
--------------------------------
É um algoritmo "guloso" (greedy) criado pelo cientista da computação Edsger Dijkstra.
Objetivo: Encontrar o caminho mais curto (de menor custo/peso) a partir de um vértice
de origem (nó inicial) para todos os outros vértices em um grafo com arestas de
pesos NÃO-NEGATIVOS.

Conceitos Fundamentais:
1. Vértice (Nó): Um ponto no grafo (ex: cidades 'A', 'B', 'C').
2. Aresta: Uma ligação entre dois nós (ex: estrada entre 'A' e 'B').
3. Peso: O custo para percorrer aquela aresta (ex: distância em km, pedágio, tempo).
4. Fila de Prioridade (Min-Heap): Estrutura de dados que sempre nos entrega o elemento
   com menor valor rapidamente (complexidade O(log n)).
=============================================================================
"""

import heapq  # Módulo nativo do Python para fila de prioridade (Min-Heap)


class Graph:
    """
    Classe para representar o Grafo usando Lista de Adjacência.
    Em Python, usamos um dicionário (dict) onde:
    - Chave: Nome do nó (ex: 'A')
    - Valor: Outro dicionário com os vizinhos e os pesos das arestas
             (ex: {'B': 4, 'C': 2})
    """

    def __init__(self):
        """
        Método construtor: executado automaticamente ao criar um objeto Graph().
        'self' representa a própria instância da classe.
        """
        # Inicializa o dicionário vazio que guardará o grafo
        self.graph = {}

    def add_edge(self, u, v, weight, bidirectional=True):
        """
        Adiciona uma aresta (ligação com peso) entre o nó 'u' e o nó 'v'.
        
        Parâmetros:
        - u: Nó de origem
        - v: Nó de destino
        - weight: Peso (distância/custo) da aresta
        - bidirectional: Se True, a aresta vai nos dois sentidos (grafo não-direcionado).
        """
        # Se o nó 'u' ainda não foi registrado no dicionário, cria uma entrada para ele
        if u not in self.graph:
            self.graph[u] = {}
        # Associa o vizinho 'v' ao peso da aresta
        self.graph[u][v] = weight

        # Se for bidirecional, também conectamos 'v' até 'u'
        if bidirectional:
            if v not in self.graph:
                self.graph[v] = {}
            self.graph[v][u] = weight

    def dijkstra(self, start_node):
        """
        Executa o Algoritmo de Dijkstra a partir de um nó de início ('start_node').
        
        Retorna:
        - distances: Dicionário com a menor distância de 'start_node' até cada nó.
        - predecessors: Dicionário que guarda quem veio antes no menor caminho
                        (essencial para reconstruir a rota depois).
        """
        # ---------------------------------------------------------------------
        # PASSO 1: Inicialização das Distâncias e Predecessores
        # ---------------------------------------------------------------------
        # Inicializamos a distância para todos os nós como "infinito" (float('inf')),
        # porque ainda não descobrimos nenhum caminho até eles.
        distances = {node: float('inf') for node in self.graph}
        
        # A distância do nó de início para ele mesmo é SEMPRE 0!
        distances[start_node] = 0

        # Predecessores: guarda qual nó nos levou ao nó atual no menor caminho
        predecessors = {node: None for node in self.graph}

        # ---------------------------------------------------------------------
        # PASSO 2: Fila de Prioridade (Priority Queue / Min-Heap) e Visitados
        # ---------------------------------------------------------------------
        # O que é uma Fila de Prioridade?
        # É uma fila inteligente: em vez de atender quem chegou primeiro (FIFO),
        # ela sempre atende quem tem a MENOR DISTÂNCIA primeiro!
        #
        # No Python, usamos tuplas no formato: (distancia, nome_do_nó).
        # Por que colocar a distância primeiro na tupla?
        # Porque quando o Python compara duas tuplas, ele sempre olha o primeiro item!
        # Exemplo: (2, 'C') vem antes de (4, 'B') porque 2 é menor que 4.
        #
        # Começamos colocando apenas o nó de partida: distância 0 até 'start_node'.
        priority_queue = [(0, start_node)]

        # 'visited' é um CONJUNTO (set em Python).
        # Para que serve? Guardar os nós cuja menor distância JÁ FOI DEFINITIVAMENTE ENCONTRADA.
        # Um conjunto (set) é perfeito aqui porque verificar "se algo está dentro" (x in visited)
        # é instantâneo em Python (complexidade O(1)).
        visited = set()

        # ---------------------------------------------------------------------
        # PASSO 3: O Laço Principal do Algoritmo (Processamento dos Nós)
        # ---------------------------------------------------------------------
        # 'while priority_queue:' significa:
        # "Enquanto a lista priority_queue NÃO estiver vazia, continue repetindo".
        while priority_queue:

            # 'heapq.heappop()' retira e devolve o menor elemento da fila (o topo do min-heap).
            # Como guardamos tuplas (distancia, nó), usamos duas variáveis para receber os valores:
            # - current_distance: recebe o número da distância
            # - current_node: recebe o nome do nó (ex: 'A', 'B', ...)
            current_distance, current_node = heapq.heappop(priority_queue)

            # O Dijkstra garante que na primeira vez que retiramos um nó da fila,
            # a distância dele já é a menor possível definitiva!
            # Mas, se o mesmo nó foi inserido mais de uma vez na fila com distâncias
            # diferentes no passado, nós ignoramos as cópias velhas com este 'if':
            if current_node in visited:
                continue  # 'continue' pula direto para a próxima repetição do while

            # Se não foi visitado ainda, agora nós o marcamos como visitado!
            visited.add(current_node)

            # -----------------------------------------------------------------
            # PASSO 4: Relaxamento das Arestas (Explorar os Vizinhos)
            # -----------------------------------------------------------------
            # O que é "Relaxamento"?
            # É o ato de testar se passar pelo nó atual ('current_node') oferece
            # um atalho mais curto para chegar aos vizinhos dele.
            #
            # O método .items() em um dicionário devolve pares (chave, valor).
            # Aqui:
            # - 'neighbor': é o nome do vizinho (chave)
            # - 'weight': é o peso da aresta entre o nó atual e esse vizinho (valor)
            for neighbor, weight in self.graph[current_node].items():
                
                # Se o vizinho já foi visitado e finalizado com sua rota ótima,
                # não precisamos recalcular nada para ele. Pula para o próximo vizinho!
                if neighbor in visited:
                    continue

                # CÁLCULO DO ATALHO:
                # Distância para chegar até aqui (current_distance) + custo da aresta até o vizinho (weight)
                distance_candidate = current_distance + weight

                # COMPARAÇÃO FUNDAMENTAL:
                # "O caminho novo (distance_candidate) é MENOR do que a distância
                # que tínhamos anotada até agora para esse vizinho?"
                if distance_candidate < distances[neighbor]:
                    # 1. Atualizamos a tabela com a nova menor distância descoberta:
                    distances[neighbor] = distance_candidate
                    
                    # 2. Anotamos o predecessor: para chegar nesse vizinho pelo melhor caminho,
                    # o passo anterior foi obrigatoriamente o 'current_node'!
                    predecessors[neighbor] = current_node
                    
                    # 3. Adicionamos esse vizinho na fila de prioridade com o novo custo,
                    # usando 'heapq.heappush' para manter a fila sempre ordenada pelo menor valor:
                    heapq.heappush(priority_queue, (distance_candidate, neighbor))

        # Quando a fila esvaziar, o algoritmo terminou para todos os nós alcançáveis.
        # Retornamos os dois dicionários com os resultados.
        return distances, predecessors

    def shortest_path(self, start_node, target_node):
        """
        Função auxiliar para reconstruir e retornar o caminho exato
        (lista com a sequência de nós) entre start_node e target_node, além do custo total.
        
        Como funciona a reconstrução?
        Fazemos uma técnica chamada BACKTRACKING (andar de trás para frente):
        Começamos no nó de destino ('target_node') e vamos perguntando:
        "Quem é o seu predecessor?" até chegar no nó de origem ('start_node').
        """
        # 1. Executa o algoritmo de Dijkstra a partir da origem
        distances, predecessors = self.dijkstra(start_node)

        # 2. Se a distância até o alvo permaneceu infinito, significa que
        # o grafo é desconexo e não há estrada/ligação até o destino!
        if distances[target_node] == float('inf'):
            return None, float('inf')

        # 3. Reconstrói o caminho de trás para frente
        path = []
        current = target_node  # Começamos pelo destino
        
        # Enquanto não chegamos na origem (cujo predecessor é None):
        while current is not None:
            path.append(current)          # Adiciona o nó na lista
            current = predecessors[current]  # Dá um passo para trás usando o predecessor

        # Como guardamos de trás para frente (ex: ['D', 'E', 'C', 'A']),
        # usamos path.reverse() para inverter a lista e ficar na ordem correta:
        # ['A', 'C', 'E', 'D']
        path.reverse()

        return path, distances[target_node]


# =============================================================================
# EXEMPLO PRÁTICO DE EXECUÇÃO
# =============================================================================
# Esta linha abaixo verifica se o arquivo está sendo executado diretamente
# (por exemplo: 'python dijkstra.py') e não apenas importado por outro código.
if __name__ == "__main__":
    print("=" * 60)
    print("DEMONSTRAÇÃO DO ALGORITMO DE DIJKSTRA (Estilo DataCamp)")
    print("=" * 60)

    # 1. Criação da instância do Grafo
    g = Graph()

    # 2. Adicionando as arestas com seus pesos
    # Imagine que são cidades e a distância em km:
    # A - (4) - B
    # A - (2) - C
    # B - (5) - C
    # B - (10) - D
    # C - (3) - E
    # E - (4) - D
    # D - (11) - F
    g.add_edge('A', 'B', 4)
    g.add_edge('A', 'C', 2)
    g.add_edge('B', 'C', 5)
    g.add_edge('B', 'D', 10)
    g.add_edge('C', 'E', 3)
    g.add_edge('E', 'D', 4)
    g.add_edge('D', 'F', 11)

    print("\nEstrutura do Grafo (Lista de Adjacência):")
    # Percorre cada nó e mostra com quem ele se conecta:
    for node, neighbors in g.graph.items():
        print(f"  Nó '{node}' conecta com: {neighbors}")

    # 3. Calculando distâncias a partir do nó 'A'
    start = 'A'
    print(f"\nCalculando menores distâncias a partir do nó '{start}'...")
    distances, predecessors = g.dijkstra(start)

    print("\n--- Menores Distâncias a partir de 'A' ---")
    for node, dist in distances.items():
        print(f"  Distância até '{node}': {dist}")

    # 4. Buscando o caminho mais curto específico de 'A' até 'D'
    target = 'D'
    path, total_dist = g.shortest_path(start, target)

    print(f"\n--- Caminho Mais Curto de '{start}' até '{target}' ---")
    # ' -> '.join(path) junta os itens da lista com setinhas: "A -> C -> E -> D"
    print(f"  Rota: {' -> '.join(path)}")
    print(f"  Custo Total: {total_dist}")
    print("=" * 60)
