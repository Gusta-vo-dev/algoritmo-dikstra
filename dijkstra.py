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
        # PASSO 2: Fila de Prioridade (Priority Queue / Min-Heap)
        # ---------------------------------------------------------------------
        # Guardaremos tuplas no formato: (distancia_acumulada, nó)
        # O heapq sempre mantém no topo da fila (índice 0) a menor distância.
        priority_queue = [(0, start_node)]

        # Conjunto (set) para registrar nós que já foram finalizados/visitados
        visited = set()

        # ---------------------------------------------------------------------
        # PASSO 3: O Laço Principal do Algoritmo
        # ---------------------------------------------------------------------
        # Enquanto houver nós na fila para analisar:
        while priority_queue:
            # Retira da fila o nó que possui a menor distância conhecida até o momento
            current_distance, current_node = heapq.heappop(priority_queue)

            # Se esse nó já foi visitado e finalizado, nós o ignoramos
            if current_node in visited:
                continue

            # Marca o nó atual como visitado
            visited.add(current_node)

            # -----------------------------------------------------------------
            # PASSO 4: Relaxamento das Arestas (Explorar os Vizinhos)
            # -----------------------------------------------------------------
            # Itera sobre todos os vizinhos do nó atual e seus respectivos pesos
            for neighbor, weight in self.graph[current_node].items():
                
                # Se o vizinho já foi finalizado, não precisamos recalcular
                if neighbor in visited:
                    continue

                # Calcula a nova distância hipotética passando pelo 'current_node'
                distance_candidate = current_distance + weight

                # SE o caminho passando pelo nó atual for MENOR do que a distância
                # que conhecíamos anteriormente para esse vizinho:
                if distance_candidate < distances[neighbor]:
                    # Atualiza a menor distância até o vizinho
                    distances[neighbor] = distance_candidate
                    
                    # Registra que para chegar ao vizinho pelo menor caminho, viemos de current_node
                    predecessors[neighbor] = current_node
                    
                    # Adiciona o vizinho na fila de prioridade com sua nova menor distância
                    heapq.heappush(priority_queue, (distance_candidate, neighbor))

        return distances, predecessors

    def shortest_path(self, start_node, target_node):
        """
        Função auxiliar para reconstruir e retornar o caminho exato
        (lista de nós) entre start_node e target_node, além da distância total.
        """
        # Executa o algoritmo de Dijkstra
        distances, predecessors = self.dijkstra(start_node)

        # Se a distância permaneceu infinita, não existe caminho até o nó alvo
        if distances[target_node] == float('inf'):
            return None, float('inf')

        # Reconstrói o caminho fazendo o caminho inverso (de trás para frente)
        # começando pelo destino e voltando pelos predecessores até a origem
        path = []
        current = target_node
        while current is not None:
            path.append(current)
            current = predecessors[current]

        # Como montamos de trás para frente, invertemos a lista para ficar: origem -> destino
        path.reverse()

        return path, distances[target_node]


# =============================================================================
# EXEMPLO PRÁTICO DE EXECUÇÃO
# =============================================================================
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
    print(f"  Rota: {' -> '.join(path)}")
    print(f"  Custo Total: {total_dist}")
    print("=" * 60)
