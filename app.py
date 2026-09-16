import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import tensorflow as tf
import textwrap

st.set_page_config(
    page_title="Aircraft Health Intelligence",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)


def render_html(html, container=st):
    """Render HTML without Streamlit's Markdown code-block parsing."""
    html = textwrap.dedent(html).strip()
    if hasattr(container, "html"):
        container.html(html)
    else:
        container.markdown(html, unsafe_allow_html=True)


st.markdown("""
<style>

/* ===== AROGYA PREMIUM AVIATION THEME ===== */

:root {
    --navy: #071426;
    --blue: #1683ff;
    --cyan: #22d3ee;
    --text: #e8f0fa;
    --muted: #94a9bf;
}

/* Main application */
.stApp {
    background:
        radial-gradient(circle at 8% 0%, rgba(22,131,255,0.14), transparent 28%),
        radial-gradient(circle at 92% 10%, rgba(34,211,238,0.10), transparent 25%),
        linear-gradient(135deg, #06111f 0%, #09192c 48%, #071426 100%);
    color: var(--text);
}

.main {
    background: transparent;
}

.block-container {
    max-width: 1500px;
    padding-top: 1.2rem;
    padding-bottom: 3rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #061221 0%, #0a1b31 55%, #071426 100%);
    border-right: 1px solid rgba(72,147,220,0.22);
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label {
    color: #dcecff !important;
}

/* Hero */
.hero {
    position: relative;
    overflow: hidden;
    padding: 28px 32px;
    margin-bottom: 22px;
    border: 1px solid rgba(87,163,235,0.28);
    border-radius: 24px;
    background:
        radial-gradient(circle at 85% 15%, rgba(34,211,238,0.16), transparent 22%),
        linear-gradient(135deg, rgba(14,47,82,0.96), rgba(7,22,40,0.96));
    box-shadow: 0 18px 55px rgba(0,0,0,0.30);
}

.hero-kicker {
    color: #67e8f9;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2.2px;
    text-transform: uppercase;
    margin-bottom: 7px;
}

.hero-title {
    color: #f5f9ff;
    font-size: clamp(30px, 4vw, 48px);
    font-weight: 850;
    line-height: 1.05;
    margin: 0;
    letter-spacing: -1px;
}

.hero-title span {
    background: linear-gradient(90deg, #ffffff, #72e5ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    color: #a9bdd2;
    font-size: 16px;
    line-height: 1.55;
    max-width: 900px;
    margin-top: 12px;
}

.hero-badges {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 18px;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    padding: 7px 11px;
    border-radius: 999px;
    color: #dff8ff;
    background: rgba(24,131,255,0.10);
    border: 1px solid rgba(91,185,255,0.22);
    font-size: 12px;
    font-weight: 700;
}

/* Section titles */
.section-title {
    position: relative;
    font-size: 22px;
    font-weight: 800;
    color: #eef7ff;
    margin-top: 30px;
    margin-bottom: 13px;
    padding: 12px 16px 12px 18px;
    border-left: 4px solid #22d3ee;
    border-radius: 0 12px 12px 0;
    background: linear-gradient(90deg, rgba(22,131,255,0.12), transparent);
}

/* Metric cards */
div[data-testid="stMetric"] {
    background: linear-gradient(145deg, rgba(17,39,66,0.96), rgba(8,25,45,0.94));
    border: 1px solid rgba(91,151,204,0.22);
    border-radius: 18px;
    padding: 16px 18px;
    min-height: 112px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.20);
    transition: transform 0.2s ease, border-color 0.2s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    border-color: rgba(34,211,238,0.45);
}

div[data-testid="stMetricLabel"] {
    color: #91a9c1 !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

div[data-testid="stMetricValue"] {
    color: #f5fbff !important;
    font-size: 28px !important;
    font-weight: 850 !important;
}

/* Text */
.stApp p, .stApp li {
    color: #b9c9da;
}

.stApp h1, .stApp h2, .stApp h3 {
    color: #eef7ff;
}

/* Inputs */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background: rgba(8,27,48,0.92) !important;
    border-color: rgba(86,148,201,0.28) !important;
    border-radius: 12px !important;
}

div[data-baseweb="select"] span {
    color: #e7f2ff !important;
}

span[data-baseweb="tag"] {
    background: rgba(22,131,255,0.18) !important;
    border: 1px solid rgba(73,174,255,0.28) !important;
}

/* Buttons */
.stButton > button,
.stDownloadButton > button {
    border-radius: 12px !important;
    border: 1px solid rgba(67,169,255,0.30) !important;
    background: linear-gradient(135deg, #0d5fc4, #087f9f) !important;
    color: white !important;
    font-weight: 750 !important;
    padding: 0.65rem 1rem !important;
    box-shadow: 0 8px 22px rgba(0,100,190,0.20);
    transition: all 0.2s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    transform: translateY(-2px);
    border-color: rgba(103,232,249,0.65) !important;
    box-shadow: 0 10px 28px rgba(22,131,255,0.30);
}

/* Alerts */
div[data-testid="stAlert"] {
    border-radius: 14px !important;
    border: 1px solid rgba(91,151,204,0.22) !important;
    background: rgba(10,29,50,0.72) !important;
}

/* Dataframe */
div[data-testid="stDataFrame"] {
    border: 1px solid rgba(91,151,204,0.20);
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 12px 32px rgba(0,0,0,0.18);
}

/* Plotly containers */
div[data-testid="stPlotlyChart"] {
    background: rgba(7,22,40,0.38);
    border: 1px solid rgba(91,151,204,0.16);
    border-radius: 18px;
    padding: 7px;
    box-shadow: 0 10px 28px rgba(0,0,0,0.16);
}

/* Footer */
.footer-card {
    margin-top: 35px;
    padding: 22px 25px;
    border-radius: 18px;
    border: 1px solid rgba(91,151,204,0.18);
    background: linear-gradient(135deg, rgba(12,35,60,0.90), rgba(7,22,40,0.90));
    text-align: center;
}

.footer-brand {
    color: #67e8f9;
    font-size: 18px;
    font-weight: 800;
    margin-bottom: 6px;
}

.footer-text {
    color: #8da4bb;
    font-size: 12px;
    line-height: 1.6;
}

@media (max-width: 900px) {
    .hero {
        padding: 22px;
        border-radius: 18px;
    }

    .section-title {
        font-size: 19px;
    }

    div[data-testid="stMetricValue"] {
        font-size: 23px !important;
    }
}


/* ===== READABLE NATIVE STREAMLIT TEXT ===== */
.stApp h2 {
    color: #f4f9ff !important;
    font-size: 24px !important;
    font-weight: 850 !important;
    margin-top: 30px !important;
    margin-bottom: 14px !important;
    padding: 11px 16px !important;
    border-left: 4px solid #22d3ee !important;
    border-radius: 0 12px 12px 0 !important;
    background: linear-gradient(90deg, rgba(22,131,255,0.14), rgba(22,131,255,0.02)) !important;
}

.stApp h3, .stApp h4 {
    color: #f0f7ff !important;
}

.stApp p, .stApp li, .stApp label {
    color: #c8d8e8 !important;
}

section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] h4,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label {
    color: #e7f3ff !important;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

render_html(
    """
    <div class="hero">
        <div class="hero-kicker">✈ AROGYA • AIRCRAFT HEALTH INTELLIGENCE</div>
        <div class="hero-title">Intelligent <span>Aircraft Health</span> Monitoring</div>
        <div class="hero-subtitle">
            AI-powered predictive maintenance, anomaly detection and
            Remaining Useful Life estimation for multivariate engine telemetry.
        </div>
        <div class="hero-badges">
            <span class="hero-badge">◉ LIVE ENGINE MONITORING</span>
            <span class="hero-badge">◈ LSTM + RANDOM FOREST</span>
            <span class="hero-badge">◇ ANOMALY INTELLIGENCE</span>
            <span class="hero-badge">▣ NASA C-MAPSS FD001</span>
        </div>
    </div>
    """
)


# ---------------------------------------------------------
# LOAD MODELS
# ---------------------------------------------------------

model = joblib.load("rul_model.pkl")
scaler = joblib.load("scaler.pkl")
anomaly_model = joblib.load("anomaly_model.pkl")

lstm_model = tf.keras.models.load_model(
    "lstm_rul_model.keras"
)

metrics = joblib.load(
    "model_metrics.pkl"
)


# ---------------------------------------------------------
# COLUMN DEFINITIONS
# ---------------------------------------------------------

columns = [
    "engine_id",
    "cycle",
    "setting_1",
    "setting_2",
    "setting_3"
]

sensor_columns = [
    f"sensor_{i}"
    for i in range(1, 22)
]

columns = columns + sensor_columns

features = sensor_columns


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

train = pd.read_csv(
    "train_FD001.txt",
    sep=r"\s+",
    header=None
)

train.columns = columns

test = pd.read_csv(
    "test_FD001.txt",
    sep=r"\s+",
    header=None
)

test.columns = columns

actual_rul = np.loadtxt(
    "RUL_FD001.txt"
)


# ---------------------------------------------------------
# DATA QUALITY
# ---------------------------------------------------------

missing_count = int(
    test.isnull().sum().sum()
)

duplicate_count = int(
    test.duplicated().sum()
)


# ---------------------------------------------------------
# PREPARE TEST DATA
# ---------------------------------------------------------

test_last = (
    test
    .groupby("engine_id")
    .last()
    .reset_index()
)

test_scaled = test_last.copy()

test_scaled[features] = scaler.transform(
    test_scaled[features]
)


# ---------------------------------------------------------
# RANDOM FOREST PREDICTION
# ---------------------------------------------------------

rf_predictions = model.predict(
    test_scaled[features]
)


# ---------------------------------------------------------
# RANDOM FOREST UNCERTAINTY
# ---------------------------------------------------------

rf_tree_predictions = np.array([
    tree.predict(test_scaled[features])
    for tree in model.estimators_
]).T

rf_uncertainty = rf_tree_predictions.std(axis=1)


def get_uncertainty_level(value):

    if value < 5:
        return "LOW"

    elif value < 10:
        return "MODERATE"

    elif value < 20:
        return "HIGH"

    else:
        return "VERY HIGH"


# ---------------------------------------------------------
# LSTM TEST SEQUENCES
# ---------------------------------------------------------

test_lstm = test.copy()

test_lstm[features] = scaler.transform(
    test_lstm[features]
)

sequence_length = 30

X_test_lstm = []
test_engine_ids = []

for current_engine_id in test_lstm["engine_id"].unique():

    engine_data = test_lstm[
        test_lstm["engine_id"] == current_engine_id
    ].sort_values("cycle")

    sensor_data = engine_data[features].values

    if len(sensor_data) >= sequence_length:

        X_test_lstm.append(
            sensor_data[-sequence_length:]
        )

        test_engine_ids.append(
            current_engine_id
        )

X_test_lstm = np.array(
    X_test_lstm
)


# ---------------------------------------------------------
# LSTM PREDICTION
# ---------------------------------------------------------

lstm_predictions = lstm_model.predict(
    X_test_lstm,
    verbose=0
).flatten()


# ---------------------------------------------------------
# ENGINE RESULTS
# ---------------------------------------------------------

results = pd.DataFrame({

    "Engine ID": test_engine_ids,

    "Random Forest RUL": rf_predictions,

    "LSTM RUL": lstm_predictions,

    "Actual RUL": actual_rul,

    "RUL Uncertainty": rf_uncertainty

})


results["Predicted RUL"] = (
    results["LSTM RUL"]
    .clip(lower=0)
)


# ---------------------------------------------------------
# HEALTH INDEX
# ---------------------------------------------------------

max_rul = results["Predicted RUL"].max()

if max_rul > 0:

    results["RUL Score"] = (
        results["Predicted RUL"]
        / max_rul
        * 100
    ).clip(0, 100)

else:

    results["RUL Score"] = 0


# ---------------------------------------------------------
# ANOMALY DETECTION
# ---------------------------------------------------------

anomaly_predictions = anomaly_model.predict(
    test_scaled[features]
)

results["Anomaly Status"] = [
    "ANOMALY" if x == -1 else "NORMAL"
    for x in anomaly_predictions
]


# ---------------------------------------------------------
# SENSOR ANOMALY SEVERITY
# ---------------------------------------------------------

train_sensor_mean = train[features].mean()

train_sensor_std = (
    train[features]
    .std()
    .replace(0, 1)
)

z_scores = (
    test_last[features]
    - train_sensor_mean
) / train_sensor_std

anomaly_score = (
    z_scores.abs()
    .mean(axis=1)
)

results["Anomaly Severity"] = anomaly_score


def severity_category(score):

    if score < 1:
        return "LOW"

    elif score < 2:
        return "MODERATE"

    elif score < 3:
        return "HIGH"

    else:
        return "SEVERE"


results["Severity Level"] = (
    results["Anomaly Severity"]
    .apply(severity_category)
)


# ---------------------------------------------------------
# ADAPTIVE HEALTH INDEX
# ---------------------------------------------------------

results["Anomaly Penalty"] = (
    results["Anomaly Status"]
    .apply(
        lambda x:
        20 if x == "ANOMALY" else 0
    )
)

results["Adaptive Health Index"] = (
    results["RUL Score"]
    - results["Anomaly Penalty"]
).clip(0, 100)


# ---------------------------------------------------------
# ADAPTIVE FSM
# ---------------------------------------------------------

def adaptive_health_state(row):

    health = row["Adaptive Health Index"]

    if health >= 75:
        return "NORMAL"

    elif health >= 50:
        return "CAUTION"

    elif health >= 25:
        return "DEGRADED"

    else:
        return "CRITICAL"


results["Adaptive Health State"] = (
    results
    .apply(adaptive_health_state, axis=1)
)


# ---------------------------------------------------------
# MAINTENANCE RISK
# ---------------------------------------------------------

def get_risk(row):

    state = row["Adaptive Health State"]
    severity = row["Severity Level"]

    if state == "CRITICAL" or severity == "SEVERE":
        return "HIGH"

    elif state == "DEGRADED" or severity == "HIGH":
        return "MEDIUM"

    elif state == "CAUTION" or severity == "MODERATE":
        return "LOW"

    else:
        return "VERY LOW"


results["Maintenance Risk"] = (
    results.apply(get_risk, axis=1)
)


# ---------------------------------------------------------
# UNCERTAINTY LEVEL
# ---------------------------------------------------------

results["Uncertainty Level"] = (
    results["RUL Uncertainty"]
    .apply(get_uncertainty_level)
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

render_html(
    """
    <div style="
        padding:16px 14px;
        border-radius:16px;
        margin-bottom:18px;
        background:linear-gradient(135deg, rgba(22,131,255,0.16), rgba(34,211,238,0.06));
        border:1px solid rgba(91,151,204,0.22);
    ">
        <div style="font-size:24px;font-weight:850;color:#f3f9ff;">✈️ AROGYA</div>
        <div style="font-size:11px;letter-spacing:1.4px;color:#67e8f9;font-weight:800;margin-top:4px;">
            HEALTH INTELLIGENCE CONSOLE
        </div>
    </div>
    """,
    container=st.sidebar
)

st.sidebar.markdown("### 🎛️ System Controls")
st.sidebar.markdown("### Engine Selection")

engine_id = st.sidebar.selectbox(
    "Select Engine",
    results["Engine ID"].tolist()
)

selected = results[
    results["Engine ID"] == engine_id
].iloc[0]

st.sidebar.markdown("---")

st.sidebar.markdown(
    "### Monitoring Information"
)

st.sidebar.write(
    "Dataset: NASA C-MAPSS FD001"
)

st.sidebar.write(
    f"Engines monitored: {len(results)}"
)

st.sidebar.write(
    f"Sensors: {len(features)}"
)


# ---------------------------------------------------------
# CURRENT ENGINE DATA
# ---------------------------------------------------------

selected_engine = test[
    test["engine_id"] == engine_id
].copy()


# ---------------------------------------------------------
# DATA QUALITY MONITORING
# ---------------------------------------------------------

st.markdown("## 🔍 Data Quality Monitoring")

dqc1, dqc2, dqc3 = st.columns(3)

with dqc1:

    st.metric(
        "Missing Values",
        missing_count
    )

with dqc2:

    st.metric(
        "Duplicate Rows",
        duplicate_count
    )

with dqc3:

    st.metric(
        "Sensors Monitored",
        len(features)
    )

if missing_count == 0 and duplicate_count == 0:

    st.success(
        "✓ Data quality check passed: no missing or duplicate records detected."
    )

else:

    st.warning(
        "Data quality issues detected. Review the sensor data."
    )


# ---------------------------------------------------------
# TOP METRICS
# ---------------------------------------------------------

st.markdown("## 📊 Engine Health Overview")

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "Predicted RUL",
        f"{selected['Predicted RUL']:.1f} cycles"
    )

with c2:

    st.metric(
        "Adaptive Health Index",
        f"{selected['Adaptive Health Index']:.1f}/100"
    )

with c3:

    st.metric(
        "Health State",
        selected["Adaptive Health State"]
    )

with c4:

    st.metric(
        "Maintenance Risk",
        selected["Maintenance Risk"]
    )


# ---------------------------------------------------------
# ANOMALY ALERT
# ---------------------------------------------------------

if selected["Anomaly Status"] == "ANOMALY":

    st.error(
        "⚠️ Statistical sensor anomaly detected for the selected engine."
    )

else:

    st.success(
        "✓ No abnormal multivariate sensor pattern detected."
    )


# ---------------------------------------------------------
# ANOMALY DETAILS
# ---------------------------------------------------------

st.markdown("## 🚨 Anomaly Analysis")

a1, a2, a3 = st.columns(3)

with a1:

    st.metric(
        "Anomaly Status",
        selected["Anomaly Status"]
    )

with a2:

    st.metric(
        "Anomaly Severity",
        f"{selected['Anomaly Severity']:.2f}"
    )

with a3:

    st.metric(
        "Severity Level",
        selected["Severity Level"]
    )

st.info(
    "The anomaly score represents statistical sensor deviation from "
    "the training-data distribution. It does not by itself confirm "
    "a physical component fault."
)


# ---------------------------------------------------------
# PREDICTION UNCERTAINTY
# ---------------------------------------------------------

st.markdown("## 📏 Prediction Uncertainty")

u1, u2 = st.columns(2)

with u1:

    st.metric(
        "RUL Uncertainty",
        f"{selected['RUL Uncertainty']:.2f} cycles"
    )

with u2:

    st.metric(
        "Uncertainty Level",
        selected["Uncertainty Level"]
    )

st.info(
    "Uncertainty represents the spread of Random Forest tree predictions. "
    "It is a model uncertainty proxy and should not be interpreted as "
    "a certified confidence interval."
)


# ---------------------------------------------------------
# SENSOR MONITORING
# ---------------------------------------------------------

st.markdown("## 📡 Multi-Sensor Monitoring")

sensor_choice = st.multiselect(
    "Select sensors to monitor",
    features,
    default=[
        "sensor_2",
        "sensor_7",
        "sensor_11"
    ]
)

if len(sensor_choice) > 0:

    fig_sensor = px.line(
        selected_engine,
        x="cycle",
        y=sensor_choice,
        title=f"Sensor Trends — Engine {engine_id}"
    )

    fig_sensor.update_layout(
        hovermode="x unified",
        height=450
    )

    st.plotly_chart(
        fig_sensor,
        use_container_width=True
    )

else:

    st.info(
        "Select at least one sensor."
    )


# ---------------------------------------------------------
# SENSOR DEVIATION EXPLAINABILITY
# ---------------------------------------------------------

st.markdown("## 🔎 Sensor Deviation Analysis")

selected_last = (
    selected_engine
    .sort_values("cycle")
    .iloc[-1]
)

sensor_deviation = (
    (
        selected_last[features]
        - train_sensor_mean
    )
    / train_sensor_std
).abs()

sensor_explainability = pd.DataFrame({
    "Sensor": features,
    "Absolute Deviation": sensor_deviation.values
})

sensor_explainability = (
    sensor_explainability
    .sort_values(
        "Absolute Deviation",
        ascending=False
    )
)

top_sensor_deviation = (
    sensor_explainability
    .head(8)
)

fig_sensor_deviation = px.bar(
    top_sensor_deviation,
    x="Absolute Deviation",
    y="Sensor",
    orientation="h",
    title="Top Sensor Statistical Deviations"
)

st.plotly_chart(
    fig_sensor_deviation,
    use_container_width=True
)

st.info(
    "These values show statistical deviation from the training distribution. "
    "They are explainability indicators, not causal model-attribution scores."
)


# ---------------------------------------------------------
# RUL ANALYSIS
# ---------------------------------------------------------

st.markdown("## 📈 Remaining Useful Life Analysis")

r1, r2 = st.columns(2)

with r1:

    fig_rul = go.Figure()

    fig_rul.add_trace(
        go.Bar(
            x=["Actual RUL"],
            y=[selected["Actual RUL"]],
            name="Actual RUL"
        )
    )

    fig_rul.add_trace(
        go.Bar(
            x=["Random Forest"],
            y=[selected["Random Forest RUL"]],
            name="Random Forest"
        )
    )

    fig_rul.add_trace(
        go.Bar(
            x=["LSTM"],
            y=[selected["LSTM RUL"]],
            name="LSTM"
        )
    )

    fig_rul.update_layout(
        title="Engine RUL Prediction Comparison",
        height=400
    )

    st.plotly_chart(
        fig_rul,
        use_container_width=True
    )

with r2:

    fig_all = px.line(
        results,
        x="Engine ID",
        y=[
            "Random Forest RUL",
            "LSTM RUL"
        ],
        title="RUL Prediction Across Test Engines"
    )

    fig_all.update_layout(
        height=400
    )

    st.plotly_chart(
        fig_all,
        use_container_width=True
    )


# ---------------------------------------------------------
# RUL DEGRADATION TRAJECTORY
# ---------------------------------------------------------

st.markdown("## 📉 Engine Degradation Analysis")

trajectory_engine = selected_engine.sort_values(
    "cycle"
).copy()

trajectory_scaled = trajectory_engine.copy()

trajectory_scaled[features] = scaler.transform(
    trajectory_scaled[features]
)

trajectory_X = []
trajectory_cycles = []

sensor_data = trajectory_scaled[
    features
].values

for i in range(
    sequence_length,
    len(sensor_data) + 1
):

    trajectory_X.append(
        sensor_data[
            i-sequence_length:i
        ]
    )

    trajectory_cycles.append(
        trajectory_engine.iloc[i-1]["cycle"]
    )

if len(trajectory_X) > 0:

    trajectory_X = np.array(
        trajectory_X
    )

    trajectory_predictions = (
        lstm_model
        .predict(
            trajectory_X,
            verbose=0
        )
        .flatten()
    )

    trajectory_predictions = np.clip(
        trajectory_predictions,
        0,
        None
    )

    trajectory = pd.DataFrame({

        "Cycle": trajectory_cycles,

        "Predicted RUL": trajectory_predictions

    })

    trajectory_max = (
        trajectory["Predicted RUL"].max()
    )

    if trajectory_max > 0:

        trajectory["Health Index"] = (
            trajectory["Predicted RUL"]
            / trajectory_max
            * 100
        ).clip(0, 100)

    else:

        trajectory["Health Index"] = 0

    t1, t2 = st.columns(2)

    with t1:

        fig_trajectory = px.line(
            trajectory,
            x="Cycle",
            y="Predicted RUL",
            markers=True,
            title="Predicted RUL Degradation Trajectory"
        )

        fig_trajectory.update_layout(
            xaxis_title="Operating Cycle",
            yaxis_title="Predicted RUL"
        )

        st.plotly_chart(
            fig_trajectory,
            use_container_width=True
        )

    with t2:

        fig_health_trajectory = px.line(
            trajectory,
            x="Cycle",
            y="Health Index",
            markers=True,
            title="Health Index Trajectory"
        )

        fig_health_trajectory.update_layout(
            xaxis_title="Cycle",
            yaxis_title="Health Index",
            yaxis_range=[0, 100]
        )

        st.plotly_chart(
            fig_health_trajectory,
            use_container_width=True
        )

    trajectory_csv = trajectory.to_csv(
        index=False
    )

    st.download_button(
        "📥 Download Degradation Data",
        trajectory_csv,
        file_name=f"engine_{engine_id}_degradation.csv",
        mime="text/csv"
    )

else:

    st.warning(
        "Not enough observed cycles to generate the RUL trajectory."
    )


# ---------------------------------------------------------
# FINITE STATE MACHINE
# ---------------------------------------------------------

st.markdown("## 🔄 Finite State Machine")

states = [
    "NORMAL",
    "CAUTION",
    "DEGRADED",
    "CRITICAL"
]

fsm_cols = st.columns(4)

for i, state in enumerate(states):

    with fsm_cols[i]:

        if state == selected["Adaptive Health State"]:

            st.success(
                f"● {state}"
            )

        else:

            st.info(
                f"○ {state}"
            )

st.markdown(
    """
    **Health transition concept:**

    NORMAL → CAUTION → DEGRADED → CRITICAL
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# FLEET HEALTH DISTRIBUTION
# ---------------------------------------------------------

st.markdown("## 📊 Fleet Health Distribution")

d1, d2 = st.columns(2)

with d1:

    state_counts = (
        results["Adaptive Health State"]
        .value_counts()
        .reset_index()
    )

    state_counts.columns = [
        "Health State",
        "Count"
    ]

    fig_state = px.bar(
        state_counts,
        x="Health State",
        y="Count",
        title="Adaptive Fleet Health States"
    )

    st.plotly_chart(
        fig_state,
        use_container_width=True
    )

with d2:

    fig_health = px.bar(
        results,
        x="Engine ID",
        y="Adaptive Health Index",
        title="Adaptive Health Index by Engine"
    )

    fig_health.update_layout(
        height=400
    )

    st.plotly_chart(
        fig_health,
        use_container_width=True
    )


# ---------------------------------------------------------
# MODEL PERFORMANCE
# ---------------------------------------------------------

st.markdown("## 🧠 AI Model Performance")

performance = pd.DataFrame({

    "Model": [
        "Random Forest",
        "LSTM"
    ],

    "MAE": [
        metrics["Random Forest MAE"],
        metrics["LSTM MAE"]
    ],

    "RMSE": [
        metrics["Random Forest RMSE"],
        metrics["LSTM RMSE"]
    ]

})

st.dataframe(
    performance,
    use_container_width=True,
    hide_index=True
)

fig_performance = px.bar(
    performance,
    x="Model",
    y=[
        "MAE",
        "RMSE"
    ],
    barmode="group",
    title="Model Performance Comparison"
)

st.plotly_chart(
    fig_performance,
    use_container_width=True
)

st.caption(
    "Performance values are based on the offline NASA C-MAPSS FD001 benchmark."
)


# ---------------------------------------------------------
# SENSOR FEATURE IMPORTANCE
# ---------------------------------------------------------

st.markdown("## 🧠 Sensor Feature Importance")

feature_importance_df = pd.DataFrame({
    "Sensor": features,
    "Importance": model.feature_importances_
})

feature_importance_df = (
    feature_importance_df
    .sort_values(
        "Importance",
        ascending=False
    )
)

fig_importance = px.bar(
    feature_importance_df.head(10),
    x="Importance",
    y="Sensor",
    orientation="h",
    title="Top 10 Sensors Used by Random Forest"
)

fig_importance.update_layout(
    height=500
)

st.plotly_chart(
    fig_importance,
    use_container_width=True
)

st.info(
    "Feature importance indicates the relative contribution of "
    "sensor variables to the Random Forest prediction process. "
    "It should not be interpreted as a causal relationship."
)


# ---------------------------------------------------------
# ENGINE TABLE
# ---------------------------------------------------------

st.markdown("## 📋 Engine Monitoring Table")

display_columns = [

    "Engine ID",

    "Predicted RUL",

    "Adaptive Health Index",

    "Adaptive Health State",

    "Anomaly Status",

    "Severity Level",

    "RUL Uncertainty",

    "Uncertainty Level",

    "Maintenance Risk"

]

st.dataframe(
    results[display_columns].round(2),
    use_container_width=True,
    hide_index=True
)


# ---------------------------------------------------------
# DOWNLOAD COMPLETE RESULTS
# ---------------------------------------------------------

st.markdown("## 📥 Reports")

full_results_csv = results.to_csv(
    index=False
)

st.download_button(
    label="📥 Download Complete Fleet Health Report",
    data=full_results_csv,
    file_name="aircraft_health_results.csv",
    mime="text/csv"
)


# ---------------------------------------------------------
# ENGINE HEALTH REPORT
# ---------------------------------------------------------

report = pd.DataFrame({

    "Parameter": [

        "Engine ID",

        "Predicted RUL",

        "Actual RUL",

        "Adaptive Health Index",

        "Health State",

        "Anomaly Status",

        "Anomaly Severity",

        "Severity Level",

        "RUL Uncertainty",

        "Uncertainty Level",

        "Maintenance Risk",

        "Random Forest RUL",

        "LSTM RUL"

    ],

    "Value": [

        engine_id,

        round(
            selected["Predicted RUL"],
            2
        ),

        round(
            selected["Actual RUL"],
            2
        ),

        round(
            selected["Adaptive Health Index"],
            2
        ),

        selected[
            "Adaptive Health State"
        ],

        selected[
            "Anomaly Status"
        ],

        round(
            selected["Anomaly Severity"],
            2
        ),

        selected[
            "Severity Level"
        ],

        round(
            selected["RUL Uncertainty"],
            2
        ),

        selected[
            "Uncertainty Level"
        ],

        selected[
            "Maintenance Risk"
        ],

        round(
            selected["Random Forest RUL"],
            2
        ),

        round(
            selected["LSTM RUL"],
            2
        )

    ]

})

csv_report = report.to_csv(
    index=False
)

st.download_button(
    label="📥 Download Selected Engine Report",
    data=csv_report,
    file_name=f"engine_{engine_id}_health_report.csv",
    mime="text/csv"
)


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

render_html(
    """
    <div class="footer-card">
        <div class="footer-brand">✈️ AROGYA — Aircraft Health Intelligence</div>
        <div class="footer-text">
            Predictive maintenance • Temporal deep learning • RUL estimation •
            Anomaly intelligence • Finite-state health classification
            <br><br>
            Research / academic prototype using multivariate engine sensor data.
            This prototype does not represent certified aircraft maintenance guidance.
        </div>
    </div>
    """
)