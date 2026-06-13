# -*- coding: utf-8 -*-
"""
MurgiCapital · Simulador profesional de carteras (Monte Carlo)
==============================================================
Versión 2. Novedades respecto a la v1:

  1. DATOS MULTI-FUENTE: catálogo de activos populares (MSCI World, índices,
     ETFs, oro, bonos...), buscador por nombre (API de búsqueda de Yahoo) y
     descarga con respaldo automático en Stooq si Yahoo falla.
  2. TRES MOTORES DE SIMULACIÓN:
       - Merton con saltos (modelo principal; reproduce el notebook original)
       - Bootstrap histórico por bloques (no paramétrico: remuestrea días
         reales conservando correlaciones y crisis conjuntas)
       - Ensemble: mezcla 50/50 de ambos (reduce el riesgo de modelo)
  3. IDENTIDAD MURGICAPITAL: logo, icono y paleta corporativa
     (azul marino #1E3A6B, gris #8E9194, dorado #C8A45C).

El archivo app.py es solo el punto de entrada; todo el código vive aquí.
"""

import gc
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib
matplotlib.use("Agg")            # backend headless: sin GUI, memoria predecible en el servidor
import matplotlib.pyplot as plt
import yfinance as yf

# ============================================================================
# IDENTIDAD CORPORATIVA
# ============================================================================

AZUL    = "#1E3A6B"   # azul marino del escudo
GRIS    = "#8E9194"   # gris del logotipo
DORADO  = "#C8A45C"   # detalle dorado del escudo
FONDO_2 = "#F4F6FA"

_AQUI = Path(__file__).parent
LOGO_PATH = _AQUI / "assets" / "logo.png"
ICON_PATH = _AQUI / "assets" / "icon.png"

st.set_page_config(
    page_title="MurgiCapital | Simulador de carteras",
    page_icon=str(ICON_PATH) if ICON_PATH.exists() else "📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS corporativo: titulares en azul marino, acentos dorados, sin elementos
# de Streamlit que delaten la plantilla (menú y footer ocultos).
st.markdown(f"""
<style>
    #MainMenu, footer {{visibility: hidden;}}
    h1, h2, h3 {{color: {AZUL} !important; font-family: Georgia, 'Times New Roman', serif;}}
    [data-testid="stMetricValue"] {{color: {AZUL};}}
    [data-testid="stMetricLabel"] {{color: {GRIS};}}
    [data-testid="stSidebar"] {{background-color: {FONDO_2};}}
    .stTabs [aria-selected="true"] {{color: {AZUL}; border-bottom-color: {DORADO} !important;}}
    .murgi-footer {{color: {GRIS}; font-size: 0.8rem; text-align: center;
                    border-top: 1px solid {FONDO_2}; padding-top: 0.8rem; margin-top: 2rem;}}
</style>
""", unsafe_allow_html=True)

if LOGO_PATH.exists():
    st.logo(str(LOGO_PATH), size="large")

# ============================================================================
# CATÁLOGO DE ACTIVOS — los más demandados, con su ticker ya resuelto
# ============================================================================

CATALOGO = {
    "MSCI World — iShares Core (EUR, Ámsterdam)":      "IWDA.AS",
    "MSCI World — iShares Core (EUR, Xetra)":          "EUNL.DE",
    "MSCI World — iShares (USD, NY)":                  "URTH",
    "FTSE All-World — Vanguard VWCE (EUR)":            "VWCE.DE",
    "S&P 500 — índice":                                "^GSPC",
    "S&P 500 — Vanguard VOO (USD)":                    "VOO",
    "Nasdaq 100 — índice":                             "^NDX",
    "EuroStoxx 50 — índice":                           "^STOXX50E",
    "IBEX 35 — índice":                                "^IBEX",
    "MSCI Emerging Markets — iShares (USD)":           "EEM",
    "Oro — futuro COMEX":                              "GC=F",
    "Oro físico — Invesco Physical Gold (EUR)":        "8PSG.DE",
    "Bonos zona euro — iShares Core Aggregate (EUR)":  "IEAG.AS",
    "Bonos globales — iShares Core US Aggregate":      "AGG",
    "Bono EEUU 20+ años — iShares TLT":                "TLT",
    "Bitcoin (USD)":                                   "BTC-USD",
    "REIT global — iShares Developed Property":        "IWDP.AS",
}

# ============================================================================
# CAPA DE DATOS MULTI-FUENTE
#   1º Yahoo Finance (yfinance)  →  2º Stooq (CSV público, sin clave)
# ============================================================================

# Equivalencias de símbolos de índices entre Yahoo y Stooq
_MAPA_STOOQ = {
    "^GSPC": "^spx", "^NDX": "^ndx", "^DJI": "^dji", "^IBEX": "^ibex",
    "^STOXX50E": "^sx5e", "^GDAXI": "^dax", "^FTSE": "^ftm", "^N225": "^nkx",
}


def _descarga_yahoo(ticker, start, end):
    """Intenta descargar el cierre desde Yahoo Finance."""
    d = yf.download(ticker, start=start, end=end, progress=False)
    if d is None or len(d) == 0:
        return None
    s = d["Close"].squeeze()
    return s if len(s) > 0 else None


def _descarga_stooq(ticker, start, end):
    """Respaldo: descarga desde Stooq (https://stooq.com), que cubre índices,
    ETFs europeos y americanos. Prueba varias convenciones de símbolo."""
    candidatos = []
    if ticker in _MAPA_STOOQ:
        candidatos.append(_MAPA_STOOQ[ticker])
    base = ticker.lower()
    candidatos += [base, base.split(".")[0] + ".us"]
    for sym in dict.fromkeys(candidatos):          # sin duplicados, en orden
        try:
            url = f"https://stooq.com/q/d/l/?s={sym}&i=d"
            d = pd.read_csv(url, parse_dates=["Date"], index_col="Date")
            if len(d) > 0 and "Close" in d.columns:
                s = d["Close"]
                s = s[(s.index >= pd.Timestamp(start)) & (s.index <= pd.Timestamp(end))]
                if len(s) > 0:
                    return s
        except Exception:
            continue
    return None


@st.cache_data(show_spinner=False, ttl=3600)
def descargar_precios(tickers, start, end):
    """Descarga cada activo probando Yahoo y después Stooq.
    Devuelve (tabla de precios en días comunes, dict ticker→fuente usada)."""
    series, fuentes, fallos = {}, {}, []
    for tk in tickers:
        s = None
        try:
            s = _descarga_yahoo(tk, start, end)
            if s is not None:
                fuentes[tk] = "Yahoo Finance"
        except Exception:
            s = None
        if s is None:
            try:
                s = _descarga_stooq(tk, start, end)
                if s is not None:
                    fuentes[tk] = "Stooq"
            except Exception:
                s = None
        if s is None:
            fallos.append(tk)
        else:
            series[tk] = s
    if fallos:
        raise ValueError(
            f"No se encontraron datos para: {', '.join(fallos)}. "
            "Usa el buscador por nombre (panel lateral) o consulta el símbolo en "
            "finance.yahoo.com o stooq.com."
        )
    precios = pd.DataFrame(series).dropna()
    if len(precios) < 252:
        raise ValueError(
            "Hay menos de un año de historia común entre los activos elegidos. "
            "Amplía las fechas o sustituye el activo con menos historia "
            "(la tabla 'Datos utilizados' indica cuál limita)."
        )
    return precios, fuentes


@st.cache_data(show_spinner=False, ttl=3600)
def buscar_activos(consulta):
    """Busca activos por nombre ('msci world', 'vanguard sp500'...) usando la
    API de búsqueda de Yahoo. Devuelve una lista de resultados legibles."""
    resultados = []
    try:                                            # vía yfinance (versiones recientes)
        from yfinance import Search
        for q in Search(consulta, max_results=12).quotes:
            resultados.append({
                "Símbolo": q.get("symbol", ""),
                "Nombre": q.get("shortname") or q.get("longname") or "",
                "Tipo": q.get("quoteType", ""),
                "Bolsa": q.get("exchange", ""),
            })
    except Exception:
        try:                                        # vía petición directa
            import requests
            r = requests.get(
                "https://query2.finance.yahoo.com/v1/finance/search",
                params={"q": consulta, "quotesCount": 12, "newsCount": 0},
                headers={"User-Agent": "Mozilla/5.0"}, timeout=10,
            ).json()
            for q in r.get("quotes", []):
                resultados.append({
                    "Símbolo": q.get("symbol", ""),
                    "Nombre": q.get("shortname") or q.get("longname") or "",
                    "Tipo": q.get("quoteType", ""),
                    "Bolsa": q.get("exchange", ""),
                })
        except Exception:
            pass
    return resultados


# ============================================================================
# NÚCLEO DE SIMULACIÓN — tres motores
# ============================================================================

def calibrar(retornos_activo, n_sigmas=3.0):
    """Calibración de Merton por umbral: separa días 'normales' de días de
    'salto' (caídas más allá de mu - n_sigmas·sigma). Idéntica al notebook."""
    mu_diario = np.mean(retornos_activo)
    sigma_diario = np.std(retornos_activo)
    umbral = mu_diario - n_sigmas * sigma_diario
    saltos = retornos_activo[retornos_activo < umbral]
    normales = retornos_activo[retornos_activo >= umbral]
    sigma = np.std(normales) * np.sqrt(252)
    mu = np.mean(normales) * 252 + 0.5 * sigma**2
    lambda_ = len(saltos) / (len(retornos_activo) / 252)
    mu_J = np.mean(saltos) if len(saltos) > 0 else 0.0
    sigma_J = np.std(saltos) if len(saltos) > 1 else 0.0
    return mu, sigma, lambda_, mu_J, sigma_J


def simular_merton(mu, sigma, lam, mu_J, sigma_J, L, T, M, seed,
                   S0=100.0, phi_comun=0.0):
    """Difusión correlacionada (Cholesky) + saltos de Poisson.
    Con phi_comun > 0, esa fracción de la intensidad mínima de salto es
    sistémica (todos los activos saltan a la vez): escenario prudente.
    Con phi_comun = 0 reproduce exactamente la secuencia del notebook."""
    np.random.seed(seed)
    dt = 1 / 252
    N = int(T / dt)
    n_act = len(mu)
    precio = np.zeros((M, N + 1, n_act), dtype=np.float32)
    precio[:, 0, :] = S0
    drift = (mu - 0.5 * sigma**2) * dt
    vol = sigma * np.sqrt(dt)
    lam_sys = phi_comun * lam.min()
    lam_idio = lam - lam_sys
    for t in range(1, N + 1):
        Z = np.random.randn(M, n_act) @ L.T
        if lam_sys > 0:
            n_j = (np.random.poisson(lam_idio * dt, size=(M, n_act))
                   + np.random.poisson(lam_sys * dt, size=(M, 1)))
        else:
            n_j = np.random.poisson(lam * dt, size=(M, n_act))
        Zj = np.random.randn(M, n_act)
        log_salto = n_j * mu_J + np.sqrt(n_j) * sigma_J * Zj
        precio[:, t, :] = precio[:, t - 1, :] * np.exp(drift + vol * Z + log_salto).astype(np.float32)
    return precio


def simular_bootstrap(retornos, T, M, seed, bloque=21, S0=100.0):
    """Bootstrap histórico por bloques: remuestrea bloques de ~1 mes de
    retornos diarios REALES de todos los activos a la vez. Al copiar días
    reales conjuntos, conserva correlaciones, colas pesadas, rachas de
    volatilidad y crisis simultáneas (2008, COVID) sin asumir ningún modelo."""
    np.random.seed(seed)
    R = retornos.astype(np.float32)                 # (D, n) retornos log diarios
    D, n_act = R.shape
    N = int(T * 252)
    n_bloques = N // bloque + 1
    precio = np.empty((M, N + 1, n_act), dtype=np.float32)
    precio[:, 0, :] = S0
    paso = 1000                                     # por trozos para cuidar la memoria
    for i0 in range(0, M, paso):
        m = min(paso, M - i0)
        inicios = np.random.randint(0, D - bloque + 1, size=(m, n_bloques))
        idx = (inicios[:, :, None] + np.arange(bloque)[None, None, :]).reshape(m, -1)[:, :N]
        r = R[idx]                                  # (m, N, n_act)
        np.cumsum(r, axis=1, out=r)
        precio[i0:i0 + m, 1:, :] = S0 * np.exp(r)
    return precio


def metricas_riesgo(valor_final, S0=100.0):
    """VaR y CVaR al 95% y 99% como pérdida sobre lo invertido."""
    perdida = (S0 - valor_final) / S0
    out = {}
    for nivel in (95, 99):
        v = np.percentile(perdida, nivel)
        out[f"VaR{nivel}"] = v
        out[f"CVaR{nivel}"] = np.mean(perdida[perdida >= v])
    return out


def max_drawdown(trayectorias):
    """Mayor caída desde máximos de cada trayectoria."""
    cummax = np.maximum.accumulate(trayectorias, axis=1)
    dd = (cummax - trayectorias) / cummax
    return dd.max(axis=1)


def formato_euro(x):
    return f"{x:,.0f} €".replace(",", ".")


def mostrar_figura(fig):
    """Renderiza una figura de Matplotlib y la cierra de inmediato.

    Cerrar la figura es imprescindible en Streamlit: la interfaz pyplot
    retiene en memoria cada figura hasta cerrarla explícitamente. Como el
    script se re-ejecuta entero en cada interacción (cambiar de modelo,
    pulsar un botón…), las figuras no cerradas se acumulan sin límite hasta
    agotar la RAM del servidor (Streamlit Cloud impone ~1 GB). Esa fuga era
    la causa de la 'pantalla en blanco' al re-simular tras cambiar de modelo.
    """
    st.pyplot(fig, width="stretch")
    plt.close(fig)


# ============================================================================
# PANEL LATERAL
# ============================================================================

st.sidebar.markdown(f"<h2 style='color:{AZUL};margin-bottom:0'>Configuración</h2>", unsafe_allow_html=True)

st.sidebar.markdown("**1 · Activos de la cartera**")
seleccion_catalogo = st.sidebar.multiselect(
    "Elige del catálogo",
    options=list(CATALOGO.keys()),
    default=["S&P 500 — índice", "Bonos zona euro — iShares Core Aggregate (EUR)", "Oro — futuro COMEX"],
    help="Activos verificados con su símbolo ya resuelto. Puedes añadir otros abajo.",
)
tickers_extra = st.sidebar.text_input(
    "Otros símbolos (separados por comas)", value="",
    help="Cualquier símbolo de Yahoo Finance o Stooq, por ejemplo AAPL, VUSA.AS, SWDA.MI",
)

with st.sidebar.expander("¿No encuentras un activo? Búscalo por nombre"):
    consulta = st.text_input("Nombre del fondo, ETF o índice", placeholder="ej.: msci world acumulación")
    if consulta:
        encontrados = buscar_activos(consulta)
        if encontrados:
            st.dataframe(pd.DataFrame(encontrados), hide_index=True, height=220)
            st.caption("Copia el símbolo en el campo 'Otros símbolos'. "
                       "Sufijos habituales: .AS Ámsterdam · .DE Alemania · .MI Milán · sin sufijo, EEUU.")
        else:
            st.warning("Sin resultados desde esta red. Busca el símbolo en finance.yahoo.com, "
                       "stooq.com o justetf.com (con el ISIN del fondo) y pégalo en 'Otros símbolos'.")

st.sidebar.markdown("**2 · Periodo histórico de aprendizaje**")
c1, c2 = st.sidebar.columns(2)
fecha_inicio = c1.date_input("Desde", value=pd.Timestamp("1990-01-01"), min_value=pd.Timestamp("1950-01-01"))
fecha_fin = c2.date_input("Hasta", value=pd.Timestamp.today())

st.sidebar.markdown("**3 · Plan de inversión**")
T = st.sidebar.slider("Años de horizonte", 1, 40, 20)
aporte_inicial = st.sidebar.number_input("Aportación inicial (€)", min_value=0, value=600, step=100)
aporte_mensual = st.sidebar.number_input("Aportación mensual (€)", min_value=0, value=300, step=50)

with st.sidebar.expander("4 · Costes, impuestos e inflación"):
    comision_aporte = st.number_input("Comisión por aporte (%)", 0.0, 5.0, 0.1, 0.05) / 100
    tipo_impositivo = st.number_input("Impuesto sobre la ganancia (%)", 0.0, 60.0, 21.0, 1.0) / 100
    inflacion_anual = st.number_input("Inflación anual estimada (%)", 0.0, 15.0, 2.0, 0.5) / 100

with st.sidebar.expander("5 · Motor de simulación y ajustes"):
    motor = st.radio(
        "Motor",
        ["Merton con saltos (principal)", "Bootstrap histórico", "Ensemble (Merton + Bootstrap)"],
        help="Merton: modelo paramétrico con desplomes súbitos (reproduce el estudio de referencia). "
             "Bootstrap: remuestrea meses reales de la historia, crisis incluidas. "
             "Ensemble: mitad de escenarios con cada motor; reduce la dependencia de un único modelo.",
    )
    M = st.select_slider("Número de escenarios", options=[1000, 2000, 3000, 5000, 10000], value=3000)
    n_sigmas = st.slider("Umbral de detección de crisis (σ)", 2.0, 4.0, 3.0, 0.5)
    rf_pct = st.number_input("Tipo de interés sin riesgo (%)", 0.0, 10.0, 2.193, 0.1)
    seed = st.number_input("Semilla aleatoria", 0, 99999, 42)
    saltos_comunes = st.checkbox(
        "Escenario prudente: crisis simultáneas entre activos", value=False,
        help="Sólo afecta al motor Merton. El bootstrap ya recoge crisis conjuntas por construcción.",
    )

RF = np.log(1 + rf_pct / 100)
ejecutar = st.sidebar.button("Ejecutar simulación", type="primary", width="stretch")
st.sidebar.caption("Herramienta educativa de MurgiCapital. No constituye asesoramiento financiero.")

# Firma de la configuración actual. Permite detectar que los resultados en
# pantalla pertenecen a una ejecución previa cuando el usuario cambia un ajuste
# (por ejemplo, el modelo) sin volver a pulsar "Ejecutar simulación".
firma_config = (
    tuple(seleccion_catalogo), tickers_extra.strip(), str(fecha_inicio), str(fecha_fin),
    int(T), int(aporte_inicial), int(aporte_mensual),
    round(float(comision_aporte), 6), round(float(tipo_impositivo), 6),
    round(float(inflacion_anual), 6), motor, int(M), float(n_sigmas), float(rf_pct),
    int(seed), bool(saltos_comunes),
)

# ============================================================================
# CABECERA
# ============================================================================

st.title("Simulador de carteras MurgiCapital")
st.markdown(
    f"<p style='color:{GRIS};font-size:1.05rem'>Análisis Monte Carlo de carteras de inversión: "
    "miles de escenarios de futuro construidos a partir del comportamiento histórico real de los "
    "activos, incluyendo crisis y desplomes. Resultados netos de comisiones, impuestos e inflación.</p>",
    unsafe_allow_html=True,
)

if not ejecutar and "resultados" not in st.session_state:
    st.info("Configure su cartera y su plan en el panel lateral y pulse **Ejecutar simulación**.")
    st.stop()

# ============================================================================
# CÁLCULO
# ============================================================================

if ejecutar:
    tickers = [CATALOGO[k] for k in seleccion_catalogo]
    tickers += [t.strip().upper() for t in tickers_extra.split(",") if t.strip()]
    tickers = list(dict.fromkeys(tickers))          # sin duplicados, en orden
    if len(tickers) < 2:
        st.error("Elija al menos dos activos (del catálogo o por símbolo).")
        st.stop()

    try:
        with st.spinner("Descargando datos históricos (Yahoo Finance y Stooq)…"):
            precios_hist, fuentes = descargar_precios(tuple(tickers), str(fecha_inicio), str(fecha_fin))
    except Exception as e:
        st.error(f"Problema con los datos: {e}")
        st.stop()

    retornos_df = np.log(precios_hist / precios_hist.shift(1))
    retornos_df = retornos_df.replace([np.inf, -np.inf], np.nan).dropna()
    if len(retornos_df) < 60:
        st.error(
            "Tras descartar precios no válidos quedan muy pocas observaciones comunes a todos "
            "los activos. Amplíe el periodo histórico o sustituya el activo con menos historia."
        )
        st.stop()
    n_act = len(tickers)

    # --- Salvaguarda de memoria (Streamlit Cloud impone ~1 GB de RAM) ---------
    # El array de precios es solo una parte del consumo: la optimización de
    # cartera, el plan de aportaciones y el cálculo de drawdown crean arrays
    # adicionales. El estimador anterior solo miraba 'precio' e infravaloraba
    # el pico real (~2,5-3x), por lo que dejaba pasar combinaciones que
    # tumbaban el servidor. Aproximamos el pico realista: precio × (1 + 3/n).
    N_pasos = int(T * 252) + 1
    precio_mb = M * N_pasos * n_act * 4 / 1e6
    pico_estimado_mb = precio_mb * (1 + 3.0 / n_act)
    PRESUPUESTO_MB = 600                 # margen prudente bajo el límite de 1 GB
    if pico_estimado_mb > PRESUPUESTO_MB:
        denom = (N_pasos * n_act * 4 / 1e6) * (1 + 3.0 / n_act)
        M_sugerido = max(1000, int(PRESUPUESTO_MB / denom) // 1000 * 1000)
        st.error(
            f"Esta combinación ({M:,} escenarios × {T} años × {n_act} activos) puede agotar la "
            f"memoria del servidor (pico estimado ≈ {pico_estimado_mb:,.0f} MB; límite ~1 GB en "
            f"Streamlit Cloud). Reduzca a unos {M_sugerido:,} escenarios, acorte el horizonte o "
            f"use menos activos.".replace(",", ".")
        )
        st.stop()

    # --- Calibración Merton (también se muestra como información del activo) ---
    parametros = [calibrar(retornos_df[tk].values, n_sigmas) for tk in tickers]
    mu_v, sigma_v, lam_v, mu_J_v, sigma_J_v = [np.array(x) for x in zip(*parametros)]

    corr = retornos_df.corr().values
    try:
        L = np.linalg.cholesky(corr)
    except np.linalg.LinAlgError:
        L = np.linalg.cholesky(corr + 1e-8 * np.eye(n_act))

    # --- Simulación según el motor elegido ---
    phi = 0.5 if saltos_comunes else 0.0
    with st.spinner(f"Generando {M:,} escenarios de {T} años…".replace(",", ".")):
        if motor == "Merton con saltos (principal)":
            precio = simular_merton(mu_v, sigma_v, lam_v, mu_J_v, sigma_J_v, L,
                                    T=T, M=M, seed=int(seed), phi_comun=phi)
        elif motor == "Bootstrap histórico":
            precio = simular_bootstrap(retornos_df.values, T=T, M=M, seed=int(seed))
        else:                                       # Ensemble 50/50
            M1 = M - M // 2
            p1 = simular_merton(mu_v, sigma_v, lam_v, mu_J_v, sigma_J_v, L,
                                T=T, M=M1, seed=int(seed), phi_comun=phi)
            p2 = simular_bootstrap(retornos_df.values, T=T, M=M // 2, seed=int(seed) + 1)
            precio = np.concatenate([p1, p2], axis=0)
            del p1, p2

    # --- Optimización de cartera por muestreo Dirichlet, evaluada por bloques ---
    n_carteras = 10000
    pesos = np.random.dirichlet(np.ones(n_act), size=n_carteras)
    precio_final = precio[:, -1, :]
    vol_cart = np.empty(n_carteras)
    ret_cart = np.empty(n_carteras)
    BLOQUE = 500
    for i in range(0, n_carteras, BLOQUE):
        v_blq = precio_final @ pesos[i:i + BLOQUE].T.astype(np.float32)
        rl = np.log(v_blq / 100.0)
        vol_cart[i:i + BLOQUE] = rl.std(axis=0) / np.sqrt(T)
        ret_cart[i:i + BLOQUE] = rl.mean(axis=0) / T
    sharpes = (ret_cart - RF) / vol_cart
    idx_ms, idx_mv = int(np.argmax(sharpes)), int(np.argmin(vol_cart))
    valor_ms = (precio_final @ pesos[idx_ms].astype(np.float32)).astype(np.float64)
    valor_mv = (precio_final @ pesos[idx_mv].astype(np.float32)).astype(np.float64)

    # --- Plan de aportaciones (DCA): horizonte y validación de aportes --------
    dias_por_mes = 21
    N = precio.shape[1] - 1
    fechas_aporte = np.arange(dias_por_mes, N + 1, dias_por_mes)
    n_aportes = len(fechas_aporte)
    total_aportado = aporte_inicial + n_aportes * aporte_mensual
    if total_aportado <= 0:
        st.error("Introduzca una aportación inicial o mensual mayor que cero.")
        st.stop()

    # Se calculan AQUÍ todas las magnitudes que dependen de 'precio' (el array
    # más grande) para poder liberarlo de inmediato y rebajar el pico de memoria.
    w_opt = pesos[idx_ms].astype(np.float32)
    valor_cartera = precio @ w_opt                       # (M, N+1) mejor equilibrio
    traj_mv = precio @ pesos[idx_mv].astype(np.float32)  # (M, N+1) conservadora
    ret_sim_1d = np.log(precio[:, 1:min(253, N + 1), 0] / precio[:, 0:min(252, N), 0]).flatten()

    del precio, precio_final                             # liberar el array grande cuanto antes
    gc.collect()

    # --- DCA vectorizado (forma cerrada, sin bucle día a día) -----------------
    # El patrimonio con aportaciones periódicas admite forma cerrada exacta:
    #   W[t] = V[t] · ( A0/V[0] + Σ_{aportes s≤t} a/V[s] )
    # con V = valor de la cartera, A0 = aporte inicial neto, a = aporte mensual
    # neto. Es idéntico al bucle original pero en una sola pasada vectorizada
    # (se eliminan ~5.000 iteraciones de Python por simulación).
    aporte_neto_mes = aporte_mensual * (1 - comision_aporte)
    coef = np.zeros((M, N + 1), dtype=np.float64)
    coef[:, 0] = (aporte_inicial * (1 - comision_aporte)) / valor_cartera[:, 0]
    if n_aportes:
        coef[:, fechas_aporte] += aporte_neto_mes / valor_cartera[:, fechas_aporte]
    np.cumsum(coef, axis=1, out=coef)
    W = (valor_cartera * coef).astype(np.float32)        # patrimonio nominal (M, N+1)
    del coef

    W_nominal = W[:, -1].astype(np.float64)
    impuesto = np.maximum(0, W_nominal - total_aportado) * tipo_impositivo
    W_real = (W_nominal - impuesto) / (1 + inflacion_anual) ** T

    # --- Alternativa lump-sum (mismo dinero, todo el día 0) ---
    ls_nominal = (total_aportado * (1 - comision_aporte) * valor_cartera[:, -1] / valor_cartera[:, 0]).astype(np.float64)
    ls_real = (ls_nominal - np.maximum(0, ls_nominal - total_aportado) * tipo_impositivo) / (1 + inflacion_anual) ** T

    # --- Riesgo ---
    riesgo_ms = metricas_riesgo(valor_ms)
    riesgo_mv = metricas_riesgo(valor_mv)
    dd_ms = max_drawdown(valor_cartera)
    dd_mv = max_drawdown(traj_mv)

    del valor_cartera, traj_mv                      # liberar memoria del servidor
    gc.collect()

    st.session_state["resultados"] = dict(
        tickers=tickers, fuentes=fuentes, motor=motor, parametros=parametros,
        corr=retornos_df.corr(),
        retornos_hist_1=retornos_df[tickers[0]].values, ret_sim_1d=ret_sim_1d,
        pesos_ms=pesos[idx_ms], pesos_mv=pesos[idx_mv],
        vol_cart=vol_cart, ret_cart=ret_cart, sharpes=sharpes, idx_ms=idx_ms, idx_mv=idx_mv,
        valor_ms=valor_ms, valor_mv=valor_mv,
        riesgo_ms=riesgo_ms, riesgo_mv=riesgo_mv, dd_ms=dd_ms, dd_mv=dd_mv,
        W_paths=W[::max(1, M // 200)].astype(np.float64), W_real=W_real, ls_real=ls_real,
        total_aportado=total_aportado, T=T, RF=RF, n_aportes=n_aportes,
        fechas_aporte=fechas_aporte, aporte_inicial=aporte_inicial, aporte_mensual=aporte_mensual,
        rango_datos=(precios_hist.index[0].date(), precios_hist.index[-1].date()),
        n_dias=len(precios_hist), saltos_comunes=saltos_comunes,
        firma=firma_config,
    )

r = st.session_state["resultados"]
tickers, T = r["tickers"], r["T"]

# Aviso de resultados obsoletos: la configuración del panel ya no coincide con
# la de la última simulación mostrada.
if not ejecutar and r.get("firma") != firma_config:
    st.warning(
        "Has cambiado la configuración (por ejemplo, el modelo de simulación) desde la última "
        "ejecución. Los resultados que se muestran corresponden a la simulación anterior; "
        "pulsa **Ejecutar simulación** para recalcular con los nuevos ajustes."
    )

# ============================================================================
# RESULTADOS
# ============================================================================

tab_resumen, tab_cartera, tab_riesgo, tab_plan, tab_valida, tab_metodo = st.tabs(
    ["Resumen", "Cartera óptima", "Análisis de riesgo", "Plan de ahorro", "Validación del modelo", "Metodología"]
)

# ---------------------------------------------------------------- RESUMEN
with tab_resumen:
    st.subheader("Conclusiones principales")
    med_real = np.median(r["W_real"])
    p_perder = np.mean(r["W_real"] < r["total_aportado"])
    c1, c2, c3 = st.columns(3)
    c1.metric("Capital aportado en total", formato_euro(r["total_aportado"]))
    c2.metric(f"Resultado típico a {T} años (en € de hoy)", formato_euro(med_real),
              delta=formato_euro(med_real - r["total_aportado"]))
    c3.metric("Probabilidad de perder poder adquisitivo", f"{p_perder:.1%}", delta_color="inverse")
    st.caption("El resultado típico es la mediana: la mitad de los escenarios termina mejor y la otra mitad peor. "
               "Importes en euros de hoy, descontadas comisiones, impuestos e inflación.")

    st.markdown("**Distribución recomendada de la cartera** (mejor relación rentabilidad/riesgo):")
    cols = st.columns(len(tickers))
    for c, tk, w in zip(cols, tickers, r["pesos_ms"]):
        c.metric(tk, f"{w:.0%}")

    with st.expander("Datos utilizados"):
        st.markdown(
            f"- Periodo: **{r['rango_datos'][0]} → {r['rango_datos'][1]}** "
            f"({r['n_dias']} sesiones comunes a todos los activos)\n"
            f"- Motor de simulación: **{r['motor']}**"
            + ("\n- Escenario prudente de crisis simultáneas: **activado**" if r["saltos_comunes"] else "")
        )
        st.dataframe(pd.DataFrame(
            {"Activo": list(r["fuentes"].keys()), "Fuente de datos": list(r["fuentes"].values())}
        ), hide_index=True)

# ---------------------------------------------------------------- CARTERA
with tab_cartera:
    st.subheader("Frontera eficiente: 10.000 combinaciones de cartera")
    st.markdown(
        "Cada punto es una forma distinta de repartir el capital entre los activos. Más arriba, "
        "más rentabilidad esperada; más a la derecha, más oscilaciones (riesgo). La línea negra une "
        "las mejores combinaciones posibles: la **frontera eficiente**."
    )

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.scatter(r["vol_cart"], r["ret_cart"], alpha=0.25, s=2, color=GRIS, label="Carteras analizadas")
    n_bins = 50
    bins_ = np.linspace(r["vol_cart"].min(), r["vol_cart"].max(), n_bins)
    ib = np.digitize(r["vol_cart"], bins_)
    fv, fr = [], []
    for b in range(1, n_bins):
        m_ = ib == b
        if m_.any():
            i_ = np.where(m_)[0][np.argmax(r["ret_cart"][m_])]
            fv.append(r["vol_cart"][i_]); fr.append(r["ret_cart"][i_])
    ax.plot(fv, fr, color="black", lw=3, label="Frontera eficiente")
    sr = np.linspace(0, r["vol_cart"].max() * 1.1, 100)
    ax.plot(sr, r["RF"] + r["sharpes"][r["idx_ms"]] * sr, "--", color=DORADO, lw=1.4, label="Línea del mercado de capitales")
    ax.scatter(r["vol_cart"][r["idx_mv"]], r["ret_cart"][r["idx_mv"]], color=GRIS, edgecolor="black", s=130, zorder=5, label="Cartera conservadora")
    ax.scatter(r["vol_cart"][r["idx_ms"]], r["ret_cart"][r["idx_ms"]], color=AZUL, s=130, zorder=5, label="Cartera de mejor equilibrio")
    ax.set_xlabel("Riesgo (volatilidad anual)"); ax.set_ylabel("Rentabilidad anual esperada (log)")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)
    mostrar_figura(fig)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### Cartera de mejor equilibrio")
        st.markdown("Máxima rentabilidad por unidad de riesgo (ratio de Sharpe). Es la empleada en el plan de ahorro.")
        st.dataframe(pd.DataFrame({"Activo": tickers, "Peso": [f"{w:.1%}" for w in r["pesos_ms"]]}), hide_index=True)
    with col_b:
        st.markdown("#### Cartera conservadora")
        st.markdown("Mínima volatilidad: prioriza la estabilidad sobre la rentabilidad.")
        st.dataframe(pd.DataFrame({"Activo": tickers, "Peso": [f"{w:.1%}" for w in r["pesos_mv"]]}), hide_index=True)

    with st.expander("Parámetros calibrados (detalle técnico)"):
        st.dataframe(pd.DataFrame(
            r["parametros"], index=tickers,
            columns=["μ (deriva anual)", "σ (volatilidad)", "λ (crisis/año)", "μ_J (tamaño medio crisis)", "σ_J (dispersión crisis)"]
        ).round(4))
        st.dataframe(r["corr"].round(3))

# ---------------------------------------------------------------- RIESGO
with tab_riesgo:
    st.subheader("¿Cuánto se puede llegar a perder?")
    st.markdown(
        f"Para 100 € invertidos hoy y mantenidos {T} años, las métricas resumen los **peores escenarios** simulados:"
    )

    def fila_riesgo(nombre, riesgo, dd, valor_fin):
        var95, cvar95 = riesgo["VaR95"], riesgo["CVaR95"]
        med = np.median(valor_fin)
        if var95 <= 0:
            txt_var = f"Incluso en el 5% de escenarios más desfavorables el resultado es una **ganancia** (≈{-var95:.0%} o más)."
        else:
            txt_var = f"En el 5% de escenarios más desfavorables la pérdida alcanza el **{var95:.0%}** o más de lo invertido."
        if cvar95 <= 0:
            txt_cvar = f"La media de ese 5% peor sigue siendo una **ganancia** del {-cvar95:.0%}."
        else:
            txt_cvar = f"Dentro de ese 5% peor, la pérdida media es del **{cvar95:.0%}**."
        st.markdown(f"#### {nombre}")
        c1, c2, c3 = st.columns(3)
        c1.metric("100 € se convierten típicamente en", f"{med:.0f} €")
        c2.metric("Peor 5% de escenarios (VaR 95%)", f"{-var95*100:+.0f}%")
        c3.metric("Mayor caída intermedia (mediana)", f"-{np.median(dd):.0%}")
        st.markdown(
            f"- {txt_var}\n- {txt_cvar}\n- Durante el camino, lo habitual es atravesar en algún momento una caída "
            f"desde máximos del **{np.median(dd):.0%}** (del {np.percentile(dd, 95):.0%} en el 5% de escenarios más "
            "turbulentos). Conocer este dato de antemano ayuda a no vender en el peor momento."
        )

    fila_riesgo("Cartera de mejor equilibrio", r["riesgo_ms"], r["dd_ms"], r["valor_ms"])
    st.divider()
    fila_riesgo("Cartera conservadora", r["riesgo_mv"], r["dd_mv"], r["valor_mv"])

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    for ax, datos, titulo in [(axes[0], r["valor_ms"], "Mejor equilibrio"), (axes[1], r["valor_mv"], "Conservadora")]:
        ax.hist(datos, bins=50, color=AZUL, alpha=0.85)
        ax.axvline(100, color=DORADO, linestyle="--", lw=2, label="Capital invertido (100 €)")
        ax.set_title(f"{titulo}: valor final de 100 € a {T} años")
        ax.set_xlabel("€ finales"); ax.legend(fontsize=8)
    mostrar_figura(fig)
    st.caption("Cada barra cuenta cuántos escenarios terminan en ese rango. A la izquierda de la línea dorada, pérdidas; "
               "a la derecha, ganancias.")

# ---------------------------------------------------------------- PLAN
with tab_plan:
    st.subheader("Plan de aportaciones periódicas")
    st.markdown(
        f"Plan analizado: **{formato_euro(r['aporte_inicial'])} iniciales + {formato_euro(r['aporte_mensual'])} mensuales** "
        f"durante {T} años en la cartera de mejor equilibrio. Capital total aportado: "
        f"**{formato_euro(r['total_aportado'])}**. Resultados en **euros de hoy** "
        "(netos de comisiones, impuestos e inflación)."
    )

    med, p5, p95 = np.median(r["W_real"]), np.percentile(r["W_real"], 5), np.percentile(r["W_real"], 95)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Resultado típico", formato_euro(med))
    c2.metric("Escenario adverso (peor 5%)", formato_euro(p5))
    c3.metric("Escenario favorable (mejor 5%)", formato_euro(p95))
    c4.metric("P(perder poder adquisitivo)", f"{np.mean(r['W_real'] < r['total_aportado']):.1%}")

    fig, ax = plt.subplots(figsize=(10, 4.5))
    Wp = r["W_paths"]
    for i in range(min(100, len(Wp))):
        ax.plot(Wp[i], color=AZUL, alpha=0.07)
    ax.plot(np.median(Wp, axis=0), color="black", lw=2, label="Evolución típica (mediana)")
    ax.plot(np.percentile(Wp, 5, axis=0), color=GRIS, lw=1.4, ls="--", label="Percentil 5")
    ax.plot(np.percentile(Wp, 95, axis=0), color=GRIS, lw=1.4, ls=":", label="Percentil 95")
    aportado = np.zeros(Wp.shape[1]); aportado[0] = r["aporte_inicial"]
    for f_ in r["fechas_aporte"]:
        aportado[f_:] += r["aporte_mensual"]
    ax.plot(aportado, color=DORADO, lw=2, label="Capital aportado")
    ax.set_xlabel("Sesiones de mercado"); ax.set_ylabel("Patrimonio (€, nominal)")
    ax.set_title("Evolución del patrimonio (100 escenarios de ejemplo)")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)
    mostrar_figura(fig)
    st.caption("La línea dorada es el dinero aportado. Cuando la nube azul discurre por encima, el plan va en ganancias.")

    st.markdown("#### Aportación única frente a aportaciones mensuales")
    fig, axes = plt.subplots(1, 2, figsize=(12, 4), sharey=True)
    todos = np.concatenate([r["W_real"], r["ls_real"]])
    bins_ = np.linspace(0, np.percentile(todos, 99), 60)
    for ax, datos, titulo in [(axes[0], r["ls_real"], "Todo invertido el día 0"), (axes[1], r["W_real"], "Aportaciones mensuales")]:
        ax.hist(datos, bins=bins_, density=True, alpha=0.85, color=AZUL)
        ax.axvline(r["total_aportado"], color=DORADO, ls="--", lw=2, label=f"Aportado: {formato_euro(r['total_aportado'])}")
        ax.axvline(np.median(datos), color="black", lw=2, label=f"Típico: {formato_euro(np.median(datos))}")
        ax.set_title(titulo); ax.set_xlabel("Patrimonio final (€ de hoy)"); ax.legend(fontsize=8)
    mostrar_figura(fig)
    st.markdown(
        f"- **Aportación única**: resultado típico {formato_euro(np.median(r['ls_real']))}; "
        f"probabilidad de terminar con menos: {np.mean(r['ls_real'] < r['total_aportado']):.1%}.\n"
        f"- **Aportaciones mensuales**: resultado típico {formato_euro(np.median(r['W_real']))}; "
        f"probabilidad de terminar con menos: {np.mean(r['W_real'] < r['total_aportado']):.1%}.\n\n"
        "Invertir todo al inicio suele rendir más en el caso típico (el capital trabaja más tiempo); "
        "las aportaciones mensuales suavizan los peores escenarios y se ajustan a la capacidad de ahorro real."
    )

# ---------------------------------------------------------------- VALIDACION
with tab_valida:
    st.subheader("Contraste del modelo con la realidad")
    st.markdown(
        f"Comparación de los movimientos diarios **reales** de `{tickers[0]}` con los **generados por el motor "
        "elegido**. Si ambas distribuciones coinciden —en particular en la zona de caídas fuertes—, el modelo "
        "es un reflejo razonable del comportamiento histórico."
    )
    fig, ax = plt.subplots(figsize=(9, 4.5))
    lim = max(np.abs(np.percentile(r["retornos_hist_1"], [0.1, 99.9]))) * 1.3
    bins_ = np.linspace(-lim, lim, 100)
    ax.hist(r["retornos_hist_1"], bins=bins_, density=True, alpha=0.6, color=GRIS, label="Histórico real")
    ax.hist(r["ret_sim_1d"], bins=bins_, density=True, alpha=0.6, color=AZUL, label="Simulado")
    ax.set_yscale("log")
    ax.set_xlabel("Movimiento diario (retorno log)"); ax.set_ylabel("Frecuencia (escala log)")
    ax.legend(); ax.grid(alpha=0.3)
    mostrar_figura(fig)

    def momentos(x):
        m, s = np.mean(x), np.std(x)
        return [m * 252, s * np.sqrt(252), np.mean(((x - m) / s) ** 3), np.mean(((x - m) / s) ** 4) - 3]

    st.dataframe(pd.DataFrame(
        [momentos(r["retornos_hist_1"]), momentos(r["ret_sim_1d"])],
        index=["Histórico", "Simulado"],
        columns=["Rentabilidad anual", "Volatilidad anual", "Asimetría", "Curtosis exceso"]).round(3))
    st.caption(
        "Escala vertical logarítmica para examinar los días extremos. El motor Merton captura los desplomes "
        "súbitos; el bootstrap reproduce además las rachas de volatilidad por remuestrear meses reales. "
        "El ensemble combina ambas virtudes."
    )

# ---------------------------------------------------------------- METODOLOGIA
with tab_metodo:
    st.subheader("Metodología en cinco pasos")
    st.markdown(f"""
1. **Datos.** Se descargan los precios históricos de los activos (Yahoo Finance, con respaldo en Stooq)
   y se trabaja con las sesiones en que todos cotizaron.
2. **Aprendizaje.** De cada activo se estima cuánto crece, cuánto oscila y con qué frecuencia e intensidad
   sufre desplomes; también la correlación entre activos.
3. **Simulación.** Se generan miles de futuros posibles de {T} años con el motor elegido:
   *Merton con saltos* (modelo paramétrico con desplomes súbitos), *bootstrap histórico* (remuestreo de
   meses reales, crisis incluidas) o *ensemble* (mitad de escenarios con cada uno, reduciendo la
   dependencia de un único modelo).
4. **Optimización.** Se evalúan 10.000 repartos de cartera y se identifican el de mejor relación
   rentabilidad/riesgo y el más estable.
5. **Plan personal.** Se simula el plan de aportaciones con comisiones, impuestos e inflación, y se
   presenta el abanico completo de resultados en euros de hoy.

**Cómo encontrar cualquier activo.** Use el catálogo (símbolo ya resuelto) o el buscador por nombre del
panel lateral. Para fondos índice europeos, la vía más fiable es localizar el ISIN del fondo en
[justETF](https://www.justetf.com) o [Morningstar](https://www.morningstar.es) y buscar ese ISIN en
[finance.yahoo.com](https://finance.yahoo.com): el símbolo resultante (con sufijo .AS, .DE, .MI según la
bolsa) es el que debe introducirse. Los fondos de gestoras sin cotización bursátil (planes de pensiones,
fondos no UCITS) no publican precio diario y deben aproximarse con su ETF equivalente.

**Glosario.** *Mediana*: la mitad de los escenarios acaba mejor y la otra mitad peor. *Volatilidad*: amplitud
de las oscilaciones. *Ratio de Sharpe*: rentabilidad por unidad de riesgo. *VaR 95%*: frontera del 5% de
escenarios más desfavorables. *CVaR*: pérdida media dentro de ese 5%. *Drawdown máximo*: mayor caída desde
un máximo previo. *Euros de hoy*: importes descontados de inflación.

**Advertencias.** El modelo aprende del pasado y el futuro puede diferir. Los resultados son educativos y
no constituyen asesoramiento financiero. La fiscalidad depende de la situación de cada inversor.
""")

st.markdown(
    f"<div class='murgi-footer'>© 2026 MurgiCapital · Herramienta educativa · "
    "Las rentabilidades pasadas no garantizan rentabilidades futuras</div>",
    unsafe_allow_html=True,
)

# Fin de murgi_app.py
