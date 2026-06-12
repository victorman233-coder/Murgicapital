# -*- coding: utf-8 -*-
"""
Simulador de inversión Monte Carlo (modelo de Merton con saltos)
================================================================
App Streamlit para público no técnico. Reproduce los resultados del notebook
MODELO_MONTECARLO_MEJORADO.ipynb: misma calibración por umbral, misma simulación
(idéntica secuencia aleatoria con la misma semilla), misma optimización Dirichlet,
mismas métricas (frontera eficiente, VaR/CVaR, drawdown, DCA con comisiones,
impuestos e inflación).

Ejecutar en local:   streamlit run app.py
"""

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import yfinance as yf

# ----------------------------------------------------------------------------
# Configuración de la página (título e icono también se usan al "instalar"
# la app en el móvil con "Añadir a pantalla de inicio")
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Simulador de inversión Monte Carlo",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# NÚCLEO DEL MODELO — idéntico al notebook (calibración, simulación, métricas)
# ============================================================================

def calibrar(retornos_activo, n_sigmas=3.0):
    """Separa los días 'normales' de los días de 'salto' (caídas más allá de
    mu - n_sigmas * sigma) y devuelve los 5 parámetros del modelo de Merton."""
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


def simular_merton(mu, sigma, lam, mu_J, sigma_J, L, T, M, seed, S0=100.0):
    """Simulación vectorizada de Merton: difusión correlacionada (Cholesky)
    + saltos de Poisson. Misma secuencia aleatoria que el notebook original."""
    np.random.seed(seed)
    dt = 1 / 252
    N = int(T / dt)
    n_act = len(mu)
    precio = np.zeros((M, N + 1, n_act), dtype=np.float32)
    precio[:, 0, :] = S0
    drift = (mu - 0.5 * sigma**2) * dt
    vol = sigma * np.sqrt(dt)
    for t in range(1, N + 1):
        Z = np.random.randn(M, n_act) @ L.T
        log_diff = drift + vol * Z
        n_j = np.random.poisson(lam * dt, size=(M, n_act))
        Zj = np.random.randn(M, n_act)
        log_salto = n_j * mu_J + np.sqrt(n_j) * sigma_J * Zj
        precio[:, t, :] = precio[:, t - 1, :] * np.exp(log_diff + log_salto).astype(np.float32)
    return precio


def metricas_riesgo(valor_final, S0=100.0):
    """VaR y CVaR al 95% y 99% expresados como pérdida sobre lo invertido."""
    perdida = (S0 - valor_final) / S0
    out = {}
    for nivel in (95, 99):
        v = np.percentile(perdida, nivel)
        out[f"VaR{nivel}"] = v
        out[f"CVaR{nivel}"] = np.mean(perdida[perdida >= v])
    return out


def max_drawdown(trayectorias):
    """Mayor caída desde máximos de cada trayectoria (lo que el inversor 'vive')."""
    cummax = np.maximum.accumulate(trayectorias, axis=1)
    dd = (cummax - trayectorias) / cummax
    return dd.max(axis=1)


@st.cache_data(show_spinner=False, ttl=3600)
def descargar_precios(tickers, start, end):
    """Descarga precios de cierre de Yahoo Finance y devuelve la tabla con
    los días en que TODOS los activos cotizaron (ventana común)."""
    series = {}
    for tk in tickers:
        d = yf.download(tk, start=start, end=end, progress=False)
        if d is None or len(d) == 0:
            raise ValueError(f"No hay datos para el ticker '{tk}'. Revisa el símbolo en finance.yahoo.com")
        series[tk] = d["Close"].squeeze()
    precios = pd.DataFrame(series).dropna()
    if len(precios) < 252:
        raise ValueError("Hay menos de un año de datos comunes entre los activos. Amplía las fechas o cambia de activos.")
    return precios


def formato_euro(x):
    return f"{x:,.0f} €".replace(",", ".")


# ============================================================================
# BARRA LATERAL — todo lo que el usuario puede elegir, con explicaciones
# ============================================================================

st.sidebar.title("⚙️ Configura tu simulación")

st.sidebar.markdown("**1. ¿En qué quieres invertir?**")
tickers_texto = st.sidebar.text_input(
    "Tickers (símbolos de Yahoo Finance, separados por comas)",
    value="^GSPC, IEAG.AS, GC=F",
    help="Ejemplos: ^GSPC = índice S&P 500 · IEAG.AS = fondo de bonos europeos · "
         "GC=F = oro · AAPL = Apple · VWCE.DE = fondo indexado mundial. "
         "Busca cualquier símbolo en finance.yahoo.com",
)

st.sidebar.markdown("**2. ¿Qué historia usamos para aprender?**")
col_f1, col_f2 = st.sidebar.columns(2)
fecha_inicio = col_f1.date_input("Desde", value=pd.Timestamp("1990-01-01"), min_value=pd.Timestamp("1950-01-01"))
fecha_fin = col_f2.date_input("Hasta", value=pd.Timestamp.today())

st.sidebar.markdown("**3. Tu plan de inversión**")
T = st.sidebar.slider("¿Cuántos años mantendrás la inversión?", 1, 40, 20)
aporte_inicial = st.sidebar.number_input("Aportación inicial (€)", min_value=0, value=600, step=100)
aporte_mensual = st.sidebar.number_input("Aportación mensual (€)", min_value=0, value=300, step=50)

with st.sidebar.expander("4. Costes, impuestos e inflación"):
    comision_aporte = st.number_input("Comisión por aporte (%)", 0.0, 5.0, 0.1, 0.05) / 100
    tipo_impositivo = st.number_input("Impuesto sobre la ganancia al vender (%)", 0.0, 60.0, 21.0, 1.0) / 100
    inflacion_anual = st.number_input("Inflación anual estimada (%)", 0.0, 15.0, 2.0, 0.5) / 100

with st.sidebar.expander("5. Ajustes avanzados (opcional)"):
    M = st.select_slider("Número de futuros simulados", options=[1000, 2000, 3000, 5000, 10000], value=3000,
                         help="Más simulaciones = resultados más estables pero más lentos.")
    n_sigmas = st.slider("Umbral de detección de crisis (en desviaciones típicas)", 2.0, 4.0, 3.0, 0.5,
                         help="Un día se considera 'crisis' (salto) si cae más allá de este umbral. "
                              "El resultado es robusto entre 2.5 y 3.5 (ver memoria).")
    rf_pct = st.number_input("Tipo de interés sin riesgo (%)", 0.0, 10.0, 2.193, 0.1)
    seed = st.number_input("Semilla aleatoria (reproducibilidad)", 0, 99999, 42)
    saltos_comunes = st.checkbox(
        "Modo prudente: crisis simultáneas entre activos", value=False,
        help="En crisis reales (2008, COVID) los activos caen a la vez. Activa esto para un "
             "escenario más conservador en el que la mitad de las crisis golpean a todos los activos al mismo tiempo.")

RF = np.log(1 + rf_pct / 100)
ejecutar = st.sidebar.button("🚀 Ejecutar simulación", type="primary", width="stretch")

st.sidebar.caption("Herramienta educativa. No es una recomendación de inversión: "
                   "rentabilidades pasadas no garantizan rentabilidades futuras.")

# ============================================================================
# CABECERA
# ============================================================================

st.title("📈 Simulador de inversión Monte Carlo")
st.markdown(
    "Esta herramienta estudia **cómo se han comportado en el pasado** los activos que elijas y, con ese "
    "aprendizaje, **simula miles de futuros posibles** para tu plan de inversión. No predice el futuro: "
    "te enseña el **abanico de resultados** que cabría esperar, incluyendo crisis repentinas "
    "(el modelo incorpora 'saltos' que imitan los desplomes de mercado)."
)

if not ejecutar and "resultados" not in st.session_state:
    st.info("👈 Configura tu plan en el panel lateral y pulsa **Ejecutar simulación**.")
    st.stop()

# ============================================================================
# CÁLCULO COMPLETO (solo al pulsar el botón; luego queda en session_state)
# ============================================================================

if ejecutar:
    tickers = [t.strip() for t in tickers_texto.split(",") if t.strip()]
    if len(tickers) < 2:
        st.error("Introduce al menos 2 tickers separados por comas.")
        st.stop()

    try:
        with st.spinner("Descargando datos históricos…"):
            precios_hist = descargar_precios(tuple(tickers), str(fecha_inicio), str(fecha_fin))
    except Exception as e:
        st.error(f"Problema con los datos: {e}")
        st.stop()

    retornos_df = np.log(precios_hist / precios_hist.shift(1)).dropna()
    n_act = len(tickers)

    # --- Calibración por activo (umbral n_sigmas, como en el notebook) ---
    parametros = [calibrar(retornos_df[tk].values, n_sigmas) for tk in tickers]
    mu_v, sigma_v, lam_v, mu_J_v, sigma_J_v = [np.array(x) for x in zip(*parametros)]

    # --- Correlación y Cholesky (regularizada por si la matriz es casi singular) ---
    corr = retornos_df.corr().values
    try:
        L = np.linalg.cholesky(corr)
    except np.linalg.LinAlgError:
        L = np.linalg.cholesky(corr + 1e-8 * np.eye(n_act))

    # --- Simulación ---
    with st.spinner(f"Simulando {M:,} futuros posibles durante {T} años…".replace(",", ".")):
        if saltos_comunes:
            # Variante prudente: la mitad de la intensidad mínima de salto es sistémica
            np.random.seed(int(seed))
            dt_ = 1 / 252
            N_ = int(T / dt_)
            lam_sys = 0.5 * lam_v.min()
            lam_idio = lam_v - lam_sys
            precio = np.zeros((M, N_ + 1, n_act), dtype=np.float32)
            precio[:, 0, :] = 100.0
            drift = (mu_v - 0.5 * sigma_v**2) * dt_
            vol = sigma_v * np.sqrt(dt_)
            for t_ in range(1, N_ + 1):
                Z = np.random.randn(M, n_act) @ L.T
                n_j = np.random.poisson(lam_idio * dt_, size=(M, n_act)) + np.random.poisson(lam_sys * dt_, size=(M, 1))
                Zj = np.random.randn(M, n_act)
                precio[:, t_, :] = precio[:, t_ - 1, :] * np.exp(drift + vol * Z + n_j * mu_J_v + np.sqrt(n_j) * sigma_J_v * Zj).astype(np.float32)
        else:
            precio = simular_merton(mu_v, sigma_v, lam_v, mu_J_v, sigma_J_v, L, T=T, M=M, seed=int(seed))

    # --- Optimización de cartera por muestreo Dirichlet (como el notebook) ---
    n_carteras = 10000
    pesos = np.random.dirichlet(np.ones(n_act), size=n_carteras)
    valor = precio[:, -1, :] @ pesos.T.astype(np.float32)
    retornos_log = np.log(valor / 100.0)
    vol_cart = np.std(retornos_log, axis=0) / np.sqrt(T)
    ret_cart = np.mean(retornos_log, axis=0) / T
    sharpes = (ret_cart - RF) / vol_cart
    idx_ms, idx_mv = int(np.argmax(sharpes)), int(np.argmin(vol_cart))

    # --- DCA con la cartera de máximo Sharpe (como el notebook) ---
    dias_por_mes = 21
    N = precio.shape[1] - 1
    w_opt = pesos[idx_ms].astype(np.float32)
    valor_cartera = precio @ w_opt
    fechas_aporte = np.arange(dias_por_mes, N + 1, dias_por_mes)
    n_aportes = len(fechas_aporte)
    total_aportado = aporte_inicial + n_aportes * aporte_mensual
    if total_aportado <= 0:
        st.error("Introduce una aportación inicial o mensual mayor que cero.")
        st.stop()

    W = np.zeros((M, N + 1), dtype=np.float32)
    W[:, 0] = aporte_inicial * (1 - comision_aporte)
    aporte_neto_mes = aporte_mensual * (1 - comision_aporte)
    fechas_set = set(fechas_aporte.tolist())
    for t_ in range(1, N + 1):
        W[:, t_] = W[:, t_ - 1] * (valor_cartera[:, t_] / valor_cartera[:, t_ - 1])
        if t_ in fechas_set:
            W[:, t_] += aporte_neto_mes

    W_nominal = W[:, -1].astype(np.float64)
    impuesto = np.maximum(0, W_nominal - total_aportado) * tipo_impositivo
    W_real = (W_nominal - impuesto) / (1 + inflacion_anual) ** T

    # --- Lump-sum equivalente (mismo dinero, todo el día 0) ---
    ls_nominal = (total_aportado * (1 - comision_aporte) * valor_cartera[:, -1] / valor_cartera[:, 0]).astype(np.float64)
    ls_real = (ls_nominal - np.maximum(0, ls_nominal - total_aportado) * tipo_impositivo) / (1 + inflacion_anual) ** T

    # --- Validación: retornos diarios simulados vs históricos (1er activo) ---
    ret_sim_1d = np.log(precio[:, 1:min(253, N + 1), 0] / precio[:, 0:min(252, N), 0]).flatten()

    # --- Riesgo ---
    riesgo_ms = metricas_riesgo(valor[:, idx_ms])
    riesgo_mv = metricas_riesgo(valor[:, idx_mv])
    dd_ms = max_drawdown(precio @ pesos[idx_ms].astype(np.float32))
    dd_mv = max_drawdown(precio @ pesos[idx_mv].astype(np.float32))

    # Guardar todo lo necesario para pintar (sin el cubo gigante de precios)
    st.session_state["resultados"] = dict(
        tickers=tickers, parametros=parametros, corr=retornos_df.corr(),
        retornos_hist_1=retornos_df[tickers[0]].values, ret_sim_1d=ret_sim_1d,
        pesos_ms=pesos[idx_ms], pesos_mv=pesos[idx_mv],
        vol_cart=vol_cart, ret_cart=ret_cart, sharpes=sharpes, idx_ms=idx_ms, idx_mv=idx_mv,
        valor_ms=valor[:, idx_ms].astype(np.float64), valor_mv=valor[:, idx_mv].astype(np.float64),
        riesgo_ms=riesgo_ms, riesgo_mv=riesgo_mv, dd_ms=dd_ms, dd_mv=dd_mv,
        W_paths=W[::max(1, M // 200)].astype(np.float64), W_real=W_real, ls_real=ls_real,
        total_aportado=total_aportado, T=T, RF=RF, n_aportes=n_aportes,
        fechas_aporte=fechas_aporte, aporte_inicial=aporte_inicial, aporte_mensual=aporte_mensual,
        rango_datos=(precios_hist.index[0].date(), precios_hist.index[-1].date()),
        n_dias=len(precios_hist), saltos_comunes=saltos_comunes,
    )

r = st.session_state["resultados"]
tickers, T = r["tickers"], r["T"]

# ============================================================================
# RESULTADOS EN PESTAÑAS
# ============================================================================

tab_resumen, tab_cartera, tab_riesgo, tab_plan, tab_valida, tab_ayuda = st.tabs(
    ["📊 Resumen", "🥧 Tu cartera ideal", "⚠️ Riesgos", "💶 Tu plan de ahorro", "🔬 ¿Es fiable el modelo?", "❓ Guía rápida"]
)

# ---------------------------------------------------------------- RESUMEN
with tab_resumen:
    st.subheader("Lo esencial en 30 segundos")
    med_real = np.median(r["W_real"])
    p_perder = np.mean(r["W_real"] < r["total_aportado"])
    c1, c2, c3 = st.columns(3)
    c1.metric("Aportarás en total", formato_euro(r["total_aportado"]))
    c2.metric(f"Resultado típico a {T} años (en € de hoy)", formato_euro(med_real),
              delta=formato_euro(med_real - r["total_aportado"]))
    c3.metric("Probabilidad de acabar perdiendo poder adquisitivo", f"{p_perder:.1%}",
              delta_color="inverse")
    st.caption("El 'resultado típico' es la mediana: la mitad de los futuros simulados acaba mejor y la otra mitad peor. "
               "Está expresado en euros de hoy: ya se han descontado comisiones, impuestos e inflación.")

    st.markdown("**Reparto recomendado por la simulación** (cartera con mejor relación rentabilidad/riesgo):")
    cols = st.columns(len(tickers))
    for c, tk, w in zip(cols, tickers, r["pesos_ms"]):
        c.metric(tk, f"{w:.0%}")
    st.caption(f"Datos usados: {r['rango_datos'][0]} → {r['rango_datos'][1]} "
               f"({r['n_dias']} días en que cotizaron todos los activos)."
               + (" Modo prudente con crisis simultáneas ACTIVADO." if r["saltos_comunes"] else ""))

# ---------------------------------------------------------------- CARTERA
with tab_cartera:
    st.subheader("¿Cómo repartir el dinero entre los activos?")
    st.markdown(
        "Hemos probado **10.000 combinaciones de pesos**. Cada punto del gráfico es una forma distinta de "
        "repartir tu dinero. Cuanto más arriba, más rentabilidad esperada; cuanto más a la derecha, más "
        "altibajos (riesgo). La línea negra es la **frontera eficiente**: las mejores combinaciones posibles."
    )

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.scatter(r["vol_cart"], r["ret_cart"], alpha=0.25, s=2, label="Carteras probadas")
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
    ax.plot(sr, r["RF"] + r["sharpes"][r["idx_ms"]] * sr, "g--", lw=1.2, label="Línea del mercado de capitales")
    ax.scatter(r["vol_cart"][r["idx_mv"]], r["ret_cart"][r["idx_mv"]], color="red", s=120, zorder=5, label="Más tranquila (mín. volatilidad)")
    ax.scatter(r["vol_cart"][r["idx_ms"]], r["ret_cart"][r["idx_ms"]], color="green", s=120, zorder=5, label="Mejor equilibrio (máx. Sharpe)")
    ax.set_xlabel("Riesgo (volatilidad anual)"); ax.set_ylabel("Rentabilidad anual esperada (log)")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)
    st.pyplot(fig, width="stretch")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### 🟢 Mejor equilibrio (máximo Sharpe)")
        st.markdown("La que más rentabilidad ofrece **por cada unidad de riesgo asumido**. Es la que usa tu plan de ahorro.")
        st.dataframe(pd.DataFrame({"Activo": tickers, "Peso": [f"{w:.1%}" for w in r["pesos_ms"]]}), hide_index=True)
    with col_b:
        st.markdown("#### 🔴 Más tranquila (mínima volatilidad)")
        st.markdown("La que **menos se mueve**: para quien prioriza dormir bien sobre maximizar la ganancia.")
        st.dataframe(pd.DataFrame({"Activo": tickers, "Peso": [f"{w:.1%}" for w in r["pesos_mv"]]}), hide_index=True)

    with st.expander("🎓 Detalle técnico (parámetros calibrados del modelo)"):
        st.markdown("Parámetros del modelo de Merton estimados a partir del histórico "
                    "(umbral de salto y método descritos en la memoria):")
        st.dataframe(pd.DataFrame(
            r["parametros"], index=tickers,
            columns=["μ (deriva anual)", "σ (volatilidad)", "λ (crisis/año)", "μ_J (tamaño medio crisis)", "σ_J (dispersión crisis)"]
        ).round(4))
        st.markdown("Correlaciones históricas entre activos:")
        st.dataframe(r["corr"].round(3))

# ---------------------------------------------------------------- RIESGO
with tab_riesgo:
    st.subheader("¿Cuánto puedo llegar a perder?")
    st.markdown(
        f"Imagina que inviertes **100 €** hoy en la cartera y esperas **{T} años**. Estas métricas resumen "
        "los **peores escenarios** de los miles de futuros simulados:"
    )

    def fila_riesgo(nombre, riesgo, dd, valor_fin):
        var95, cvar95 = riesgo["VaR95"], riesgo["CVaR95"]
        med = np.median(valor_fin)
        if var95 <= 0:
            txt_var = f"Incluso en el 5% de futuros más desfavorables acabarías **ganando** (~{-var95:.0%} o más)."
        else:
            txt_var = f"En el 5% de futuros más desfavorables perderías **{var95:.0%} o más** de lo invertido."
        if cvar95 <= 0:
            txt_cvar = f"El promedio de ese 5% peor sigue siendo una **ganancia** del {-cvar95:.0%}."
        else:
            txt_cvar = f"Si ocurre ese 5% peor, la pérdida media sería del **{cvar95:.0%}**."
        st.markdown(f"#### {nombre}")
        c1, c2, c3 = st.columns(3)
        c1.metric("100 € se convierten típicamente en", f"{med:.0f} €")
        c2.metric("Peor 5% de los casos (VaR 95%)", f"{-var95*100:+.0f}%")
        c3.metric("Mayor bache por el camino (mediana)", f"-{np.median(dd):.0%}")
        st.markdown(f"- {txt_var}\n- {txt_cvar}\n- Por el camino, lo normal es sufrir en algún momento una caída "
                    f"desde máximos de **{np.median(dd):.0%}** (y de {np.percentile(dd, 95):.0%} en el 5% de futuros más turbulentos). "
                    "Conviene saberlo de antemano para no vender en pánico.")

    fila_riesgo("🟢 Cartera de mejor equilibrio", r["riesgo_ms"], r["dd_ms"], r["valor_ms"])
    st.divider()
    fila_riesgo("🔴 Cartera más tranquila", r["riesgo_mv"], r["dd_mv"], r["valor_mv"])

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    for ax, datos, titulo in [(axes[0], r["valor_ms"], "Mejor equilibrio"), (axes[1], r["valor_mv"], "Más tranquila")]:
        ax.hist(datos, bins=50, color="steelblue", alpha=0.8)
        ax.axvline(100, color="red", linestyle="--", label="Lo invertido (100 €)")
        ax.set_title(f"{titulo}: valor final de 100 € a {T} años")
        ax.set_xlabel("€ finales"); ax.legend(fontsize=8)
    st.pyplot(fig, width="stretch")
    st.caption("Cada barra cuenta cuántos futuros simulados acabaron en ese rango de valor. "
               "La cola hacia la derecha son los futuros excepcionales; la zona a la izquierda de la línea roja, las pérdidas.")

# ---------------------------------------------------------------- PLAN
with tab_plan:
    st.subheader("Tu plan de ahorro, mes a mes")
    st.markdown(
        f"Plan simulado: **{formato_euro(r['aporte_inicial'])} iniciales + {formato_euro(r['aporte_mensual'])} al mes** "
        f"durante {T} años, invertidos en la cartera de mejor equilibrio. Total aportado: "
        f"**{formato_euro(r['total_aportado'])}**. Todos los resultados están en **euros de hoy** "
        "(descontadas comisiones, impuestos e inflación), que es lo único comparable con tu bolsillo actual."
    )

    med, p5, p95 = np.median(r["W_real"]), np.percentile(r["W_real"], 5), np.percentile(r["W_real"], 95)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Resultado típico", formato_euro(med))
    c2.metric("Si va mal (peor 5%)", formato_euro(p5))
    c3.metric("Si va muy bien (mejor 5%)", formato_euro(p95))
    c4.metric("P(perder poder adquisitivo)", f"{np.mean(r['W_real'] < r['total_aportado']):.1%}")
    st.caption("'Si va mal' no es el peor caso imaginable, sino la frontera del 5% de futuros más desfavorables.")

    # Evolución temporal
    fig, ax = plt.subplots(figsize=(10, 4.5))
    Wp = r["W_paths"]
    for i in range(min(100, len(Wp))):
        ax.plot(Wp[i], color="blue", alpha=0.08)
    ax.plot(np.median(Wp, axis=0), color="black", lw=2, label="Camino típico (mediana)")
    ax.plot(np.percentile(Wp, 5, axis=0), color="red", lw=1.3, ls="--", label="Percentil 5")
    ax.plot(np.percentile(Wp, 95, axis=0), color="green", lw=1.3, ls="--", label="Percentil 95")
    aportado = np.zeros(Wp.shape[1]); aportado[0] = r["aporte_inicial"]
    for f_ in r["fechas_aporte"]:
        aportado[f_:] += r["aporte_mensual"]
    ax.plot(aportado, color="orange", lw=2, label="Dinero aportado")
    ax.set_xlabel("Días de mercado"); ax.set_ylabel("Patrimonio (€, nominal)")
    ax.set_title("Cómo crecería tu hucha (100 futuros de ejemplo)")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)
    st.pyplot(fig, width="stretch")
    st.caption("La línea naranja es lo que sale de tu bolsillo. Si la nube azul vuela por encima, vas ganando.")

    st.markdown("#### ¿Y si lo invirtiera todo de golpe? (lump-sum vs aportes mensuales)")
    fig, axes = plt.subplots(1, 2, figsize=(12, 4), sharey=True)
    todos = np.concatenate([r["W_real"], r["ls_real"]])
    bins_ = np.linspace(0, np.percentile(todos, 99), 60)
    for ax, datos, titulo in [(axes[0], r["ls_real"], "Todo de golpe el día 0"), (axes[1], r["W_real"], "Aportes mensuales (DCA)")]:
        ax.hist(datos, bins=bins_, density=True, alpha=0.8, color="steelblue")
        ax.axvline(r["total_aportado"], color="orange", ls="--", lw=2, label=f"Aportado: {formato_euro(r['total_aportado'])}")
        ax.axvline(np.median(datos), color="black", lw=2, label=f"Típico: {formato_euro(np.median(datos))}")
        ax.set_title(titulo); ax.set_xlabel("Patrimonio final (€ de hoy)"); ax.legend(fontsize=8)
    st.pyplot(fig, width="stretch")
    st.markdown(
        f"- **Todo de golpe**: resultado típico {formato_euro(np.median(r['ls_real']))}, "
        f"probabilidad de acabar con menos: {np.mean(r['ls_real'] < r['total_aportado']):.1%}.\n"
        f"- **Mes a mes (DCA)**: resultado típico {formato_euro(np.median(r['W_real']))}, "
        f"probabilidad de acabar con menos: {np.mean(r['W_real'] < r['total_aportado']):.1%}.\n\n"
        "Invertir de golpe suele acabar mejor *en el caso típico* (el dinero trabaja más tiempo), pero los aportes "
        "mensuales suavizan los peores escenarios y, en la práctica, es como ahorra la mayoría de la gente."
    )

# ---------------------------------------------------------------- VALIDACION
with tab_valida:
    st.subheader("¿Se parece lo simulado a la realidad?")
    st.markdown(
        f"Comparamos los movimientos diarios **reales** de `{tickers[0]}` con los que **genera el modelo**. "
        "Si las dos campanas se parecen —especialmente en la zona de caídas fuertes (cola izquierda)—, "
        "el modelo es un espejo razonable del comportamiento histórico."
    )
    fig, ax = plt.subplots(figsize=(9, 4.5))
    lim = max(np.abs(np.percentile(r["retornos_hist_1"], [0.1, 99.9]))) * 1.3
    bins_ = np.linspace(-lim, lim, 100)
    ax.hist(r["retornos_hist_1"], bins=bins_, density=True, alpha=0.55, label="Realidad (histórico)")
    ax.hist(r["ret_sim_1d"], bins=bins_, density=True, alpha=0.55, label="Modelo (simulado)")
    ax.set_yscale("log")
    ax.set_xlabel("Movimiento diario (retorno log)"); ax.set_ylabel("Frecuencia (escala log)")
    ax.legend(); ax.grid(alpha=0.3)
    st.pyplot(fig, width="stretch")

    def momentos(x):
        m, s = np.mean(x), np.std(x)
        return [m * 252, s * np.sqrt(252), np.mean(((x - m) / s) ** 3), np.mean(((x - m) / s) ** 4) - 3]

    st.dataframe(pd.DataFrame(
        [momentos(r["retornos_hist_1"]), momentos(r["ret_sim_1d"])],
        index=["Realidad", "Modelo"],
        columns=["Rentabilidad anual", "Volatilidad anual", "Asimetría", "Curtosis exceso"]).round(3))
    st.caption(
        "La escala vertical es logarítmica para poder mirar con lupa los días extremos. El modelo de Merton "
        "captura las caídas bruscas (por eso existe la pestaña de riesgos); la 'curtosis' simulada suele quedar "
        "algo por debajo de la real porque el modelo no encadena rachas de nervios del mercado (volatilidad en "
        "racimos), una limitación conocida y documentada en la memoria."
    )

# ---------------------------------------------------------------- AYUDA
with tab_ayuda:
    st.subheader("Guía rápida para no perderse")
    st.markdown(f"""
**¿Qué hace exactamente esta app?**
1. Descarga los precios históricos de los activos que elijas.
2. Aprende de ellos: cuánto suelen subir, cuánto vibran y cada cuánto sufren desplomes ("saltos").
3. Genera miles de futuros posibles de {T} años con esas características (método **Monte Carlo**, modelo de **Merton**).
4. Prueba 10.000 repartos de cartera y te enseña los dos más interesantes.
5. Simula tu plan de aportaciones con comisiones, impuestos e inflación incluidos.

**Diccionario en una línea:**
- **Ticker**: el código de un activo en bolsa (`^GSPC` es el S&P 500, `AAPL` es Apple).
- **Mediana / resultado típico**: la mitad de los futuros acaba mejor y la otra mitad peor. Más honesta que la media, a la que la inflan unos pocos futuros excepcionales.
- **Volatilidad**: cuánto "vibra" la inversión. Más volatilidad = viaje más movido.
- **Ratio de Sharpe**: rentabilidad obtenida por cada unidad de riesgo. Más alto = mejor.
- **VaR 95%**: la frontera del 5% de futuros más desfavorables.
- **CVaR 95%**: si caes en ese 5% peor, cuánto pierdes en promedio. Siempre igual o peor que el VaR.
- **Drawdown máximo**: el mayor bache desde un máximo previo. Es el "mal trago" que hay que saber aguantar.
- **Euros de hoy (reales)**: cantidades ya descontadas de inflación, comparables con tu poder de compra actual.
- **DCA**: invertir una cantidad fija cada mes, pase lo que pase.

**Avisos importantes:**
- El modelo aprende del pasado; el futuro puede comportarse distinto (cambios estructurales, crisis inéditas).
- Herramienta educativa: **no es asesoramiento financiero**. Para decisiones reales, consulta a un profesional.
- Los impuestos dependen de tu país y situación; el tipo aplicado aquí es el que tú introduzcas.
""")
