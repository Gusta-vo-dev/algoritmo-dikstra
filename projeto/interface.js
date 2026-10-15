// ============================================================
// 1. DADOS DO GRAFO
// ============================================================

// O grafo e o cálculo do menor caminho ficam no Python (dijkstra.py).
// A página pede os dados ao servidor do dijkstra.py quando abre.
let grafo = {};

// Nome da cidade que cada sigla representa
const nomes = {
    RS: "Rio do Sul",
    TA: "Taió",
    LA: "Laurentino",
    SA: "Salete",
    RO: "Rio do Oeste",
    TC: "Trombudo Central",
    AG: "Agronômica",
    LO: "Lontras",
    PG: "Presidente Getúlio",
    WI: "Witmarsum",
    AU: "Aurora",
    VR: "Vidal Ramos",
    PR: "Pouso Redondo",
    IB: "Ibirama",
    IT: "Ituporanga"
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
// 2. COMUNICAÇÃO COM O PYTHON (dijkstra.py)
// ============================================================

// Pede ao servidor o grafo definido no dijkstra.py
async function buscarGrafo() {
    const resposta = await fetch("/grafo");
    return await resposta.json();
}

// Pede ao servidor o menor caminho, calculado pela função
// dijkstra_ponto_a_ponto do dijkstra.py
async function calcularNoPython(origem, destino) {
    const resposta = await fetch("/calcular?origem=" + origem + "&destino=" + destino);
    return await resposta.json();
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

        // Nome da cidade logo abaixo do círculo
        const nomeCidade = criarElemento("text", {
            x: p.x, y: p.y + RAIO_VERTICE + 20, "text-anchor": "middle", class: "nome-cidade"
        });
        nomeCidade.textContent = nomes[vertice];
        grupo.appendChild(nomeCidade);

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
        const texto = vertice + " - " + nomes[vertice];
        selectOrigem.appendChild(new Option(texto, vertice));
        selectDestino.appendChild(new Option(texto, vertice));
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
async function atualizar() {
    const origem = selectOrigem.value;
    const destino = selectDestino.value;

    if (origem === "" || destino === "") {
        destacarCaminho(origem === "" ? [] : [origem]);
        resultado.innerHTML = "<p>Escolha a origem e o destino para ver o menor caminho.</p>";
        return;
    }

    const resposta = await calcularNoPython(origem, destino);

    // O Python devolve distância vazia (null) quando não existe caminho
    if (resposta.distancia === null) {
        destacarCaminho([]);
        resultado.innerHTML = '<p class="erro">Não há caminho entre ' + nomes[origem] + " e " + nomes[destino] + ".</p>";
        return;
    }

    destacarCaminho(resposta.caminho);

    // Lista cada trecho da rota com o seu custo
    let trechos = "";
    for (let i = 0; i < resposta.caminho.length - 1; i++) {
        const a = resposta.caminho[i];
        const b = resposta.caminho[i + 1];
        trechos += "<li>" + nomes[a] + " → " + nomes[b] + ": " + grafo[a][b] + "</li>";
    }

    // Troca cada sigla do caminho pelo nome da cidade
    const nomesDoCaminho = resposta.caminho.map(function (vertice) {
        return nomes[vertice];
    });

    resultado.innerHTML =
        "<p>Distância mínima de " + nomes[origem] + " até " + nomes[destino] + ":</p>" +
        '<p class="distancia">' + resposta.distancia + "</p>" +
        '<p class="rota">Rota: ' + nomesDoCaminho.join(" → ") + "</p>" +
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

// Inicia a página: busca o grafo no Python e depois desenha
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
