"""
🛠️ Multi-Agent Predictive Maintenance Dashboard
=================================================
Agentic AI System for Industrial Predictive Maintenance
3 Specialized Agents | Advanced RAG | Real-time Diagnostics

Author: Dr. Fatih Hattatoglu
GitHub: https://github.com/fhattat
"""

import onnxruntime
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import requests
import json
import time
import os
import chromadb
from datetime import datetime

# =============================================
# PAGE CONFIG
# =============================================
st.set_page_config(
    page_title="AI Predictive Maintenance",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# CUSTOM CSS
# =============================================
st.markdown("""
<style>
    /* Ana başlık */
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1B2A4A;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #6B7B8D;
        margin-top: -10px;
        margin-bottom: 25px;
    }
    
    /* Metrik kartları */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 12px;
        color: white;
        text-align: center;
    }
    .metric-card-warning {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    .metric-card-success {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    /* Risk badge */
    .risk-critical { 
        background-color: #FF4B4B; color: white; 
        padding: 5px 15px; border-radius: 20px; font-weight: 700;
        display: inline-block; font-size: 0.9rem;
    }
    .risk-warning { 
        background-color: #FFA726; color: white; 
        padding: 5px 15px; border-radius: 20px; font-weight: 700;
        display: inline-block; font-size: 0.9rem;
    }
    .risk-elevated { 
        background-color: #FFD54F; color: #333; 
        padding: 5px 15px; border-radius: 20px; font-weight: 700;
        display: inline-block; font-size: 0.9rem;
    }
    .risk-normal { 
        background-color: #66BB6A; color: white; 
        padding: 5px 15px; border-radius: 20px; font-weight: 700;
        display: inline-block; font-size: 0.9rem;
    }
    
    /* Agent log */
    .agent-step {
        padding: 10px 15px;
        border-left: 4px solid #667eea;
        background: #f8f9ff;
        margin-bottom: 8px;
        border-radius: 0 8px 8px 0;
    }
    
    /* Report box */
    .report-box {
        background: #f0f4f8;
        border: 1px solid #d0d7de;
        border-radius: 10px;
        padding: 20px;
        font-size: 0.95rem;
        line-height: 1.7;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1B2A4A 0%, #2D3E5F 100%);
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    [data-testid="stSidebar"] .stSelectbox label {
        color: #a0b4cc !important;
    }
</style>
""", unsafe_allow_html=True)


# =============================================
# AGENT DEFINITIONS
# =============================================

class SensorAnalystAgent:
    """Ajan 1: Kural tabanlı sensör analizi (LLM kullanmaz)"""
    
    THRESHOLDS = {
        'vibration':   {'normal': (0.60, 0.90), 'warning': (1.10, 1.25), 'critical': 1.30},
        'acoustic':    {'normal': (0.50, 0.70), 'warning': (0.85, 0.95), 'critical': 1.00},
        'temperature': {'normal': (60, 72),     'warning': (76, 82),     'critical': 85},
        'current':     {'normal': (11.5, 13.5), 'warning': (14.5, 15.2), 'critical': 15.5}
    }
    
    FAILURE_MODES = {
        'Tip_A': {
            'name': 'Mekanik Yorgunluk ve Rulman Arızası',
            'conditions': lambda d: d['vibration'] > 1.25 and d['acoustic'] > 0.90
        },
        'Tip_B': {
            'name': 'Elektriksel Aşırı Yük ve Isınma',
            'conditions': lambda d: d['current'] > 15.0 and d['temperature'] > 80
        },
        'Tip_C': {
            'name': 'Akustik Rezonans (Gevşek Parça)',
            'conditions': lambda d: d['acoustic'] > 1.10 and d['vibration'] < 1.10 and d['temperature'] < 76
        }
    }
    
    def _classify(self, param, value):
        t = self.THRESHOLDS[param]
        if value >= t['critical']:
            return 'CRITICAL'
        elif t['warning'][0] <= value <= t['warning'][1]:
            return 'WARNING'
        elif value > t['normal'][1]:
            return 'ELEVATED'
        return 'NORMAL'
    
    def analyze(self, sensor_data: dict) -> dict:
        param_status = {}
        for p in ['vibration', 'acoustic', 'temperature', 'current']:
            v = sensor_data[p]
            s = self._classify(p, v)
            t = self.THRESHOLDS[p]
            param_status[p] = {
                'value': v, 'status': s,
                'normal_range': f"{t['normal'][0]} - {t['normal'][1]}",
                'critical_threshold': t['critical']
            }
        
        failures = []
        for mid, minfo in self.FAILURE_MODES.items():
            if minfo['conditions'](sensor_data):
                failures.append({'mode': mid, 'name': minfo['name']})
        
        imf_alert = None
        if sensor_data.get('IMF_1', 0) > 0.30:
            imf_alert = f"IMF_1 ({sensor_data['IMF_1']:.3f}) > 0.30 — Yapısal çatlak riski!"
        
        statuses = [p['status'] for p in param_status.values()]
        if 'CRITICAL' in statuses: risk = 'CRITICAL'
        elif 'WARNING' in statuses: risk = 'WARNING'
        elif 'ELEVATED' in statuses: risk = 'ELEVATED'
        else: risk = 'NORMAL'
        
        return {
            'timestamp': sensor_data.get('timestamp', 'N/A'),
            'machine_id': sensor_data.get('machine_id', 'N/A'),
            'overall_risk': risk,
            'parameter_analysis': param_status,
            'detected_failure_modes': failures,
            'imf_alert': imf_alert
        }


class KnowledgeRetrieverAgent:
    """Ajan 2: ChromaDB semantic search (LLM kullanmaz)"""
    
    def __init__(self, collection):
        self.collection = collection
    
    def retrieve(self, anomaly_report: dict, n_results: int = 3) -> dict:
        parts = []
        for f in anomaly_report.get('detected_failure_modes', []):
            parts.append(f['name'])
        for p, info in anomaly_report.get('parameter_analysis', {}).items():
            if info['status'] in ['CRITICAL', 'WARNING']:
                parts.append(f"{p} threshold exceeded")
        if anomaly_report.get('imf_alert'):
            parts.append("IMF structural crack")
        
        query = ". ".join(parts) if parts else "machine maintenance procedures"
        results = self.collection.query(query_texts=[query], n_results=n_results)
        
        docs = []
        if results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                docs.append({'content': doc, 'rank': i + 1})
        
        return {
            'query': query,
            'documents': docs,
            'combined_context': "\n\n---\n\n".join([d['content'] for d in docs])
        }


class MaintenancePlannerAgent:
    """Ajan 3: LLM-powered rapor üretici (Groq API)"""
    
    SYSTEM_PROMPT = """Sen Alpha-V8 endüstriyel makineler konusunda 20 yıllık deneyime sahip 
kıdemli bir Bakım Mühendisisin. Sensör analizlerini ve teknik kılavuz bilgilerini
birleştirerek net, uygulanabilir bakım raporları üret.

Raporunda şu yapıyı takip et:
1. DURUM ÖZETİ (1-2 cümle)
2. TESPİT EDİLEN SORUNLAR
3. KÖK NEDEN ANALİZİ
4. ACİL MÜDAHALE PLANI (numaralı)
5. ÖNLEYİCİ BAKIM ÖNERİLERİ

Teknik ve profesyonel bir dil kullan. Türkçe yaz."""

    def generate(self, anomaly_report: dict, context: str, api_key: str) -> str:
        lines = [f"Makine: {anomaly_report['machine_id']} | Zaman: {anomaly_report['timestamp']}"]
        lines.append(f"Risk: {anomaly_report['overall_risk']}")
        for p, info in anomaly_report['parameter_analysis'].items():
            lines.append(f"  {p}: {info['value']} → {info['status']} (Normal: {info['normal_range']})")
        if anomaly_report['detected_failure_modes']:
            lines.append("Arıza Modları:")
            for f in anomaly_report['detected_failure_modes']:
                lines.append(f"  - {f['mode']}: {f['name']}")
        if anomaly_report.get('imf_alert'):
            lines.append(f"IMF: {anomaly_report['imf_alert']}")
        
        user_prompt = f"""[SENSÖR ANALİZİ]:\n{chr(10).join(lines)}\n\n[TEKNİK KILAVUZ]:\n{context}\n\nBakım raporu üret."""
        
        try:
            time.sleep(2)
            resp = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": self.SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": 0.2, "max_tokens": 2000
                }
            )
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"]
            else:
                return f"❌ API Hatası ({resp.status_code}): {resp.json().get('error', {}).get('message', 'Bilinmeyen')}"
        except Exception as e:
            return f"❌ Bağlantı Hatası: {str(e)}"


# =============================================
# DATA & CHROMADB LOADING
# =============================================

@st.cache_data
def load_data():
    """Veri setini yükle ve cache'le."""
    path = os.path.join(os.path.dirname(__file__), 'data', 'raw', 'predictive_maintenance_dataset.csv')
    if not os.path.exists(path):
        # Alternatif path (farklı çalışma dizini)
        alt_paths = [
            'data/raw/predictive_maintenance_dataset.csv',
            '../data/raw/predictive_maintenance_dataset.csv',
            'predictive_maintenance_dataset.csv'
        ]
        for ap in alt_paths:
            if os.path.exists(ap):
                path = ap
                break
    return pd.read_csv(path)


@st.cache_resource
def load_chromadb():
    """ChromaDB koleksiyonunu ONNX embedding ile yükle (PyTorch gerektirmez)."""
    
    # PyTorch gerektirmeyen default embedding (ONNX tabanlı)
    client = chromadb.PersistentClient(path="data/db_app")
    collection = client.get_or_create_collection(name="technical_manual_app")
    
    # Her zaman teknik kılavuzu yükle (küçük veri, saniyeler sürer)
    if collection.count() == 0:
        manual_paths = [
            os.path.join(os.path.dirname(__file__), 'docs', 'technical_manual.md'),
            'docs/technical_manual.md', '../docs/technical_manual.md'
        ]
        for mp in manual_paths:
            if os.path.exists(mp):
                with open(mp, 'r', encoding='utf-8') as f:
                    content = f.read()
                chunks = [c.strip() for c in content.split('##') if len(c.strip()) > 10]
                if not chunks:
                    chunks = [content.strip()]
                collection.add(
                    documents=chunks,
                    ids=[f"id_{i}" for i in range(len(chunks))],
                    metadatas=[{"source": "manual", "part": i} for i in range(len(chunks))]
                )
    
    return collection

# =============================================
# VISUALIZATION HELPERS
# =============================================

def create_gauge_chart(value, param_name, thresholds):
    """Tek parametre için gauge chart oluşturur."""
    t = thresholds
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': param_name.capitalize(), 'font': {'size': 16, 'color': '#1B2A4A'}},
        number={'font': {'size': 28, 'color': '#1B2A4A'}},
        gauge={
            'axis': {'range': [t['normal'][0] * 0.5, t['critical'] * 1.3],
                     'tickwidth': 1, 'tickcolor': "#ccc"},
            'bar': {'color': "#1B2A4A", 'thickness': 0.3},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#e0e0e0",
            'steps': [
                {'range': [t['normal'][0] * 0.5, t['normal'][1]], 'color': '#C8E6C9'},
                {'range': [t['normal'][1], t['warning'][0]], 'color': '#FFF9C4'},
                {'range': [t['warning'][0], t['critical']], 'color': '#FFE0B2'},
                {'range': [t['critical'], t['critical'] * 1.3], 'color': '#FFCDD2'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 3},
                'thickness': 0.8,
                'value': t['critical']
            }
        }
    ))
    fig.update_layout(height=220, margin=dict(l=20, r=20, t=40, b=10))
    return fig


def create_timeline_chart(df_machine, param):
    """Bir makine için zaman serisi grafiği."""
    t = SensorAnalystAgent.THRESHOLDS[param]
    
    fig = go.Figure()
    
    # Normal kayıtlar
    normal = df_machine[df_machine['label'] == 0]
    failure = df_machine[df_machine['label'] == 1]
    
    fig.add_trace(go.Scatter(
        x=normal['timestamp'], y=normal[param],
        mode='lines', name='Normal', line=dict(color='#4FC3F7', width=1.5),
        opacity=0.8
    ))
    
    # Arıza noktaları
    if len(failure) > 0:
        fig.add_trace(go.Scatter(
            x=failure['timestamp'], y=failure[param],
            mode='markers', name='Arıza', 
            marker=dict(color='#FF5252', size=8, symbol='x', line=dict(width=1, color='#B71C1C'))
        ))
    
    # Eşik çizgileri
    fig.add_hline(y=t['warning'][0], line_dash="dash", line_color="#FFA726",
                  annotation_text="Uyarı", annotation_position="top right")
    fig.add_hline(y=t['critical'], line_dash="dash", line_color="#FF5252",
                  annotation_text="Kritik", annotation_position="top right")
    
    fig.update_layout(
        title=f"{param.capitalize()} Zaman Serisi",
        height=280, margin=dict(l=10, r=10, t=40, b=10),
        xaxis_title="", yaxis_title=param.capitalize(),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        template="plotly_white"
    )
    return fig


def create_radar_chart(anomaly_report):
    """Parametre durumlarını radar chart'ta gösterir."""
    params = list(anomaly_report['parameter_analysis'].keys())
    
    # Her parametreyi 0-1 arasına normalize et (critical threshold'a göre)
    values = []
    for p in params:
        info = anomaly_report['parameter_analysis'][p]
        t = SensorAnalystAgent.THRESHOLDS[p]
        normalized = info['value'] / (t['critical'] * 1.2)
        values.append(min(normalized, 1.0))
    values.append(values[0])  # Radar'ı kapat
    params_display = [p.capitalize() for p in params] + [params[0].capitalize()]
    
    fig = go.Figure()
    
    # Kritik eşik çemberi
    fig.add_trace(go.Scatterpolar(
        r=[1/1.2]*5, theta=params_display,
        fill=None, mode='lines',
        line=dict(color='#FF5252', dash='dash', width=1.5),
        name='Kritik Eşik'
    ))
    
    # Gerçek değerler
    fig.add_trace(go.Scatterpolar(
        r=values, theta=params_display,
        fill='toself', fillcolor='rgba(102, 126, 234, 0.2)',
        line=dict(color='#667eea', width=2.5),
        name='Mevcut Değer'
    ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1], showticklabels=False)),
        showlegend=True, height=350, margin=dict(l=40, r=40, t=30, b=30),
        legend=dict(orientation="h", yanchor="bottom", y=-0.15)
    )
    return fig


# =============================================
# MAIN APP
# =============================================

def main():
    # --- SIDEBAR ---
    with st.sidebar:
        st.markdown("## 🛠️ Kontrol Paneli")
        st.markdown("---")
        
        # API Key
        api_key = st.text_input("🔑 Groq API Key", type="password", 
                                help="console.groq.com adresinden ücretsiz alabilirsiniz")
        
        if not api_key:
            st.warning("⚠️ Devam etmek için Groq API Key girin.")
        
        st.markdown("---")
        
        # Veri yükleme
        try:
            df = load_data()
            collection = load_chromadb()
            st.success(f"✅ {df.shape[0]} kayıt yüklendi")
            st.success(f"✅ ChromaDB: {collection.count()} doküman")
        except Exception as e:
            st.error(f"Veri yükleme hatası: {e}")
            return
        
        st.markdown("---")
        
        # Makine seçimi
        machines = sorted(df['machine_id'].unique())
        selected_machine = st.selectbox("🏭 Makine Seçin", machines)
        
        # Kayıt filtresi
        df_machine = df[df['machine_id'] == selected_machine]
        failure_count = df_machine[df_machine['label'] == 1].shape[0]
        
        st.markdown(f"""
        **Makine İstatistikleri:**  
        📊 Toplam kayıt: `{len(df_machine)}`  
        ⚠️ Arıza sayısı: `{failure_count}`  
        ✅ Normal: `{len(df_machine) - failure_count}`
        """)
        
        st.markdown("---")
        
        # Kayıt seçimi
        record_type = st.radio("📋 Kayıt Tipi", ["Arızalı Kayıtlar", "Tüm Kayıtlar"])
        
        if record_type == "Arızalı Kayıtlar":
            df_filtered = df_machine[df_machine['label'] == 1]
        else:
            df_filtered = df_machine
        
        if len(df_filtered) == 0:
            st.info("Bu filtrede kayıt bulunamadı.")
            return
        
        selected_idx = st.selectbox(
            "⏱️ Zaman Damgası",
            df_filtered.index,
            format_func=lambda x: df_filtered.loc[x, 'timestamp']
        )
        
        st.markdown("---")
        st.markdown("##### 🏗️ Mimari")
        st.markdown("""
        `SensorAnalyst` → Kural Tabanlı  
        `KnowledgeRetriever` → RAG  
        `MaintenancePlanner` → LLM
        """)
    
    # --- MAIN CONTENT ---
    st.markdown('<p class="main-header">🛠️ Multi-Agent Predictive Maintenance</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">3 AI Agent • Advanced RAG • Real-time Diagnostics</p>', unsafe_allow_html=True)
    
    # Seçilen kayıt
    selected_record = df.loc[selected_idx].to_dict()
    
    # === BÖLÜM 1: PARAMETRE DASHBOARD ===
    st.markdown("### 📊 Sensör Parametre Dashboard")
    
    gauge_cols = st.columns(4)
    params = ['vibration', 'acoustic', 'temperature', 'current']
    for i, param in enumerate(params):
        with gauge_cols[i]:
            fig = create_gauge_chart(
                selected_record[param], param, SensorAnalystAgent.THRESHOLDS[param]
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # === BÖLÜM 2: ZAMAN SERİSİ GRAFİKLERİ ===
    st.markdown("### 📈 Zaman Serisi Analizi")
    
    ts_cols = st.columns(2)
    for i, param in enumerate(params):
        with ts_cols[i % 2]:
            fig = create_timeline_chart(df_machine, param)
            st.plotly_chart(fig, use_container_width=True)
    
    # === BÖLÜM 3: MULTI-AGENT ANALİZ ===
    st.markdown("---")
    st.markdown("### 🤖 Multi-Agent Analiz")
    
    if not api_key:
        st.info("👈 Sidebar'dan Groq API Key girerek analizi başlatabilirsiniz.")
        return
    
    if st.button("🚀 Analizi Başlat", type="primary", use_container_width=True):
        
        # Agent 1
        with st.status("🔵 Ajan 1: SensorAnalyst çalışıyor...", expanded=True) as status:
            t0 = time.time()
            sensor_agent = SensorAnalystAgent()
            anomaly_report = sensor_agent.analyze(selected_record)
            d1 = time.time() - t0
            st.write(f"✅ Tamamlandı ({d1:.3f}s) → Risk: **{anomaly_report['overall_risk']}**")
            status.update(label=f"🔵 SensorAnalyst ✅ ({d1:.3f}s)", state="complete")
        
        # Agent 2
        with st.status("🟡 Ajan 2: KnowledgeRetriever çalışıyor...", expanded=True) as status:
            t0 = time.time()
            knowledge_agent = KnowledgeRetrieverAgent(collection)
            retrieval = knowledge_agent.retrieve(anomaly_report)
            d2 = time.time() - t0
            st.write(f"✅ Tamamlandı ({d2:.3f}s) → {len(retrieval['documents'])} doküman bulundu")
            status.update(label=f"🟡 KnowledgeRetriever ✅ ({d2:.3f}s)", state="complete")
        
        # Agent 3
        with st.status("🔴 Ajan 3: MaintenancePlanner çalışıyor (LLM)...", expanded=True) as status:
            t0 = time.time()
            planner_agent = MaintenancePlannerAgent()
            report = planner_agent.generate(anomaly_report, retrieval['combined_context'], api_key)
            d3 = time.time() - t0
            st.write(f"✅ Tamamlandı ({d3:.3f}s)")
            status.update(label=f"🔴 MaintenancePlanner ✅ ({d3:.3f}s)", state="complete")
        
        total = d1 + d2 + d3
        
        # === SONUÇLAR ===
        st.markdown("---")
        
        # Sonuç metrikleri
        res_cols = st.columns(4)
        with res_cols[0]:
            risk = anomaly_report['overall_risk']
            risk_class = risk.lower()
            st.markdown(f'<span class="risk-{risk_class}">{risk}</span>', unsafe_allow_html=True)
            st.caption("Genel Risk")
        with res_cols[1]:
            modes = ", ".join([f['mode'] for f in anomaly_report['detected_failure_modes']]) or "—"
            st.metric("Arıza Modu", modes)
        with res_cols[2]:
            st.metric("Pipeline Süresi", f"{total:.2f}s")
        with res_cols[3]:
            st.metric("Getirilen Doküman", f"{len(retrieval['documents'])}")
        
        # Radar chart ve rapor yan yana
        radar_col, report_col = st.columns([1, 2])
        
        with radar_col:
            st.markdown("#### 🎯 Parametre Radar")
            fig = create_radar_chart(anomaly_report)
            st.plotly_chart(fig, use_container_width=True)
            
            # IMF uyarısı
            if anomaly_report.get('imf_alert'):
                st.warning(f"🔬 {anomaly_report['imf_alert']}")
        
        with report_col:
            st.markdown("#### 📋 Bakım Raporu")
            st.markdown(f'<div class="report-box">{report}</div>', unsafe_allow_html=True)
        
        # Pipeline performans detayı
        with st.expander("📊 Pipeline Performans Detayı"):
            perf_df = pd.DataFrame([
                {"Ajan": "🔵 SensorAnalyst", "Tür": "Kural Tabanlı", "Süre (s)": f"{d1:.3f}", "LLM": "Hayır"},
                {"Ajan": "🟡 KnowledgeRetriever", "Tür": "Semantic Search", "Süre (s)": f"{d2:.3f}", "LLM": "Hayır"},
                {"Ajan": "🔴 MaintenancePlanner", "Tür": "LLM Generation", "Süre (s)": f"{d3:.3f}", "LLM": "Evet"},
            ])
            st.dataframe(perf_df, use_container_width=True, hide_index=True)
            
            # Süre dağılımı
            fig_perf = px.bar(
                x=["SensorAnalyst", "KnowledgeRetriever", "MaintenancePlanner"],
                y=[d1, d2, d3],
                color=["SensorAnalyst", "KnowledgeRetriever", "MaintenancePlanner"],
                color_discrete_map={
                    "SensorAnalyst": "#667eea",
                    "KnowledgeRetriever": "#FFA726",
                    "MaintenancePlanner": "#FF5252"
                },
                labels={"x": "Ajan", "y": "Süre (saniye)"},
                title="Ajan Bazında Süre Dağılımı"
            )
            fig_perf.update_layout(showlegend=False, height=300)
            st.plotly_chart(fig_perf, use_container_width=True)
        
        # Getirilen dokümanlar
        with st.expander("📚 RAG - Getirilen Teknik Dokümanlar"):
            st.caption(f"Arama Sorgusu: `{retrieval['query']}`")
            for doc in retrieval['documents']:
                st.markdown(f"**Doküman #{doc['rank']}:**")
                st.code(doc['content'][:500], language=None)


if __name__ == "__main__":
    main()