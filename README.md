# Algoritmo de Dijkstra - Menor Caminho em Grafos

> Projeto desenvolvido para a disciplina de **Estrutura de Dados II** (Turma: T32).  
> **Autores:** Matheus Schramm e Gustavo Pickler Vieira.

---

## 📌 Sobre o Projeto

Este repositório contém a implementação do **Algoritmo de Dijkstra**, um algoritmo clássico guloso (*greedy*) utilizado para encontrar o caminho de menor custo (menor distância ponderada) entre vértices em um grafo com arestas de pesos não-negativos.

O projeto conta com duas formas de utilização:
1. **Script Python (CLI)**: Execução direta no terminal com validações e cálculo via fila de prioridades (*min-heap*).
2. **Interface Web Interativa (HTML/CSS/JS + SVG)**: Visualização gráfica e interativa onde o usuário pode selecionar vértices por listas suspensas ou clicando diretamente nos nós do grafo desenhado em SVG.

---

## 🚀 Funcionalidades

- **Cálculo de Rota Ponto a Ponto**: Determina a distância mínima e a sequência exata de vértices que compõem o melhor trajeto.
- **Estrutura de Alta Eficiência**:
  - Em Python: Uso da biblioteca `heapq` ($O((V + E) \log V)$).
  - Em JavaScript: Resolução e renderização dinâmica no navegador com destaque visual das arestas e nós percorridos.
- **Parada Antecipada**: O algoritmo interrompe a busca assim que o vértice de destino é desempilhado da fila de prioridade, otimizando o processamento.
- **Rastreamento de Predecessores (Backtracking)**: Reconstrói o trajeto completo percorrido da origem até o destino.
- **Interface Gráfica com SVG**: Grafo interativo com nós clicáveis, custos exibidos nas arestas e atualização em tempo real do trajeto selecionado.

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
└── README.md                    # Documentação do projeto
```

---

## 🛠️ Como Executar

### 1. Executando via Terminal (Python)

Certifique-se de ter o **Python 3.8+** instalado. Não é necessário instalar nenhuma dependência externa (o módulo `heapq` faz parte da biblioteca padrão do Python).

```bash
# Navegue até a pasta do projeto
cd projeto

# Execute o script interativo
python dijkstra.py
```

**Exemplo de uso no terminal:**
```text
Vértices disponíveis no grafo: RS, TA, LA, SA, RO, TC, AG, LO, PG, WI, AU, VR, PR, IB, IT
Digite o ponto de partida: RS
Digite o ponto de chegada: PR

Distância mínima de RS até PR: 9
Rota recomendada: RS -> PR
```

---

### 2. Executando a Interface Web

Para visualizar e interagir com o grafo graficamente:

1. Acesse a pasta `projeto/`.
2. Abra o arquivo `interface.html` em qualquer navegador moderno (Google Chrome, Firefox, Edge, etc.).
3. Selecione os vértices de partida e chegada pelas caixas de seleção ou clicando diretamente sobre as bolinhas do grafo!

---

## 🧠 Como o Algoritmo Funciona

1. **Inicialização**: A distância para o nó inicial é definida como `0` e para todos os outros nós como $\infty$ (`Infinity`).
2. **Fila de Prioridades**: O algoritmo retira sempre o nó com menor distância acumulada.
3. **Relaxamento de Arestas**: Para cada vizinho do nó atual, calcula se passar por ele resulta em uma distância menor do que a anteriormente conhecida. Se sim:
   - A menor distância do vizinho é atualizada;
   - O nó atual é salvo como predecessor do vizinho;
   - O vizinho é inserido na fila de prioridades com o novo custo acumulado.
4. **Reconstrução**: Ao alcançar o destino, o caminho é reconstruído voltando nó a nó a partir dos predecessores.

---

## 👥 Autores

- **Matheus Schramm**
- **Gustavo Pickler Vieira**

*Disciplina de Estrutura de Dados II — Turma T32*
