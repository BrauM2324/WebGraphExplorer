const formulario = document.querySelector("#formulario");
const repetir = document.querySelector("#repetir");
const pausar = document.querySelector("#pausar");
const lienzo = document.querySelector("#lienzoGrafo");
const ctx = lienzo.getContext("2d");
const estado = document.querySelector("#estado");
const tituloGrafo = document.querySelector("#tituloGrafo");
const totalNodos = document.querySelector("#totalNodos");
const totalEnlaces = document.querySelector("#totalEnlaces");
const algoritmoActivo = document.querySelector("#algoritmoActivo");
const conclusion = document.querySelector("#conclusion");
const tablaRecorrido = document.querySelector("#tablaRecorrido");
const tablaResumen = document.querySelector("#tablaResumen");

const colores = {
  BFS: "#00f5ff",
  DFS: "#ff2bd6",
  "A*": "#b6ff00",
};

let ultimoResultado = null;
let nodos = [];
let enlaces = [];
let mapaNodos = new Map();
let activos = new Map();
let animando = false;
let pausado = false;
let fisicaActiva = false;
let vista = { x: 0, y: 0, escala: 1 };
let arrastre = null;

function ajustarLienzo() {
  const rect = lienzo.getBoundingClientRect();
  const escala = window.devicePixelRatio || 1;
  lienzo.width = Math.max(1, Math.floor(rect.width * escala));
  lienzo.height = Math.max(1, Math.floor(rect.height * escala));
  ctx.setTransform(escala, 0, 0, escala, 0, 0);
}

function pantallaAMundo(x, y) {
  return {
    x: (x - vista.x) / vista.escala,
    y: (y - vista.y) / vista.escala,
  };
}

function dominio(url) {
  try {
    return new URL(url).hostname.replace(/^www\./, "");
  } catch {
    return url;
  }
}

function recortar(texto, maximo = 42) {
  if (!texto) return "";
  return texto.length > maximo ? `${texto.slice(0, maximo - 1)}...` : texto;
}

function prepararGrafo(grafo, urlInicial) {
  mapaNodos = new Map();
  enlaces = [];
  const limiteNodos = 180;
  const limiteEnlaces = 280;

  function agregarNodo(url) {
    if (!mapaNodos.has(url) && mapaNodos.size < limiteNodos) {
      const indice = mapaNodos.size;
      const angulo = indice * 2.399963;
      const radio = 80 + 11 * Math.sqrt(indice);
      mapaNodos.set(url, {
        url,
        x: lienzo.clientWidth / 2 + Math.cos(angulo) * radio,
        y: lienzo.clientHeight / 2 + Math.sin(angulo) * radio,
        vx: 0,
        vy: 0,
        central: url === urlInicial,
        visitado: false,
        relevante: false,
        algoritmos: new Set(),
      });
    }
    return mapaNodos.get(url);
  }

  agregarNodo(urlInicial);
  for (const [origen, destinos] of Object.entries(grafo)) {
    const nodoOrigen = agregarNodo(origen);
    if (!nodoOrigen) continue;
    for (const destino of destinos) {
      const nodoDestino = agregarNodo(destino);
      if (!nodoDestino || enlaces.length >= limiteEnlaces) continue;
      enlaces.push({ source: nodoOrigen, target: nodoDestino });
    }
  }

  nodos = [...mapaNodos.values()];
  vista = { x: 0, y: 0, escala: 1 };
  fisicaActiva = true;
  totalNodos.textContent = nodos.length;
  totalEnlaces.textContent = enlaces.length;
}

function simularFisica() {
  const ancho = lienzo.clientWidth;
  const alto = lienzo.clientHeight;
  const centroX = ancho / 2;
  const centroY = alto / 2;

  for (let i = 0; i < nodos.length; i += 1) {
    const a = nodos[i];
    for (let j = i + 1; j < nodos.length; j += 1) {
      const b = nodos[j];
      const dx = a.x - b.x || 0.01;
      const dy = a.y - b.y || 0.01;
      const distancia2 = dx * dx + dy * dy;
      const fuerza = Math.min(500 / distancia2, 0.4);
      a.vx += dx * fuerza;
      a.vy += dy * fuerza;
      b.vx -= dx * fuerza;
      b.vy -= dy * fuerza;
    }
  }

  for (const enlace of enlaces) {
    const dx = enlace.target.x - enlace.source.x;
    const dy = enlace.target.y - enlace.source.y;
    const distancia = Math.hypot(dx, dy) || 1;
    const fuerza = (distancia - 125) * 0.002;
    const fx = dx * fuerza;
    const fy = dy * fuerza;
    enlace.source.vx += fx;
    enlace.source.vy += fy;
    enlace.target.vx -= fx;
    enlace.target.vy -= fy;
  }

  for (const nodo of nodos) {
    const atraccion = nodo.central ? 0.04 : 0.008;
    nodo.vx += (centroX - nodo.x) * atraccion;
    nodo.vy += (centroY - nodo.y) * atraccion;
    nodo.vx *= 0.82;
    nodo.vy *= 0.82;
    nodo.x = Math.min(ancho - 24, Math.max(24, nodo.x + nodo.vx));
    nodo.y = Math.min(alto - 24, Math.max(24, nodo.y + nodo.vy));
  }
}

function dibujar() {
  const ancho = lienzo.clientWidth;
  const alto = lienzo.clientHeight;
  ctx.clearRect(0, 0, ancho, alto);
  ctx.save();
  ctx.translate(vista.x, vista.y);
  ctx.scale(vista.escala, vista.escala);

  ctx.lineWidth = 1;
  for (const enlace of enlaces) {
    const origenActivo = activos.get(enlace.source.url);
    const destinoActivo = activos.get(enlace.target.url);
    const colorEnlace = origenActivo || destinoActivo;
    ctx.strokeStyle = colorEnlace || "rgba(255,255,255,0.11)";
    ctx.shadowColor = ctx.strokeStyle;
    ctx.shadowBlur = colorEnlace ? 10 : 0;
    ctx.beginPath();
    ctx.moveTo(enlace.source.x, enlace.source.y);
    ctx.lineTo(enlace.target.x, enlace.target.y);
    ctx.stroke();
  }

  ctx.shadowBlur = 0;
  for (const nodo of nodos) {
    const colorActivo = activos.get(nodo.url);
    const radio = nodo.central ? 14 : colorActivo ? 10 : nodo.visitado ? 7 : 4;
    const color = nodo.central ? "#ffffff" : colorActivo || (nodo.relevante ? "#ffd23f" : "rgba(255,255,255,0.78)");

    if (nodo.algoritmos.size > 0) {
      const algoritmos = [...nodo.algoritmos];
      const segmento = (Math.PI * 2) / algoritmos.length;
      algoritmos.forEach((algoritmo, indice) => {
        ctx.strokeStyle = colores[algoritmo] || "#ffffff";
        ctx.shadowColor = ctx.strokeStyle;
        ctx.shadowBlur = 14;
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(nodo.x, nodo.y, radio + 6, indice * segmento, (indice + 1) * segmento - 0.08);
        ctx.stroke();
      });
    }

    ctx.fillStyle = color;
    ctx.shadowColor = color;
    ctx.shadowBlur = nodo.central || colorActivo || nodo.relevante ? 22 : 0;
    ctx.beginPath();
    ctx.arc(nodo.x, nodo.y, radio, 0, Math.PI * 2);
    ctx.fill();

    if (nodo.central || colorActivo) {
      ctx.shadowBlur = 0;
      ctx.fillStyle = "#ffffff";
      ctx.font = nodo.central ? "700 13px system-ui" : "700 11px system-ui";
      ctx.fillText(recortar(dominio(nodo.url), nodo.central ? 34 : 28), nodo.x + radio + 6, nodo.y + 4);
    }
  }
  ctx.restore();
}

function bucle() {
  if (nodos.length) {
    if (fisicaActiva) simularFisica();
    dibujar();
  } else {
    ctx.clearRect(0, 0, lienzo.clientWidth, lienzo.clientHeight);
  }
  requestAnimationFrame(bucle);
}

function llenarResumen(datos) {
  tablaResumen.innerHTML = "";
  for (const item of datos.algoritmos) {
    const fila = document.createElement("tr");
    fila.innerHTML = `
      <td>${item.algoritmo}</td>
      <td>${item.nodos_visitados}</td>
      <td>${item.profundidad}</td>
      <td>${Number(item.tiempo).toFixed(4)}</td>
      <td>${item.resultados.length}</td>
    `;
    tablaResumen.appendChild(fila);
  }
}

function agregarFila(algoritmo, paso) {
  const fila = document.createElement("tr");
  fila.className = "activo";
  fila.style.color = colores[algoritmo] || "#ffffff";
  fila.innerHTML = `
    <td>${algoritmo}</td>
    <td>${paso.order}</td>
    <td>${paso.depth}</td>
    <td><span class="chip ${paso.found ? "si" : "no"}">${paso.found ? "Si" : "No"}</span></td>
    <td class="url" title="${paso.url}">${paso.url}</td>
  `;
  tablaRecorrido.appendChild(fila);
  setTimeout(() => fila.classList.remove("activo"), 450);
}

function esperar(ms) {
  return new Promise((resolve) => {
    const inicio = performance.now();
    function revisar(ahora) {
      if (!pausado && ahora - inicio >= ms) {
        resolve();
        return;
      }
      requestAnimationFrame(revisar);
    }
    requestAnimationFrame(revisar);
  });
}

async function animarRecorridos(datos) {
  animando = true;
  pausado = false;
  fisicaActiva = true;
  repetir.disabled = true;
  pausar.disabled = false;
  pausar.textContent = "Pausar";
  tablaRecorrido.innerHTML = "";
  activos.clear();
  for (const nodo of nodos) {
    nodo.visitado = false;
    nodo.relevante = false;
    nodo.algoritmos.clear();
  }

  for (const algoritmo of datos.algoritmos) {
    algoritmoActivo.textContent = algoritmo.algoritmo;
    estado.textContent = `Recorriendo con ${algoritmo.algoritmo}`;
    const color = colores[algoritmo.algoritmo] || "#ffffff";

    for (const paso of algoritmo.recorrido) {
      const nodo = mapaNodos.get(paso.url);
      if (nodo) {
        nodo.visitado = true;
        nodo.relevante = Boolean(paso.found);
        nodo.algoritmos.add(algoritmo.algoritmo);
      }
      activos.set(paso.url, color);
      agregarFila(algoritmo.algoritmo, paso);
      await esperar(260);
      activos.delete(paso.url);
    }
    await esperar(450);
  }

  algoritmoActivo.textContent = "-";
  estado.textContent = "Recorrido finalizado";
  conclusion.textContent = datos.conclusion;
  repetir.disabled = false;
  pausar.disabled = true;
  pausado = false;
  fisicaActiva = false;
  animando = false;
}

async function buscar(evento) {
  evento.preventDefault();
  if (animando) return;

  const boton = formulario.querySelector("button");
  boton.disabled = true;
  repetir.disabled = true;
  pausar.disabled = true;
  estado.textContent = "Construyendo grafo desde la URL inicial...";
  conclusion.textContent = "Ejecutando busquedas BFS, DFS y A*. Esto puede tardar segun el sitio web.";
  tablaRecorrido.innerHTML = "";
  tablaResumen.innerHTML = "";

  const payload = {
    url_inicial: document.querySelector("#urlInicial").value,
    palabra_clave: document.querySelector("#palabraClave").value,
    max_nodos: document.querySelector("#maxNodos").value,
    max_profundidad: document.querySelector("#maxProfundidad").value,
  };

  try {
    const respuesta = await fetch("/api/buscar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const datos = await respuesta.json();
    if (!respuesta.ok) throw new Error(datos.error || "No se pudo completar la busqueda.");

    ultimoResultado = datos;
    tituloGrafo.textContent = dominio(datos.url_inicial);
    prepararGrafo(datos.grafo, datos.url_inicial);
    llenarResumen(datos);
    await animarRecorridos(datos);
  } catch (error) {
    estado.textContent = "Ocurrio un problema";
    conclusion.textContent = error.message;
  } finally {
    boton.disabled = false;
  }
}

formulario.addEventListener("submit", buscar);
repetir.addEventListener("click", () => {
  if (ultimoResultado && !animando) {
    animarRecorridos(ultimoResultado);
  }
});

pausar.addEventListener("click", () => {
  if (!animando) return;
  pausado = !pausado;
  fisicaActiva = !pausado;
  pausar.textContent = pausado ? "Reanudar" : "Pausar";
  estado.textContent = pausado ? "Animacion pausada" : `Recorriendo con ${algoritmoActivo.textContent}`;
});

lienzo.addEventListener("wheel", (evento) => {
  evento.preventDefault();
  const rect = lienzo.getBoundingClientRect();
  const mouseX = evento.clientX - rect.left;
  const mouseY = evento.clientY - rect.top;
  const antes = pantallaAMundo(mouseX, mouseY);
  const factor = evento.deltaY < 0 ? 1.12 : 0.88;
  vista.escala = Math.min(3, Math.max(0.35, vista.escala * factor));
  vista.x = mouseX - antes.x * vista.escala;
  vista.y = mouseY - antes.y * vista.escala;
});

lienzo.addEventListener("pointerdown", (evento) => {
  lienzo.setPointerCapture(evento.pointerId);
  const rect = lienzo.getBoundingClientRect();
  const punto = pantallaAMundo(evento.clientX - rect.left, evento.clientY - rect.top);
  const nodo = [...nodos].reverse().find((item) => Math.hypot(item.x - punto.x, item.y - punto.y) < 18);
  arrastre = nodo
    ? { tipo: "nodo", nodo, dx: punto.x - nodo.x, dy: punto.y - nodo.y }
    : { tipo: "vista", x: evento.clientX, y: evento.clientY, origenX: vista.x, origenY: vista.y };
});

lienzo.addEventListener("pointermove", (evento) => {
  if (!arrastre) return;
  if (arrastre.tipo === "vista") {
    vista.x = arrastre.origenX + evento.clientX - arrastre.x;
    vista.y = arrastre.origenY + evento.clientY - arrastre.y;
    return;
  }

  const rect = lienzo.getBoundingClientRect();
  const punto = pantallaAMundo(evento.clientX - rect.left, evento.clientY - rect.top);
  arrastre.nodo.x = punto.x - arrastre.dx;
  arrastre.nodo.y = punto.y - arrastre.dy;
  arrastre.nodo.vx = 0;
  arrastre.nodo.vy = 0;
});

lienzo.addEventListener("pointerup", () => {
  arrastre = null;
});

lienzo.addEventListener("pointercancel", () => {
  arrastre = null;
});

window.addEventListener("resize", () => {
  ajustarLienzo();
  if (ultimoResultado) prepararGrafo(ultimoResultado.grafo, ultimoResultado.url_inicial);
});

ajustarLienzo();
bucle();
