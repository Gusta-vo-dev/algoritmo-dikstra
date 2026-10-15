# Algoritmo de Dijkstra - Menor Caminho em Grafos

> Projeto desenvolvido para a disciplina de **Estrutura de Dados II** (Turma: T32).  
> **Autores:** Matheus Schramm e Gustavo Pickler Vieira.

---

## 📌 Sobre o Projeto

Este repositório contém a implementação do **Algoritmo de Dijkstra**, um algoritmo clássico guloso (*greedy*) criado pelo cientista da computação Edsger Dijkstra. Seu objetivo é encontrar o caminho de menor custo (menor distância acumulada) entre vértices em um grafo com arestas de pesos não-negativos.

O projeto disponibiliza duas formas de visualização e uso:
1. **Script Python (CLI)**: Executado diretamente via terminal, estruturado com fila de prioridades (*min-heap*), validações e reconstrução da rota.
2. **Interface Web Interativa (HTML/CSS/JS + SVG)**: Renderização gráfica e interativa onde o usuário pode selecionar vértices via dropdowns ou clicando diretamente sobre os nós do grafo em SVG.

---

## 🚀 Funcionalidades

- **Cálculo de Rota Ponto a Ponto**: Determina a distância mínima e a sequência exata de vértices que compõem o melhor trajeto.
- **Estrutura com Fila de Prioridades (Min-Heap)**: Uso da biblioteca `heapq` em Python para garantir complexidade $O((V + E) \log V)$.
- **Parada Antecipada**: A busca é interrompida assim que o vértice de destino é extraído da fila de prioridade, economizando iterações desnecessárias.
- **Rastreamento de Predecessores (Backtracking)**: Mapeamento em tempo de execução para reconstruir o trajeto do destino de volta à origem.
- **Interface Gráfica com SVG**: Grafo interativo com nós clicáveis, custos exibidos nas arestas e atualização dinâmica do caminho calculado.

---

## 📁 Estrutura do Repositório

```text
algoritmo-dikstra/
├── Licenças/
│   └── LICENSE                  # Licença do projeto
├── projeto/
│   ├── dijkstra.py              # Implementação principal em Python (CLI)
│   ├── dijkstra_estudo.py       # Versão comentada passo a passo para fins didáticos
│   ├── interface.html           # Página web da interface gráfica interativa
│   ├── interface.css            # Estilização visual moderna e responsiva
│   ├── interface.js             # Lógica do Dijkstra e manipulação do SVG no navegador
│   └── grafo_com_custos.pdf     # Representação esquemática do grafo de referência
└── README.md                    # Documentação detalhada do projeto
```

---

## 🐍 Guia Rápido: Python vs JavaScript

Para quem vem do ecossistema **JavaScript**, a tabela abaixo resume as equivalências diretas utilizadas no código:

| Conceito | Python (`dijkstra.py`) | Equivalente em JavaScript |
| :--- | :--- | :--- |
| **Dicionário / Objeto** | `{"A": 5}` | `{ A: 5 }` |
| **Lista / Array** | `[1, 2, 3]` | `[1, 2, 3]` |
| **Infinito** | `float('inf')` | `Infinity` |
| **Nulo** | `None` | `null` |
| **Verificar chave** | `if item in grafo:` | `if (item in grafo)` ou `grafo.hasOwnProperty(item)` |
| **Desestruturação (Unpacking)** | `dist, vertice = tupla` | `const [dist, vertice] = tupla` |
| **Iterar Chave e Valor** | `for vizinho, peso in grafo[no].items():` | `for (const [vizinho, peso] of Object.entries(grafo[no]))` |
| **Adicionar ao Array** | `lista.append(item)` | `array.push(item)` |
| **Inverter Array** | `lista.reverse()` | `array.reverse()` |
| **Fila de Prioridade** | Módulo nativo `heapq` | Não nativo (necessário ordenar ou criar classe Heap) |
| **Interpolação de String** | `f"Rota: {caminho}"` | `` `Rota: ${caminho}` `` |

---

## 🔍 Entendendo o Código Passo a Passo (`dijkstra.py`)

Abaixo está o detalhamento de cada bloco e comando do arquivo `dijkstra.py`:

### 1. Importação e Validação Inicial

```python
import heapq

def dijkstra_ponto_a_ponto(grafo, inicio, fim):
    if inicio not in grafo or fim not in grafo:
        return None, []
```

- **`import heapq`**: Módulo nativo do Python que implementa uma fila de prioridade (*min-heap*). Garante que a remoção do menor elemento ocorra em tempo logarítmico ($O(\log n)$).
- **`def dijkstra_ponto_a_ponto(grafo, inicio, fim):`**: Assinatura da função principal.
- **`if inicio not in grafo or fim not in grafo:`**: Protege o algoritmo contra entradas inválidas digitadas pelo usuário, retornando `None` para a distância e `[]` para a rota.

---

### 2. Inicialização das Estruturas de Dados

```python
    distancias = {vertice: float('inf') for vertice in grafo}
    distancias[inicio] = 0
    
    anteriores = {vertice: None for vertice in grafo}
    
    fila_prioridade = [(0, inicio)]
    chegou_ao_destino = False
```

- **`distancias = {vertice: float('inf') for vertice in grafo}`**: *Dict comprehension* que inicializa a distância até cada nó como infinita ($\infty$).
- **`distancias[inicio] = 0`**: A distância para começar no ponto de partida é zero.
- **`anteriores = {vertice: None for vertice in grafo}`**: Tabela de predecessores que armazena quem visitou cada nó para permitir a reconstrução do caminho no final.
- **`fila_prioridade = [(0, inicio)]`**: Lista iniciada com uma tupla `(distancia_acumulada, vertice)`. No Python, o `heapq` compara sempre o primeiro elemento da tupla para manter o menor no topo.
- **`chegou_ao_destino = False`**: Flag booleana que controla o encerramento do laço de repetição.

---

### 3. O Loop Principal (Relaxamento das Arestas)

```python
    while fila_prioridade and not chegou_ao_destino:
        distancia_atual, vertice_atual = heapq.heappop(fila_prioridade)

        if vertice_atual == fim:
            chegou_ao_destino = True

        elif distancia_atual <= distancias[vertice_atual]:
            for vizinho, peso in grafo[vertice_atual].items():
                distancia_nova = distancia_atual + peso

                if distancia_nova < distancias[vizinho]:
                    distancias[vizinho] = distancia_nova
                    anteriores[vizinho] = vertice_atual
                    heapq.heappush(fila_prioridade, (distancia_nova, vizinho))
```

- **`while fila_prioridade and not chegou_ao_destino:`**: Continua enquanto houver nós pendentes na fila e o destino não tiver sido alcançado.
- **`distancia_atual, vertice_atual = heapq.heappop(fila_prioridade)`**: Extrai o elemento com menor custo acumulado da fila.
- **Parada Antecipada (`if vertice_atual == fim`)**: Como o algoritmo de Dijkstra garante que a primeira vez que um nó é desempilhado da fila ele já tem seu menor custo definitivo, podemos encerrar o laço imediatamente ao alcançar o destino.
- **`elif distancia_atual <= distancias[vertice_atual]:`**: Descarta registros obsoletos que possam ter sobrado na fila com custos maiores do que o já registrado na tabela de distâncias.
- **Relaxamento de Arestas**:
  - `distancia_nova = distancia_atual + peso`: Calcula o custo para atingir o vizinho vindo pelo nó atual.
  - Se `distancia_nova < distancias[vizinho]`:
    1. Atualiza `distancias[vizinho] = distancia_nova`.
    2. Registra o predecessor: `anteriores[vizinho] = vertice_atual`.
    3. Insere na fila de prioridade: `heapq.heappush(fila_prioridade, (distancia_nova, vizinho))`.

---

### 4. Reconstrução do Caminho (Backtracking)

```python
    caminho = []
    atual = fim
    while atual is not None:
        caminho.append(atual)
        atual = anteriores[atual]
    caminho.reverse()
    
    if distancias[fim] == float('inf'):
        return float('inf'), []
        
    return distancias[fim], caminho
```

- Inicia no `fim` e faz a leitura reversa consultando o dicionário `anteriores`.
- `caminho.reverse()`: Desinverte a lista para que a rota fique no sentido correto (`origem -> ... -> destino`).
- Retorna uma tupla contendo o custo final e o array do trajeto.

---

### 5. Execução do Script (`if __name__ == "__main__":`)

```python
if __name__ == "__main__":
    # Definição do grafo em formato de dicionário
    ...
    origem = input("Digite o ponto de partida: ").strip().upper()
    destino = input("Digite o ponto de chegada: ").strip().upper()

    distancia, caminho = dijkstra_ponto_a_ponto(grafo, origem, destino)
    ...
```

- **`if __name__ == "__main__":`**: Garante que o bloco interativo com `input()` só execute se o arquivo for rodado diretamente (`python dijkstra.py`). Se for importado por outro arquivo (`import dijkstra`), o bloco não executa sozinho.
- **`.strip().upper()`**: Higieniza o texto digitado pelo usuário, removendo espaços e convertendo para letras maiúsculas.

---

## 🧪 Simulação Prática Passo a Passo

Imagine um grafo simplificado:
- **A** conecta em **B** com peso **4**
- **A** conecta em **C** com peso **2**
- **C** conecta em **B** com peso **1**
- **Origem:** `A` | **Destino:** `B`

Veja o estado da memória a cada passo:

| Passo | Ação / Nó Extraído | Fila de Prioridade | Tabela de Distâncias | Predecessores (`anteriores`) |
| :---: | :--- | :--- | :--- | :--- |
| **0** | Inicialização | `[(0, 'A')]` | `{A: 0, B: ∞, C: ∞}` | `{A: None, B: None, C: None}` |
| **1** | Extrai `(0, 'A')` | Analisa vizinhos `B` e `C` | `{A: 0, B: 4, C: 2}` | `{B: 'A', C: 'A'}` |
| | Coloca `(2, 'C')` e `(4, 'B')` | `[(2, 'C'), (4, 'B')]` | | |
| **2** | Extrai `(2, 'C')` *(menor custo)* | Analisa vizinho `B`: custo $2+1=3 < 4$ (**Atalho encontrado!**) | `{A: 0, B: 3, C: 2}` | `{B: 'C', C: 'A'}` |
| | Atualiza e empilha `(3, 'B')` | `[(3, 'B'), (4, 'B')]` | | |
| **3** | Extrai `(3, 'B')` | `vertice_atual == destino` (`'B' == 'B'`). **Fim da busca!** | `{A: 0, B: 3, C: 2}` | `{B: 'C', C: 'A'}` |

**Reconstrução do trajeto:**
- Começa em `B` $\rightarrow$ anterior é `C` $\rightarrow$ anterior é `A` $\rightarrow$ anterior é `None`.
- Invertendo o caminho: `['A', 'C', 'B']` com distância total **3**.

---

## 🛠️ Como Executar o Projeto

### 1. Terminal (Python CLI)

Certifique-se de possuir o **Python 3.8+** instalado:

```bash
# Entre na pasta do projeto
cd projeto

# Execute o script interativo
python dijkstra.py
```

**Exemplo no terminal:**
```text
Vértices disponíveis no grafo: RS, TA, LA, SA, RO, TC, AG, LO, PG, WI, AU, VR, PR, IB, IT
Digite o ponto de partida: RS
Digite o ponto de chegada: PR

Distância mínima de RS até PR: 9
Rota recomendada: RS -> PR
```

---

### 2. Interface Web Interativa (HTML/CSS/JS)

1. Acesse o diretório `projeto/`.
2. Abra o arquivo `interface.html` no seu navegador de preferência (Google Chrome, Firefox, Safari ou Edge).
3. Selecione os nós de origem e destino nos menus suspensos ou clique diretamente nas circunferências dos vértices no desenho SVG.
4. A rota ótima será calculada e iluminada na tela em tempo real!

---

## 👥 Autores

- **Matheus Schramm**
- **Gustavo Pickler Vieira**

*Disciplina de Estrutura de Dados II — Turma T32*
