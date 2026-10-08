import heapq

def dijkstra_ponto_a_ponto(grafo, inicio, fim):
    """
    Calcula a menor distância e o caminho percorrido entre um ponto de origem e um de destino.
    """
    # Validação rápida de existência dos nós
    if inicio not in grafo or fim not in grafo:
        return None, []

    distancias = {vertice: float('inf') for vertice in grafo}
    distancias[inicio] = 0
    
    # Dicionário para rastrear o caminho (predecessores)
    anteriores = {vertice: None for vertice in grafo}
    
    # Fila de prioridades: (distância acumulada, vértice atual)
    fila_prioridade = [(0, inicio)]

    # Indica se já chegamos ao destino (usado para encerrar o laço)
    chegou_ao_destino = False

    # O laço continua enquanto houver vértices na fila e o destino não tiver sido alcançado
    while fila_prioridade and not chegou_ao_destino:
        distancia_atual, vertice_atual = heapq.heappop(fila_prioridade)

        # Parada antecipada: se chegamos ao destino, marcamos para o laço terminar
        if vertice_atual == fim:
            chegou_ao_destino = True

        # Só analisa os vizinhos se esta for a menor distância conhecida para o vértice
        elif distancia_atual <= distancias[vertice_atual]:
            for vizinho, peso in grafo[vertice_atual].items():
                distancia_nova = distancia_atual + peso

                if distancia_nova < distancias[vizinho]:
                    distancias[vizinho] = distancia_nova
                    anteriores[vizinho] = vertice_atual
                    heapq.heappush(fila_prioridade, (distancia_nova, vizinho))
                
    # Reconstrução do caminho percorrido do destino de volta até a origem
    caminho = []
    atual = fim
    while atual is not None:
        caminho.append(atual)
        atual = anteriores[atual]
    caminho.reverse()
    
    # Caso não exista rota conectando os dois pontos
    if distancias[fim] == float('inf'):
        return float('inf'), []
        
    return distancias[fim], caminho


# Exemplos de uso interativo
if __name__ == "__main__":
    grafo = {
        "RS": {"TA": 7, "RO": 5, "TC": 4, "LO": 2, "PG": 6, "PR": 9, "IB": 5, "IT": 8},
        "TA": {"LA": 4, "SA": 5, "AG": 9, "RS": 7, "PR": 12},
        "LA": {"TA": 4, "RO": 3},
        "SA": {"TA": 5, "TC": 6},
        "RO": {"LA": 3, "AG": 4, "RS": 5, "IT": 14},
        "TC": {"SA": 6, "RS": 4, "LO": 3, "IT": 11},
        "AG": {"TA": 9, "RO": 4, "WI": 6, "IB": 10},
        "LO": {"TC": 3, "RS": 2, "PG": 4, "IB": 8},
        "PG": {"LO": 4, "RS": 6, "VR": 3, "PR": 13, "IB": 7},
        "WI": {"AG": 6, "AU": 2, "PR": 5, "IB": 6},
        "AU": {"WI": 2, "PR": 3, "IT": 9},
        "VR": {"PG": 3, "IT": 4},
        "PR": {"TA": 12, "RS": 9, "WI": 5, "AU": 3, "PG": 13},
        "IB": {"RS": 5, "AG": 10, "LO": 8, "PG": 7, "WI": 6, "IT": 2},
        "IT": {"RS": 8, "RO": 14, "TC": 11, "VR": 4, "AU": 9, "IB": 2}
    }

    no_validos = list(grafo.keys())
    print(f"Vértices disponíveis no grafo: {', '.join(no_validos)}")
    
    origem = input("Digite o ponto de partida: ").strip().upper()
    destino = input("Digite o ponto de chegada: ").strip().upper()

    distancia, caminho = dijkstra_ponto_a_ponto(grafo, origem, destino)

    if distancia is None:
        print("\n[Erro] Certifique-se de escolher nós válidos presentes no grafo.")
    elif distancia == float('inf'):
        print(f"\nNão há caminho disponível entre {origem} e {destino}.")
    else:
        print(f"\nDistância mínima de {origem} até {destino}: {distancia}")
        print(f"Rota recomendada: {' -> '.join(caminho)}")