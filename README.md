# Algoritmo de Dijkstra - Menor Caminho em Grafos

> Projeto desenvolvido para a disciplina de **Estrutura de Dados II** (Turma: T32).  
> **Autores:** Matheus Schramm e Gustavo Pickler Vieira.

---

## 📌 Sobre o Projeto

Este repositório contém a implementação do **Algoritmo de Dijkstra**, um algoritmo clássico guloso (*greedy*) criado pelo cientista da computação Edsger Dijkstra. Seu objetivo é encontrar o caminho de menor custo (menor distância acumulada) entre vértices em um grafo com arestas de pesos não-negativos.

O cálculo é feito em **Python** (`dijkstra.py`) e o resultado é mostrado em uma **interface web** (HTML/CSS/JS + SVG), onde o usuário escolhe a origem e o destino e vê o menor caminho destacado no desenho do grafo.

---

## 🚀 Funcionalidades

- **Cálculo de Rota Ponto a Ponto**: Determina a distância mínima e a sequência exata de vértices que compõem o melhor trajeto.
- **Estrutura com Fila de Prioridades (Min-Heap)**: Uso da biblioteca `heapq` em Python para garantir complexidade $O((V + E) \log V)$.
- **Parada Antecipada**: A busca é interrompida assim que o vértice de destino é extraído da fila de prioridade, economizando iterações desnecessárias.
- **Rastreamento de Predecessores (Backtracking)**: Mapeamento em tempo de execução para reconstruir o trajeto do destino de volta à origem.
- **Servidor Python embutido**: O próprio `dijkstra.py` liga o algoritmo à interface usando o módulo `http.server`, que já vem com o Python (nada para instalar).
- **Interface Gráfica com SVG**: Grafo interativo com nós clicáveis, nome das cidades, custos nas arestas e o caminho calculado destacado em azul.

---

## 📁 Estrutura do Repositório

```text
algoritmo-dikstra/
├── Licenças/
│   └── LICENSE                  # Licença do projeto
├── projeto/
│   ├── dijkstra.py              # Algoritmo de Dijkstra + servidor da interface
│   ├── dijkstra_estudo.py       # Versão comentada passo a passo para fins didáticos
│   ├── interface.html           # Estrutura da página
│   ├── interface.css            # Aparência da página (cores, layout)
│   ├── interface.js             # Desenho do grafo e comunicação com o Python
│   └── grafo_com_custos.pdf     # Representação esquemática do grafo de referência
└── README.md                    # Documentação do projeto
```

---

## 🛠️ Como Executar o Projeto

Certifique-se de possuir o **Python 3.8+** instalado:

```bash
# Entre na pasta do projeto
cd projeto

# Inicie o servidor
python dijkstra.py
```

O terminal vai mostrar:

```text
Abra no navegador: http://127.0.0.1:8000/interface.html
Para encerrar, aperte Ctrl+C.
```

1. Abra o endereço `http://127.0.0.1:8000/interface.html` no navegador.
2. Escolha a origem e o destino nas listas, ou clique nos vértices do grafo (o primeiro clique é a origem, o segundo é o destino).
3. A distância mínima, a rota e o custo de cada trecho aparecem no painel, e o caminho fica destacado em azul no grafo.

> ⚠️ **Importante:** abrir o `interface.html` com dois cliques **não funciona**, porque o cálculo é feito pelo Python. A página precisa ser aberta pelo endereço do servidor. O comando também precisa ser rodado **dentro da pasta `projeto`**, pois o servidor entrega os arquivos da pasta onde foi iniciado.

---

## 🔄 Como as Peças se Conectam

O navegador não sabe executar Python. Por isso o `dijkstra.py` também funciona como um **servidor**: um programa que fica esperando pedidos do navegador e responde a eles.

```text
┌──────────────────────────┐                         ┌──────────────────────────────┐
│        NAVEGADOR         │                         │      PYTHON (dijkstra.py)    │
│                          │  1. GET /interface.html │                              │
│  interface.html          │ ──────────────────────► │  entrega os arquivos         │
│  interface.css           │ ◄────────────────────── │  html, css e js              │
│  interface.js            │                         │                              │
│                          │  2. GET /grafo          │                              │
│  desenha o grafo         │ ──────────────────────► │  envia o dicionário grafo    │
│                          │ ◄────────────────────── │  em formato JSON             │
│                          │                         │                              │
│  usuário escolhe         │  3. GET /calcular       │                              │
│  origem e destino        │    ?origem=LA           │  chama                       │
│                          │    &destino=VR          │  dijkstra_ponto_a_ponto()    │
│  destaca o caminho       │ ──────────────────────► │                              │
│                          │ ◄────────────────────── │  {"distancia": 17,           │
│                          │                         │   "caminho": [...]}          │
└──────────────────────────┘                         └──────────────────────────────┘
```

1. **Abrir a página:** o navegador pede o `interface.html`, que por sua vez pede o `interface.css` e o `interface.js`. O servidor entrega os três arquivos.
2. **Desenhar o grafo:** o `interface.js` pede o endereço `/grafo`. O Python responde com o dicionário `grafo` convertido para **JSON** (um formato de texto que tanto o Python quanto o JavaScript entendem).
3. **Calcular a rota:** quando o usuário escolhe origem e destino, o `interface.js` pede `/calcular?origem=LA&destino=VR`. O Python executa a função `dijkstra_ponto_a_ponto` e devolve a distância e o caminho, que a página mostra na tela.

Ou seja: **todo o cálculo do menor caminho acontece no Python**. O JavaScript só desenha e mostra o resultado.

---

## 🔍 Entendendo o `dijkstra.py` Linha por Linha

O arquivo tem quatro partes: as importações, a função do algoritmo, o grafo e o servidor.

### 1. Importações

```python
import heapq
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
```

- **`import heapq`**: Módulo do Python que implementa uma fila de prioridade (*min-heap*). Ele sempre devolve o **menor** elemento da fila, em tempo $O(\log n)$. É usado pelo algoritmo.
- **`import json`**: Converte dados do Python (dicionários, listas, números) para texto JSON, que é enviado ao navegador. Usado pelo servidor.
- **`from http.server import HTTPServer, SimpleHTTPRequestHandler`**: Ferramentas para criar um servidor web. O `HTTPServer` fica escutando os pedidos, e o `SimpleHTTPRequestHandler` sabe responder a eles entregando arquivos da pasta. Usado pelo servidor.
- **`from urllib.parse import urlparse, parse_qs`**: Funções para "desmontar" um endereço. Por exemplo, separam `/calcular?origem=RS&destino=IT` em caminho (`/calcular`) e parâmetros (`origem=RS`, `destino=IT`). Usado pelo servidor.

---

### 2. Assinatura da Função e Validação Inicial

```python
def dijkstra_ponto_a_ponto(grafo, inicio, fim):
    """
    Calcula a menor distância e o caminho percorrido entre um ponto de origem e um de destino.
    """
    # Validação rápida de existência dos nós
    if inicio not in grafo or fim not in grafo:
        return None, []
```

- **`def dijkstra_ponto_a_ponto(grafo, inicio, fim):`**: Define a função. Ela recebe o grafo (um dicionário), o vértice de partida e o vértice de chegada.
- **`"""..."""`**: *Docstring*, um texto que documenta o que a função faz.
- **`if inicio not in grafo or fim not in grafo:`**: Verifica se a origem e o destino existem no grafo. O operador `in` em um dicionário verifica se a chave existe.
- **`return None, []`**: Se algum vértice não existir, a função termina aqui e devolve duas coisas: `None` (nenhuma distância) e `[]` (uma lista vazia, nenhum caminho).

---

### 3. Inicialização das Estruturas de Dados

```python
    distancias = {vertice: float('inf') for vertice in grafo}
    distancias[inicio] = 0
    
    # Dicionário para rastrear o caminho (predecessores)
    anteriores = {vertice: None for vertice in grafo}
    
    # Fila de prioridades: (distância acumulada, vértice atual)
    fila_prioridade = [(0, inicio)]

    # Indica se já chegamos ao destino (usado para encerrar o laço)
    chegou_ao_destino = False
```

- **`distancias = {vertice: float('inf') for vertice in grafo}`**: Cria um dicionário com todos os vértices, cada um com distância **infinita** ($\infty$). É uma *dict comprehension*: uma forma curta de montar um dicionário com um `for`. Infinito significa "ainda não sabemos chegar lá".
- **`distancias[inicio] = 0`**: A distância da origem até ela mesma é zero.
- **`anteriores = {vertice: None for vertice in grafo}`**: Para cada vértice, guarda **de qual vértice viemos** no melhor caminho encontrado. Começa tudo com `None` (nenhum). É com ele que o caminho é montado no final.
- **`fila_prioridade = [(0, inicio)]`**: A fila começa com uma tupla `(distância, vértice)` contendo só a origem. O `heapq` compara as tuplas pelo primeiro elemento, então o vértice com **menor distância** sempre sai primeiro.
- **`chegou_ao_destino = False`**: Uma *flag* (variável verdadeiro/falso) que controla quando o laço principal deve parar.

---

### 4. O Laço Principal (Relaxamento das Arestas)

```python
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
```

- **`while fila_prioridade and not chegou_ao_destino:`**: Repete enquanto **houver itens na fila** (uma lista vazia conta como falso) **e** o destino ainda **não** tiver sido alcançado. Quando qualquer uma das duas condições falha, o laço termina.
- **`distancia_atual, vertice_atual = heapq.heappop(fila_prioridade)`**: Tira da fila o item de **menor distância** e separa a tupla em duas variáveis (*desempacotamento*).
- **`if vertice_atual == fim:`**: Se o vértice que saiu da fila é o destino, a busca terminou.
- **`chegou_ao_destino = True`**: Muda a flag. Na próxima verificação do `while`, a condição fica falsa e o laço para. Isso funciona porque, no Dijkstra, quando um vértice sai da fila, a distância dele já é a menor possível.
- **`elif distancia_atual <= distancias[vertice_atual]:`**: Um mesmo vértice pode entrar na fila mais de uma vez (cada vez que achamos um caminho melhor até ele). Se a distância que saiu da fila for **maior** do que a já registrada, é um registro antigo e é ignorado. Só seguimos se ela for a melhor conhecida.
- **`for vizinho, peso in grafo[vertice_atual].items():`**: Percorre cada vizinho do vértice atual. O `.items()` devolve pares `(chave, valor)`, aqui `(vizinho, peso da aresta)`.
- **`distancia_nova = distancia_atual + peso`**: Calcula quanto custaria chegar ao vizinho passando pelo vértice atual.
- **`if distancia_nova < distancias[vizinho]:`**: Se esse caminho for **mais curto** do que o melhor conhecido até agora para o vizinho... (esse passo se chama **relaxamento**)
  - **`distancias[vizinho] = distancia_nova`**: ...atualiza a menor distância do vizinho;
  - **`anteriores[vizinho] = vertice_atual`**: ...anota que o melhor jeito de chegar ao vizinho é vindo do vértice atual;
  - **`heapq.heappush(fila_prioridade, (distancia_nova, vizinho))`**: ...e coloca o vizinho na fila para ser analisado depois.

---

### 5. Reconstrução do Caminho (Backtracking)

```python
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
```

- **`caminho = []`**: Lista vazia que vai receber os vértices da rota.
- **`atual = fim`**: Começamos pelo **destino** e andamos para trás.
- **`while atual is not None:`**: Repete até chegar em um vértice sem anterior, que é a origem.
- **`caminho.append(atual)`**: Adiciona o vértice atual no fim da lista.
- **`atual = anteriores[atual]`**: Vai para o vértice de onde viemos.
- **`caminho.reverse()`**: Como montamos de trás para frente (destino → origem), invertemos a lista para ficar origem → destino.
- **`if distancias[fim] == float('inf'):`**: Se a distância do destino continua infinita, nenhum caminho chegou até ele.
- **`return float('inf'), []`**: Nesse caso, devolve distância infinita e caminho vazio.
- **`return distancias[fim], caminho`**: Caso contrário, devolve a menor distância e a lista com a rota.

---

### 6. O Grafo

```python
grafo = {
    "RS": {"TA": 7, "RO": 5, "TC": 4, "LO": 2, "PG": 6, "PR": 9, "IB": 5, "IT": 8},
    "TA": {"LA": 4, "SA": 5, "AG": 9, "RS": 7, "PR": 12},
    ...
    "IT": {"RS": 8, "RO": 14, "TC": 11, "VR": 4, "AU": 9, "IB": 2}
}
```

- O grafo é um **dicionário de dicionários** (uma *lista de adjacência*). Cada chave é um vértice, e o valor é outro dicionário com os **vizinhos** e o **custo** para chegar até eles.
- Exemplo: `"RS": {"TA": 7, ...}` significa que existe uma aresta de RS até TA com custo 7.
- O grafo é **não direcionado**: toda aresta aparece nos dois sentidos (`"RS": {"TA": 7}` e `"TA": {"RS": 7}`).
- Ele fica **fora** da função e fora do `if __name__`, para o servidor conseguir enviá-lo à interface. O desenho no `grafo_com_custos.pdf` representa exatamente este dicionário.

---

### 7. O Servidor da Interface

```python
class Servidor(SimpleHTTPRequestHandler):

    def do_GET(self):
        endereco = urlparse(self.path)
```

- **`class Servidor(SimpleHTTPRequestHandler):`**: Cria uma classe chamada `Servidor` que **herda** do `SimpleHTTPRequestHandler`. Ou seja, ela já sabe tudo que a classe original sabe (como entregar arquivos), e nós só acrescentamos o que é diferente.
- **`def do_GET(self):`**: Esse método é chamado automaticamente **toda vez que o navegador pede algo** ao servidor (um pedido do tipo GET).
- **`endereco = urlparse(self.path)`**: `self.path` é o endereço pedido, por exemplo `/calcular?origem=RS&destino=IT`. O `urlparse` separa em `endereco.path` (`/calcular`) e `endereco.query` (`origem=RS&destino=IT`).

```python
        # A página pede o grafo para desenhar na tela
        if endereco.path == "/grafo":
            self.responder(grafo)
```

- **`if endereco.path == "/grafo":`**: Se a página pediu o grafo...
- **`self.responder(grafo)`**: ...envia o dicionário `grafo` para ela (o método `responder` está explicado mais abaixo).

```python
        # A página pede o menor caminho, ex.: /calcular?origem=RS&destino=IT
        elif endereco.path == "/calcular":
            parametros = parse_qs(endereco.query)
            origem = parametros["origem"][0]
            destino = parametros["destino"][0]

            distancia, caminho = dijkstra_ponto_a_ponto(grafo, origem, destino)

            # Sem caminho: enviamos a distância vazia (null)
            if distancia == float('inf'):
                distancia = None

            self.responder({"distancia": distancia, "caminho": caminho})
```

- **`elif endereco.path == "/calcular":`**: Se a página pediu um cálculo...
- **`parametros = parse_qs(endereco.query)`**: Transforma `origem=RS&destino=IT` em um dicionário: `{"origem": ["RS"], "destino": ["IT"]}`. Cada valor vem dentro de uma lista, porque um endereço pode repetir o mesmo parâmetro.
- **`origem = parametros["origem"][0]`** e **`destino = parametros["destino"][0]`**: Pegam o primeiro (e único) valor de cada lista.
- **`distancia, caminho = dijkstra_ponto_a_ponto(grafo, origem, destino)`**: Chama o algoritmo. **É aqui que o Python faz o cálculo pedido pela interface.**
- **`if distancia == float('inf'): distancia = None`**: O formato JSON não tem "infinito". Por isso, quando não existe caminho, trocamos por `None`, que no JSON vira `null`.
- **`self.responder({"distancia": distancia, "caminho": caminho})`**: Envia a resposta, por exemplo `{"distancia": 17, "caminho": ["LA", "RO", "RS", "PG", "VR"]}`.

```python
        # Qualquer outro pedido: entrega os arquivos da pasta (html, css, js)
        else:
            super().do_GET()
```

- **`else: super().do_GET()`**: Para qualquer outro endereço (como `/interface.html` ou `/interface.css`), usamos o comportamento **original** da classe pai (`super()`), que procura o arquivo na pasta e o entrega ao navegador.

```python
    # Envia os dados para a página no formato JSON
    def responder(self, dados):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(dados).encode("utf-8"))
```

- **`def responder(self, dados):`**: Método criado por nós para não repetir o código de resposta.
- **`self.send_response(200)`**: Envia o código **200**, que significa "deu tudo certo".
- **`self.send_header("Content-Type", "application/json")`**: Avisa o navegador que a resposta é JSON.
- **`self.end_headers()`**: Fecha o cabeçalho; a partir daqui vem o conteúdo.
- **`json.dumps(dados)`**: Converte o dado do Python em texto JSON. Ex.: `None` vira `null`, `["RS", "IT"]` continua `["RS", "IT"]`.
- **`.encode("utf-8")`**: Converte o texto em bytes, que é o que a rede transmite. O UTF-8 garante que acentos funcionem.
- **`self.wfile.write(...)`**: Escreve os bytes na resposta enviada ao navegador.

---

### 8. Execução do Script (`if __name__ == "__main__":`)

```python
if __name__ == "__main__":
    servidor = HTTPServer(("127.0.0.1", 8000), Servidor)
    print("Abra no navegador: http://127.0.0.1:8000/interface.html")
    print("Para encerrar, aperte Ctrl+C.")
    servidor.serve_forever()
```

- **`if __name__ == "__main__":`**: Esse bloco só roda quando o arquivo é executado diretamente (`python dijkstra.py`). Se o arquivo for importado por outro (`import dijkstra`), o servidor não é iniciado.
- **`servidor = HTTPServer(("127.0.0.1", 8000), Servidor)`**: Cria o servidor.
  - `"127.0.0.1"` é o endereço do **próprio computador**. Usamos ele em vez de `"localhost"` porque no Windows o `localhost` pode deixar cada pedido cerca de 2 segundos mais lento.
  - `8000` é a **porta**, um "número de canal" para o navegador encontrar o servidor.
  - `Servidor` é a nossa classe, que diz como responder a cada pedido.
- **`print(...)`**: Mostra no terminal o endereço para abrir e como encerrar.
- **`servidor.serve_forever()`**: Inicia o servidor e fica esperando pedidos **para sempre**, até o usuário apertar `Ctrl+C`.

---

## 🌐 Entendendo o `interface.js` Bloco por Bloco

O `interface.js` é dividido em 4 seções, marcadas com comentários no código.

### 1. Dados do Grafo

```javascript
let grafo = {};
```

- **`let grafo = {};`**: Começa vazio. Ele é preenchido com o grafo que vem do Python quando a página abre. Usamos `let` (e não `const`) porque o valor é trocado depois.

```javascript
const nomes = {
    RS: "Rio do Sul",
    TA: "Taió",
    ...
};
```

- **`nomes`**: Liga cada sigla ao nome da cidade, usado no desenho, nas listas e no resultado. Para corrigir algum nome, basta alterar aqui.

```javascript
const posicoes = {
    TA: { x: 455, y: 110 },
    ...
};
```

- **`posicoes`**: As coordenadas (x, y) de cada vértice na tela, copiadas do `grafo_com_custos.pdf` para o desenho ficar igual. O `x` cresce para a direita e o `y` cresce **para baixo**.

```javascript
const posicaoDoCusto = {
    "RS-RO": 0.55, "RS-PR": 0.55, ...
};

const RAIO_VERTICE = 36;
```

- **`posicaoDoCusto`**: Em que ponto da linha o número do custo é escrito. `0.5` é o meio da aresta, `0.3` é a 30% do caminho, e assim por diante. Só as arestas que não ficam no meio aparecem aqui, para os números não se sobreporem (como no PDF).
- **`RAIO_VERTICE`**: O tamanho (raio) dos círculos dos vértices.

---

### 2. Comunicação com o Python

```javascript
async function buscarGrafo() {
    const resposta = await fetch("/grafo");
    return await resposta.json();
}
```

- **`async function`**: Indica uma função que faz algo que **demora** (esperar o servidor) sem travar a página.
- **`fetch("/grafo")`**: Faz um pedido ao servidor Python no endereço `/grafo`.
- **`await`**: Espera a resposta chegar antes de seguir para a próxima linha.
- **`resposta.json()`**: Converte o texto JSON recebido em um objeto JavaScript.

```javascript
async function calcularNoPython(origem, destino) {
    const resposta = await fetch("/calcular?origem=" + origem + "&destino=" + destino);
    return await resposta.json();
}
```

- Monta o endereço com os parâmetros (ex.: `/calcular?origem=LA&destino=VR`), pede ao Python e devolve o resultado, que é um objeto como `{ distancia: 17, caminho: ["LA", "RO", "RS", "PG", "VR"] }`.

---

### 3. Desenho do Grafo na Tela (SVG)

O **SVG** é um formato de desenho feito de formas (linhas, círculos, textos) descritas por código, que o navegador mostra na tela.

```javascript
const svg = document.getElementById("grafo");
const SVG_NS = "http://www.w3.org/2000/svg";

function criarElemento(tipo, atributos) {
    const elemento = document.createElementNS(SVG_NS, tipo);
    for (const nome in atributos) {
        elemento.setAttribute(nome, atributos[nome]);
    }
    return elemento;
}
```

- **`document.getElementById("grafo")`**: Pega a área `<svg id="grafo">` do `interface.html`, onde o desenho será feito.
- **`SVG_NS`**: O "*namespace*" do SVG. O navegador exige esse endereço para saber que os elementos criados são de desenho SVG, e não HTML comum.
- **`criarElemento(tipo, atributos)`**: Função auxiliar que cria uma forma (ex.: `"line"`, `"circle"`) e aplica todos os atributos de uma vez (posição, tamanho, classe CSS...).

```javascript
function listarArestas() {
    const arestas = [];
    const jaAdicionadas = {};

    for (const a in grafo) {
        for (const b in grafo[a]) {
            if (!jaAdicionadas[b + "-" + a]) {
                jaAdicionadas[a + "-" + b] = true;
                arestas.push({ a: a, b: b, custo: grafo[a][b] });
            }
        }
    }
    return arestas;
}
```

- Percorre todos os vértices (`a`) e seus vizinhos (`b`) para montar a lista de arestas.
- Como o grafo tem cada aresta duas vezes (RS→TA e TA→RS), o objeto **`jaAdicionadas`** guarda as que já entraram. Se o par invertido (`b-a`) já foi adicionado, a aresta é pulada, para não desenhar a mesma linha duas vezes.

```javascript
function idAresta(a, b) {
    return a < b ? a + "-" + b : b + "-" + a;
}
```

- Gera um nome único para cada aresta, sempre em **ordem alfabética**. Assim, `idAresta("RS", "IB")` e `idAresta("IB", "RS")` dão o mesmo resultado: `"IB-RS"`. Isso é usado para achar a aresta na hora de destacar o caminho.
- O `? :` é o operador ternário: `condição ? valor_se_verdadeiro : valor_se_falso`.

```javascript
function desenharGrafo() {
    const camadaArestas = criarElemento("g", {});
    const camadaCustos = criarElemento("g", {});
    const camadaVertices = criarElemento("g", {});
```

- Cria três **camadas** (`<g>` é um grupo no SVG). No SVG, o que é desenhado depois fica por cima. As camadas garantem a ordem: linhas embaixo, custos no meio e vértices por cima.

```javascript
    for (const aresta of listarArestas()) {
        const p1 = posicoes[aresta.a];
        const p2 = posicoes[aresta.b];
        const id = idAresta(aresta.a, aresta.b);

        const linha = criarElemento("line", {
            x1: p1.x, y1: p1.y, x2: p2.x, y2: p2.y,
            class: "aresta",
            "data-aresta": id
        });
        camadaArestas.appendChild(linha);
```

- Para cada aresta, pega a posição dos dois vértices (`p1` e `p2`) e cria uma **linha** ligando um ao outro.
- **`class: "aresta"`**: Liga a linha ao estilo `.aresta` do CSS (cor cinza).
- **`"data-aresta": id`**: Guarda o nome da aresta dentro do elemento, para encontrá-la depois.
- **`appendChild`**: Coloca a linha dentro da camada de arestas.

```javascript
        let t = posicaoDoCusto[aresta.a + "-" + aresta.b];
        if (t === undefined) {
            t = 0.5;
        }
        const x = p1.x + (p2.x - p1.x) * t;
        const y = p1.y + (p2.y - p1.y) * t;
        const largura = aresta.custo >= 10 ? 32 : 22;
```

- **`t`**: Em que fração da linha o custo será escrito. Se a aresta não estiver em `posicaoDoCusto`, usa `0.5` (o meio).
- **`x` e `y`**: Calculam o ponto da linha nessa fração. É uma interpolação: partindo de `p1`, anda `t` vezes a distância até `p2`.
- **`largura`**: Números com dois dígitos (10 ou mais) ganham uma caixinha mais larga.

```javascript
        const grupoCusto = criarElemento("g", { class: "custo", "data-aresta": id });
        grupoCusto.appendChild(criarElemento("rect", {
            x: x - largura / 2, y: y - 13, width: largura, height: 26, rx: 4
        }));
        const texto = criarElemento("text", {
            x: x, y: y, "text-anchor": "middle", "dominant-baseline": "central"
        });
        texto.textContent = aresta.custo;
        grupoCusto.appendChild(texto);
        camadaCustos.appendChild(grupoCusto);
    }
```

- Cria um grupo com uma caixinha (`rect`) e o número do custo (`text`) dentro dela.
- **`x: x - largura / 2, y: y - 13`**: Desloca a caixa para que o ponto calculado fique no **centro** dela.
- **`rx: 4`**: Arredonda os cantos da caixa.
- **`"text-anchor": "middle"`** e **`"dominant-baseline": "central"`**: Centralizam o texto na horizontal e na vertical.
- **`texto.textContent = aresta.custo`**: Escreve o valor do custo.

```javascript
    for (const vertice in posicoes) {
        const p = posicoes[vertice];
        const grupo = criarElemento("g", { class: "vertice", "data-vertice": vertice });

        grupo.appendChild(criarElemento("circle", { cx: p.x, cy: p.y, r: RAIO_VERTICE }));
        const texto = criarElemento("text", {
            x: p.x, y: p.y, "text-anchor": "middle", "dominant-baseline": "central"
        });
        texto.textContent = vertice;
        grupo.appendChild(texto);
```

- Para cada vértice, cria um grupo com um **círculo** (centro `cx`, `cy` e raio `r`) e a **sigla** escrita no meio.

```javascript
        const nomeCidade = criarElemento("text", {
            x: p.x, y: p.y + RAIO_VERTICE + 20, "text-anchor": "middle", class: "nome-cidade"
        });
        nomeCidade.textContent = nomes[vertice];
        grupo.appendChild(nomeCidade);
```

- Escreve o **nome da cidade** logo abaixo do círculo: a posição `y` é o centro + o raio + 20 de espaço.

```javascript
        grupo.addEventListener("click", function () {
            clicarVertice(vertice);
        });

        camadaVertices.appendChild(grupo);
    }

    svg.appendChild(camadaArestas);
    svg.appendChild(camadaCustos);
    svg.appendChild(camadaVertices);
}
```

- **`addEventListener("click", ...)`**: Faz o vértice "escutar" cliques. Ao clicar, chama `clicarVertice` com a sigla dele.
- No final, as três camadas são colocadas no SVG **nesta ordem**, garantindo que os vértices fiquem por cima das linhas.

```javascript
function destacarCaminho(caminho) {
    for (const elemento of svg.querySelectorAll(".no-caminho, .extremo")) {
        elemento.classList.remove("no-caminho", "extremo");
    }
```

- Recebe a lista de vértices do caminho (ex.: `["LA", "RO", "RS"]`).
- Primeiro **apaga o destaque anterior**: procura todos os elementos com as classes `no-caminho` ou `extremo` e remove essas classes.

```javascript
    for (let i = 0; i < caminho.length; i++) {
        const vertice = svg.querySelector('[data-vertice="' + caminho[i] + '"]');
        vertice.classList.add("no-caminho");

        if (i === 0 || i === caminho.length - 1) {
            vertice.classList.add("extremo");
        }

        if (i < caminho.length - 1) {
            const id = idAresta(caminho[i], caminho[i + 1]);
            for (const elemento of svg.querySelectorAll('[data-aresta="' + id + '"]')) {
                elemento.classList.add("no-caminho");
            }
        }
    }
}
```

- Percorre o caminho pela posição `i`:
  - Encontra o vértice pelo `data-vertice` e adiciona a classe **`no-caminho`** (o CSS pinta de azul).
  - Se for o **primeiro** (`i === 0`) ou o **último** vértice, adiciona também **`extremo`** (azul mais forte, com borda).
  - Se não for o último, destaca a **aresta** entre ele e o próximo (`caminho[i + 1]`), tanto a linha quanto a caixinha do custo, que têm o mesmo `data-aresta`.
- Quem decide as cores é o CSS. O JavaScript só **liga e desliga classes**.

---

### 4. Interação com o Usuário

```javascript
const selectOrigem = document.getElementById("origem");
const selectDestino = document.getElementById("destino");
const botaoLimpar = document.getElementById("limpar");
const resultado = document.getElementById("resultado");
```

- Pega os elementos do `interface.html` que serão usados: as duas listas, o botão e a área do resultado.

```javascript
function preencherListas() {
    for (const vertice in grafo) {
        const texto = vertice + " - " + nomes[vertice];
        selectOrigem.appendChild(new Option(texto, vertice));
        selectDestino.appendChild(new Option(texto, vertice));
    }
}
```

- Para cada vértice, cria uma opção nas duas listas.
- **`new Option(texto, vertice)`**: O primeiro valor é o que o usuário vê (`"RS - Rio do Sul"`), e o segundo é o valor guardado (`"RS"`).

```javascript
function clicarVertice(vertice) {
    if (selectOrigem.value === "" || selectDestino.value !== "") {
        selectOrigem.value = vertice;
        selectDestino.value = "";
    } else {
        selectDestino.value = vertice;
    }
    atualizar();
}
```

- Decide o que o clique significa:
  - Se **ainda não há origem**, ou se **já há origem e destino** (rota completa), o clique define uma **nova origem** e limpa o destino.
  - Caso contrário (já tem origem, falta destino), o clique define o **destino**.
- Depois chama `atualizar()` para recalcular.

```javascript
async function atualizar() {
    const origem = selectOrigem.value;
    const destino = selectDestino.value;

    if (origem === "" || destino === "") {
        destacarCaminho(origem === "" ? [] : [origem]);
        resultado.innerHTML = "<p>Escolha a origem e o destino para ver o menor caminho.</p>";
        return;
    }
```

- Lê o que está escolhido nas duas listas.
- Se **faltar** origem ou destino, destaca só a origem (se houver), mostra uma mensagem de instrução e **para a função** (`return`).

```javascript
    const resposta = await calcularNoPython(origem, destino);

    if (resposta.distancia === null) {
        destacarCaminho([]);
        resultado.innerHTML = '<p class="erro">Não há caminho entre ' + nomes[origem] + " e " + nomes[destino] + ".</p>";
        return;
    }

    destacarCaminho(resposta.caminho);
```

- **`await calcularNoPython(origem, destino)`**: Pede o cálculo ao Python e espera a resposta.
- Se a distância vier `null`, não existe caminho: mostra uma mensagem de erro.
- Caso contrário, destaca o caminho recebido no grafo.

```javascript
    let trechos = "";
    for (let i = 0; i < resposta.caminho.length - 1; i++) {
        const a = resposta.caminho[i];
        const b = resposta.caminho[i + 1];
        trechos += "<li>" + nomes[a] + " → " + nomes[b] + ": " + grafo[a][b] + "</li>";
    }
```

- Monta a lista de **trechos** da rota. Para cada par de vértices seguidos (`a` e `b`), cria um item como `"Laurentino → Rio do Oeste: 3"`. O custo vem de `grafo[a][b]`.

```javascript
    const nomesDoCaminho = resposta.caminho.map(function (vertice) {
        return nomes[vertice];
    });

    resultado.innerHTML =
        "<p>Distância mínima de " + nomes[origem] + " até " + nomes[destino] + ":</p>" +
        '<p class="distancia">' + resposta.distancia + "</p>" +
        '<p class="rota">Rota: ' + nomesDoCaminho.join(" → ") + "</p>" +
        '<ul class="trechos">' + trechos + "</ul>";
}
```

- **`.map(...)`**: Cria uma nova lista trocando cada sigla pelo nome da cidade (`["LA", "RO"]` vira `["Laurentino", "Rio do Oeste"]`).
- **`.join(" → ")`**: Junta a lista em um texto, separado por setas.
- **`resultado.innerHTML = ...`**: Escreve o resultado no painel: a distância, a rota completa e os trechos.

```javascript
function limpar() {
    selectOrigem.value = "";
    selectDestino.value = "";
    atualizar();
}

selectOrigem.addEventListener("change", atualizar);
selectDestino.addEventListener("change", atualizar);
botaoLimpar.addEventListener("click", limpar);
```

- **`limpar()`**: Esvazia as duas listas e atualiza a tela (que volta ao estado inicial).
- **`addEventListener("change", atualizar)`**: Sempre que o usuário trocar a opção de uma lista, recalcula.
- **`addEventListener("click", limpar)`**: O botão "Limpar" chama a função `limpar`.

```javascript
async function iniciar() {
    try {
        grafo = await buscarGrafo();
        preencherListas();
        desenharGrafo();
    } catch (erro) {
        resultado.innerHTML =
            '<p class="erro">Não foi possível falar com o Python. ' +
            "Abra a interface rodando <b>python dijkstra.py</b> na pasta do projeto.</p>";
    }
}

iniciar();
```

- **`iniciar()`**: É o ponto de partida da página.
  - Busca o grafo no Python, preenche as listas e desenha o grafo, **nessa ordem** (as outras duas dependem do grafo).
- **`try { ... } catch (erro) { ... }`**: Se algo der errado dentro do `try` (por exemplo, o servidor Python não estiver rodando), o código do `catch` é executado e mostra uma mensagem explicando o que fazer, em vez de a página simplesmente ficar em branco.
- **`iniciar();`**: Chama a função assim que o arquivo é carregado.

---

## 🧱 O `interface.html` e o `interface.css`

**`interface.html`** define a **estrutura** da página:

- **`<link rel="stylesheet" href="interface.css">`**: Carrega o arquivo de estilos.
- **`<header>`**: Título e subtítulo da página.
- **`<section class="painel">`**: Painel da esquerda, com as listas `<select id="origem">` e `<select id="destino">`, o botão `<button id="limpar">` e a área `<div id="resultado">`. Os `id`s são os nomes que o `interface.js` usa para encontrar cada elemento.
- **`<svg id="grafo" viewBox="30 60 860 1215">`**: Área de desenho do grafo, que começa vazia e é preenchida pelo JavaScript. O `viewBox` define qual região das coordenadas aparece: começa em x=30, y=60, com 860 de largura e 1215 de altura. O navegador ajusta essa região ao tamanho da tela.
- **`<footer>`**: Nome dos alunos e turma.
- **`<script src="interface.js"></script>`**: Carrega o JavaScript. Fica **no final** do `<body>` para que todos os elementos já existam quando o script rodar.

**`interface.css`** define a **aparência**:

- **`:root { --caminho: #2563eb; ... }`**: Variáveis de cor, usadas no resto do arquivo com `var(--caminho)`. Para mudar uma cor, basta alterar aqui.
- **`main { display: flex; }`**: Coloca o painel e o grafo lado a lado.
- **`.aresta`, `.custo`, `.vertice`**: A aparência normal das linhas, dos custos e dos vértices.
- **`.no-caminho` e `.extremo`**: A aparência do caminho destacado (azul). São essas classes que o `destacarCaminho` liga e desliga.
- **`.nome-cidade`**: O nome das cidades, com um contorno branco (`stroke` + `paint-order`) para continuar legível quando passa uma linha por trás.
- **`@media (max-width: 760px)`**: Em telas pequenas (celular), coloca o painel em cima do grafo.

---

## 🐍 Guia Rápido: Python vs JavaScript

O projeto usa as duas linguagens. A tabela abaixo mostra as equivalências entre elas:

| Conceito | Python (`dijkstra.py`) | JavaScript (`interface.js`) |
| :--- | :--- | :--- |
| **Dicionário / Objeto** | `{"A": 5}` | `{ A: 5 }` |
| **Lista / Array** | `[1, 2, 3]` | `[1, 2, 3]` |
| **Infinito** | `float('inf')` | `Infinity` |
| **Nulo** | `None` | `null` |
| **Verificar chave** | `if item in grafo:` | `if (item in grafo)` |
| **Desestruturação (Unpacking)** | `dist, vertice = tupla` | `const [dist, vertice] = tupla` |
| **Iterar Chave e Valor** | `for vizinho, peso in grafo[no].items():` | `for (const vizinho in grafo[no]) { grafo[no][vizinho] }` |
| **Adicionar ao Array** | `lista.append(item)` | `array.push(item)` |
| **Inverter Array** | `lista.reverse()` | `array.reverse()` |
| **Juntar em texto** | `" -> ".join(caminho)` | `caminho.join(" → ")` |
| **Fila de Prioridade** | Módulo nativo `heapq` | Não nativo (necessário ordenar ou criar classe Heap) |
| **Interpolação de String** | `f"Rota: {caminho}"` | `` `Rota: ${caminho}` `` |

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

Repare que o item `(4, 'B')` ficou sobrando na fila. Se o laço continuasse, ele seria descartado pela condição `distancia_atual <= distancias[vertice_atual]` ($4 > 3$).

**Reconstrução do trajeto:**
- Começa em `B` $\rightarrow$ anterior é `C` $\rightarrow$ anterior é `A` $\rightarrow$ anterior é `None`.
- Invertendo o caminho: `['A', 'C', 'B']` com distância total **3**.

---

## 👥 Autores

- **Matheus Schramm**
- **Gustavo Pickler Vieira**

*Disciplina de Estrutura de Dados II — Turma T32*
