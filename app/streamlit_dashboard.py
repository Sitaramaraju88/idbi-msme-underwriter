# app/streamlit_dashboard.py
import sys
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Import your custom pipeline blocks
from services.uli_service import ULIService
from services.aa_service import AAService
from services.ocen_service import OCENService
from agents.base_agent import AgentSignals
from agents.gst_agent import GSTAgent
from agents.upi_agent import UPIAgent
from agents.epfo_agent import EPFOAgent
from agents.aa_agent import AAAgent
from agents.scoring_agent import ScoringAgent

# Initialize pipeline instances
uli = ULIService()
aa = AAService()
ocen = OCENService()

gst_agent = GSTAgent()
upi_agent = UPIAgent()
epfo_agent = EPFOAgent()
banking_agent = AAAgent()
scoring_agent = ScoringAgent()

# Set up clean Streamlit layout page
st.set_page_config(page_title="IDBI Alternate Credit Intelligence", layout="wide")
st.title("🛡️ IDBI Bank MSME Underwriting Hub")
st.subheader("Unified Lending Interface (ULI) & Account Aggregator (AA) Multi-Agent Engine")
st.markdown("---")

# --- Step 1: Discover available mock files ---
MOCK_DIR = "data/mock_personas"
if not os.path.exists(MOCK_DIR) or len(os.listdir(MOCK_DIR)) == 0:
    st.error("⚠️ No mock MSME profiles found! Please execute `python data/synthetic_generator.py` in your terminal first.")
    st.stop()

# Build dropdown mapping list
msme_files = [f for f in os.listdir(MOCK_DIR) if f.startswith("msme_") and f.endswith(".json")]
msme_list = []
for f in msme_files:
    mid = f.replace("msme_", "").replace(".json", "")
    with open(os.path.join(MOCK_DIR, f), "r") as json_f:
        m_data = json.load(json_f)
        b_name = m_data["metadata"]["business_name"]
        arch_type = m_data["metadata"].get("archetype", "unknown").upper().replace("_", " ")
        msme_list.append({"id": mid, "label": f"ID {mid} | {b_name} ({arch_type})"})

msme_df = pd.DataFrame(msme_list).sort_values("id")

# --- Sidebar Configuration Selector ---
st.sidebar.header("🏢 Profile Selector")
selected_label = st.sidebar.selectbox("Choose MSME Profile for Evaluation:", msme_df["label"].tolist())
selected_id = msme_df[msme_df["label"] == selected_label]["id"].values[0]

# --- Step 2: Trigger the Processing Pipeline Execution ---
# 1. Fetch raw data vectors over infrastructure plumbing paths
raw_gst = uli.get_gst_data(selected_id)
raw_upi = uli.get_upi_data(selected_id)
raw_epfo = uli.get_epfo_data(selected_id)
consent_h = aa.request_consent(selected_id)
raw_banking = aa.fetch_consented_banking_data(consent_h)

# Load basic business metadata record details
with open(os.path.join(MOCK_DIR, f"msme_{selected_id}.json"), "r") as f:
    full_profile = json.load(f)
meta = full_profile["metadata"]

# 2. Pipe datasets through downstream specialized parsing agents
shared_state = AgentSignals()
shared_state = gst_agent.process(raw_gst, shared_state)
shared_state = upi_agent.process(raw_upi, shared_state)
shared_state = epfo_agent.process(raw_epfo, shared_state)
shared_state = banking_agent.process(raw_banking, shared_state)

# 3. Compute structural score values & text narration reports
scores = scoring_agent.calculate_scores(shared_state)
credit_memo = scoring_agent.generate_credit_memo(shared_state, scores)
ocen_offer = ocen.generate_loan_offer(selected_id, scores, shared_state.average_monthly_turnover_inr)

# --- Step 3: Render User Interface Dashboard ---

# KPI Headers Block Row Layout
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Selected Business Entity", value=meta["business_name"])
with col2:
    st.metric(label="DPI Credit Segment Profile", value=f"{meta['segment']} ({meta['constitution']})")
with col3:
    grade_color = "🟢" if "LOW" in scores["grade"] else "🟡" if "MEDIUM" in scores["grade"] else "🔴"
    st.metric(label="Assigned Risk Status Grade", value=f"{grade_color} {scores['total_score']} / 1000")
with col4:
    offer = ocen_offer["offer_details"]
    limit_val = f"₹{offer['max_credit_limit_inr']:,}" if offer["is_eligible"] else "NOT ELIGIBLE"
    st.metric(label="Calculated OCEN Capital Limit", value=limit_val)

st.markdown("---")

left_panel, right_panel = st.columns([1, 1])

with left_panel:
    st.subheader("📊 Multi-Dimensional Risk Radar Matrix")
    
    # Structure Plotly Radar Component values mapping matrix pillars
    categories = ['Revenue & Scale Stability', 'Cash Flow Consistency', 'Operational Formality', 'Transaction Maturity']
    max_values = [300, 350, 150, 200]
    current_values = [
        scores["breakdown"]["revenue_stability"],
        scores["breakdown"]["cash_flow_consistency"],
        scores["breakdown"]["operational_formality"],
        scores["breakdown"]["transaction_maturity"]
    ]
    
    # Normalize values out of 100 for clean graphical layout charting geometry
    normalized_scores = [(v / m) * 100 for v, m in zip(current_values, max_values)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=normalized_scores + [normalized_scores[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='MSME Performance Profile Index',
        line_color='#2E7D32' if "LOW" in scores["grade"] else '#EF6C00' if "MEDIUM" in scores["grade"] else '#C62828'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        margin=dict(l=40, r=40, t=20, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

    # Detailed signals diagnostic expander section blocks
    with st.expander("🔍 Inspect Extracted Infrastructure Telemetry Signals"):
        st.write(shared_state.model_dump())

with right_panel:
    st.subheader("📝 Underwriter's AI Credit Memo Narrative")
    st.info("Generated through Multi-Agent aggregation processing analysis layers.")
    st.markdown(credit_memo)

st.markdown("---")
st.subheader("📡 Live OCEN Infrastructure Network Outbound Payload Offer")
st.caption("Standardized transaction payload ready for instant API ecosystem broadcasting transmission routing.")
st.json(ocen_offer)