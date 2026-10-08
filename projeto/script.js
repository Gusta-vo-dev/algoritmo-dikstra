// ============================================================
// 1. DADOS DO GRAFO (o mesmo grafo do dijkstra.py)
// ============================================================

// Cada vértice tem seus vizinhos e o custo para chegar até eles
const grafo = {
    RS: { TA: 7, RO: 5, TC: 4, LO: 2, PG: 6, PR: 9, IB: 5, IT: 8 },
    TA: { LA: 4, SA: 5, AG: 9, RS: 7, PR: 12 },
    LA: { TA: 4, RO: 3 },
    SA: { TA: 5, TC: 6 },
    RO: { LA: 3, AG: 4, RS: 5, IT: 14 },
    TC: { SA: 6, RS: 4, LO: 3, IT: 11 },
    AG: { TA: 9, RO: 4, WI: 6, IB: 10 },
    LO: { TC: 3, RS: 2, PG: 4, IB: 8 },
    PG: { LO: 4, RS: 6, VR: 3, PR: 13, IB: 7 },
    WI: { AG: 6, AU: 2, PR: 5, IB: 6 },
    AU: { WI: 2, PR: 3, IT: 9 },
    VR: { PG: 3, IT: 4 },
    PR: { TA: 12, RS: 9, WI: 5, AU: 3, PG: 13 },
    IB: { RS: 5, AG: 10, LO: 8, PG: 7, WI: 6, IT: 2 },
    IT: { RS: 8, RO: 14, TC: 11, VR: 4, AU: 9, IB: 2 }
};

// Posição (x, y) de cada vértice na tela, igual ao desenho do PDF
const posicoes = {
    TA: { x: 455, y: 110 },
    LA: { x: 300, y: 163 },
    SA: { x: 608, y: 163 },
    RO: { x: 177, y: 312 },
    TC: { x: 731, y: 312 },
    AG: { x: 108, y: 529 },
    LO: { x: 800, y: 529 },
    RS: { x: 455, y: 648 },
    WI: { x: 108, y: 768 },
    PG: { x: 800, y: 768 },
    AU: { x: 177, y: 985 },
    VR: { x: 731, y: 985 },
    PR: { x: 300, y: 1135 },
    IB: { x: 455, y: 1189 },
    IT: { x: 608, y: 1135 }
};

// Onde fica o custo ao longo da aresta (0.5 = no meio).
// Algumas arestas usam outro valor para os números não ficarem
// um em cima do outro, como no PDF.
const posicaoDoCusto = {
    "RS-RO": 0.55, "RS-PR": 0.55, "RS-IT": 0.55,
    "TA-AG": 0.35, "TA-PR": 0.3,
    "RO-IT": 0.3, "TC-IT": 0.4,
    "AG-IB": 0.3, "LO-IB": 0.55,
    "PG-PR": 0.2, "PG-IB": 0.35,
    "WI-PR": 0.3, "WI-IB": 0.4,
    "AU-IT": 0.25
};

const RAIO_VERTICE = 36;


// ============================================================
// 2. ALGORITMO DE DIJKSTRA
// ============================================================

function dijkstra(grafo, inicio, fim) {
    const distancias = {};   // menor distância conhecida até cada vértice
    const anteriores = {};   // de qual vértice chegamos (para montar o caminho)
    const visitados = {};    // vértices que já foram analisados

    // No começo, todas as distâncias são "infinitas"
    for (const vertice in grafo) {
        distancias[vertice] = Infinity;
        anteriores[vertice] = null;
        visitados[vertice] = false;
    }
    distancias[inicio] = 0;

    let chegouAoDestino = false;

    while (!chegouAoDestino) {
        // Procura o vértice não visitado com a menor distância
        let atual = null;
        for (const vertice in grafo) {
            if (!visitados[vertice] && (atual === null || distancias[vertice] < distancias[atual])) {
                atual = vertice;
            }
        }

        // Se não sobrou nenhum vértice alcançável, encerramos
        if (atual === null || distancias[atual] === Infinity) {
            chegouAoDestino = true;
        } else {
            visitados[atual] = true;

            // Parada antecipada: chegamos ao destino
            if (atual === fim) {
                chegouAoDestino = true;
            } else {
                // Atualiza a distância dos vizinhos se encontrarmos um caminho melhor
                for (const vizinho in grafo[atual]) {
                    const distanciaNova = distancias[atual] + grafo[atual][vizinho];

                    if (distanciaNova < distancias[vizinho]) {
                        distancias[vizinho] = distanciaNova;
                        anteriores[vizinho] = atual;
                    }
                }
            }
        }
    }

    // Caso não exista rota entre os dois pontos
    if (distancias[fim] === Infinity) {
        return { distancia: Infinity, caminho: [] };
    }

    // Monta o caminho do destino de volta até a origem
    const caminho = [];
    let atual = fim;
    while (atual !== null) {
        caminho.push(atual);
        atual = anteriores[atual];
    }
    caminho.reverse();

    return { distancia: distancias[fim], caminho: caminho };
}


// ============================================================
// 3. DESENHO DO GRAFO NA TELA (SVG)
// ============================================================

const svg = document.getElementById("grafo");
const SVG_NS = "http://www.w3.org/2000/svg";

// Cria um elemento SVG com os atributos informados
function criarElemento(tipo, atributos) {
    const elemento = document.createElementNS(SVG_NS, tipo);
    for (const nome in atributos) {
        elemento.setAttribute(nome, atributos[nome]);
    }
    return elemento;
}

// Gera a lista de arestas sem repetir (RS-TA e TA-RS são a mesma aresta)
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

// Nome usado para identificar uma aresta, sempre na mesma ordem
function idAresta(a, b) {
    return a < b ? a + "-" + b : b + "-" + a;
}

function desenharGrafo() {
    const camadaArestas = criarElemento("g", {});
    const camadaCustos = criarElemento("g", {});
    const camadaVertices = criarElemento("g", {});

    // Arestas e seus custos
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

        // Ponto ao longo da linha onde o custo será escrito
        let t = posicaoDoCusto[aresta.a + "-" + aresta.b];
        if (t === undefined) {
            t = 0.5;
        }
        const x = p1.x + (p2.x - p1.x) * t;
        const y = p1.y + (p2.y - p1.y) * t;
        const largura = aresta.custo >= 10 ? 32 : 22;

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

    // Vértices (círculos com o nome)
    for (const vertice in posicoes) {
        const p = posicoes[vertice];
        const grupo = criarElemento("g", { class: "vertice", "data-vertice": vertice });

        grupo.appendChild(criarElemento("circle", { cx: p.x, cy: p.y, r: RAIO_VERTICE }));
        const texto = criarElemento("text", {
            x: p.x, y: p.y, "text-anchor": "middle", "dominant-baseline": "central"
        });
        texto.textContent = vertice;
        grupo.appendChild(texto);

        // Clicar em um vértice escolhe a origem ou o destino
        grupo.addEventListener("click", function () {
            clicarVertice(vertice);
        });

        camadaVertices.appendChild(grupo);
    }

    // A ordem importa: linhas embaixo, custos no meio, vértices por cima
    svg.appendChild(camadaArestas);
    svg.appendChild(camadaCustos);
    svg.appendChild(camadaVertices);
}

// Pinta de azul os vértices e arestas do caminho encontrado
function destacarCaminho(caminho) {
    // Primeiro remove qualquer destaque anterior
    for (const elemento of svg.querySelectorAll(".no-caminho, .extremo")) {
        elemento.classList.remove("no-caminho", "extremo");
    }

    for (let i = 0; i < caminho.length; i++) {
        const vertice = svg.querySelector('[data-vertice="' + caminho[i] + '"]');
        vertice.classList.add("no-caminho");

        // Origem e destino ganham um destaque a mais
        if (i === 0 || i === caminho.length - 1) {
            vertice.classList.add("extremo");
        }

        // Destaca a aresta entre este vértice e o próximo
        if (i < caminho.length - 1) {
            const id = idAresta(caminho[i], caminho[i + 1]);
            for (const elemento of svg.querySelectorAll('[data-aresta="' + id + '"]')) {
                elemento.classList.add("no-caminho");
            }
        }
    }
}


// ============================================================
// 4. INTERAÇÃO COM O USUÁRIO
// ============================================================

const selectOrigem = document.getElementById("origem");
const selectDestino = document.getElementById("destino");
const botaoLimpar = document.getElementById("limpar");
const resultado = document.getElementById("resultado");

// Preenche as listas de seleção com os vértices do grafo
function preencherListas() {
    for (const vertice in grafo) {
        selectOrigem.appendChild(new Option(vertice, vertice));
        selectDestino.appendChild(new Option(vertice, vertice));
    }
}

// Primeiro clique escolhe a origem, o segundo escolhe o destino
function clicarVertice(vertice) {
    if (selectOrigem.value === "" || selectDestino.value !== "") {
        selectOrigem.value = vertice;
        selectDestino.value = "";
    } else {
        selectDestino.value = vertice;
    }
    atualizar();
}

// Calcula e mostra o resultado sempre que a escolha muda
function atualizar() {
    const origem = selectOrigem.value;
    const destino = selectDestino.value;

    if (origem === "" || destino === "") {
        destacarCaminho(origem === "" ? [] : [origem]);
        resultado.innerHTML = "<p>Escolha a origem e o destino para ver o menor caminho.</p>";
        return;
    }

    const resposta = dijkstra(grafo, origem, destino);

    if (resposta.distancia === Infinity) {
        destacarCaminho([]);
        resultado.innerHTML = '<p class="erro">Não há caminho entre ' + origem + " e " + destino + ".</p>";
        return;
    }

    destacarCaminho(resposta.caminho);

    // Lista cada trecho da rota com o seu custo
    let trechos = "";
    for (let i = 0; i < resposta.caminho.length - 1; i++) {
        const a = resposta.caminho[i];
        const b = resposta.caminho[i + 1];
        trechos += "<li>" + a + " → " + b + ": " + grafo[a][b] + "</li>";
    }

    resultado.innerHTML =
        "<p>Distância mínima de " + origem + " até " + destino + ":</p>" +
        '<p class="distancia">' + resposta.distancia + "</p>" +
        '<p class="rota">Rota: ' + resposta.caminho.join(" → ") + "</p>" +
        '<ul class="trechos">' + trechos + "</ul>";
}

function limpar() {
    selectOrigem.value = "";
    selectDestino.value = "";
    atualizar();
}

selectOrigem.addEventListener("change", atualizar);
selectDestino.addEventListener("change", atualizar);
botaoLimpar.addEventListener("click", limpar);

// Inicia a página
preencherListas();
desenharGrafo();
