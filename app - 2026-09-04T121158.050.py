import math
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
 
os.environ['STREAMLIT_SERVER_PORT'] = '8505'
 
st.set_page_config(layout="wide", page_title="Foreclosure Scenario Calculator")
 
st.markdown("""
<style>
    /* Main container background */
    .stApp {
        background-color: #F8FAFC !important;
    }
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"],
    [data-testid="stHeader"], [data-testid="stSidebar"],
    [data-testid="stMain"], [data-testid="block-container"] {
        background-color: #F8FAFC !important;
    }
    
    /* Panel cards - scoped to the two named containers ONLY, so nested
       3-column rows (Foreclosure fields, Top-up fields) are never matched. */
    div[class*="st-key-chola_card"],
    div[class*="st-key-nb_card"] {
        background-color: #FFFFFF !important;
        padding: 20px !important;
        border-radius: 12px !important;
        border: 1px solid #E2E8F0 !important;
        overflow: hidden !important;
    }
    
    /* Top-up Details full-width card - sits below both panels, always visible */
    div[class*="st-key-topup_card"] {
        background-color: #FFFFFF !important;
        padding: 24px !important;
        border-radius: 12px !important;
        border: 1px solid #E2E8F0 !important;
        margin-top: 24px !important;
        margin-bottom: 24px !important;
    }
    
    .topup-card-title {
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        color: #1E3A8A !important;
        margin-bottom: 16px !important;
    }
    
    /* Radio + checkbox accent colors: navy on the Chola side, pink/burgundy on the New Bank side.
       Streamlit's radio/checkbox are custom BaseWeb widgets (not plain native inputs styled via
       accent-color), so we override the actual visible circle/box/tick elements directly. */
    div[class*="st-key-chola_card"] input[type="radio"],
    div[class*="st-key-chola_card"] input[type="checkbox"] {
        accent-color: #1E3A8A !important;
    }
    div[class*="st-key-chola_card"] [data-testid="stCheckbox"] span[aria-hidden="true"],
    div[class*="st-key-chola_card"] [role="checkbox"] span[aria-hidden="true"],
    div[class*="st-key-chola_card"] [data-testid="stRadio"] label > div:first-child,
    div[class*="st-key-chola_card"] [data-baseweb="radio"] > div:first-child,
    div[class*="st-key-chola_card"] [role="radio"] {
        border-color: #1E3A8A !important;
    }
    div[class*="st-key-chola_card"] [role="checkbox"][aria-checked="true"] span[aria-hidden="true"],
    div[class*="st-key-chola_card"] [data-testid="stCheckbox"] span[aria-hidden="true"][data-checked="true"],
    div[class*="st-key-chola_card"] [role="radio"][aria-checked="true"] > div:first-child,
    div[class*="st-key-chola_card"] [data-baseweb="radio"] > div:first-child > div {
        background-color: #1E3A8A !important;
        border-color: #1E3A8A !important;
    }
    div[class*="st-key-chola_card"] [data-testid="stCheckbox"] svg,
    div[class*="st-key-chola_card"] [data-testid="stRadio"] svg {
        fill: #1E3A8A !important;
    }
    
    div[class*="st-key-nb_card"] input[type="radio"],
    div[class*="st-key-nb_card"] input[type="checkbox"] {
        accent-color: #9D174D !important;
    }
    div[class*="st-key-nb_card"] [data-testid="stCheckbox"] span[aria-hidden="true"],
    div[class*="st-key-nb_card"] [role="checkbox"] span[aria-hidden="true"],
    div[class*="st-key-nb_card"] [data-testid="stRadio"] label > div:first-child,
    div[class*="st-key-nb_card"] [data-baseweb="radio"] > div:first-child,
    div[class*="st-key-nb_card"] [role="radio"] {
        border-color: #9D174D !important;
    }
    div[class*="st-key-nb_card"] [role="checkbox"][aria-checked="true"] span[aria-hidden="true"],
    div[class*="st-key-nb_card"] [data-testid="stCheckbox"] span[aria-hidden="true"][data-checked="true"],
    div[class*="st-key-nb_card"] [role="radio"][aria-checked="true"] > div:first-child,
    div[class*="st-key-nb_card"] [data-baseweb="radio"] > div:first-child > div {
        background-color: #9D174D !important;
        border-color: #9D174D !important;
    }
    div[class*="st-key-nb_card"] [data-testid="stCheckbox"] svg,
    div[class*="st-key-nb_card"] [data-testid="stRadio"] svg {
        fill: #9D174D !important;
    }
    
    /* Expander section title - bigger, bold. Blue on the Chola side (e.g.
       "Foreclosure & Rate Reset"), dark neutral on the New Bank side (e.g. "NB Fees"). */
    .stExpander summary p,
    .stExpander [data-testid="stMarkdownContainer"] p {
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        color: #1E293B !important;
    }
    
    div[class*="st-key-chola_card"] .stExpander summary p,
    div[class*="st-key-chola_card"] .stExpander [data-testid="stMarkdownContainer"] p {
        color: #1E3A8A !important;
    }
    
    /* Panel header banners - full-bleed, rounded top corners only */
    .panel-header-banner {
        margin: -20px -20px 20px -20px !important;
        padding: 16px 20px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        border-radius: 12px 12px 0 0 !important;
    }
    
    .panel-header-chola {
        background-color: #E8F4F8 !important;
        color: #1E3A8A !important;
    }
    
    .panel-header-nb {
        background-color: #FCE8EE !important;
        color: #9D174D !important;
    }
    
    /* Card title styling */
    .card-title {
        font-size: 16px !important;
        font-weight: 700 !important;
        margin: -20px -20px 16px -20px !important;
        padding: 12px 20px !important;
        border-radius: 8px 8px 0 0 !important;
    }
    
    .card-title-chola {
        background-color: #B3D9E8 !important;
        color: #214A82 !important;
    }
    
    .card-title-nb {
        background-color: #E8B3D9 !important;
        color: #980045 !important;
    }
    
    [data-testid="block-container"] {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    
    /* Header styling */
    .header-container {
        background-color: #FFFFFF;
        padding: 20px 40px;
        margin-bottom: 30px;
        border-radius: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        border-bottom: 1px solid #E5E7EB;
    }
    
    .header-logo {
        position: absolute;
        left: 40px;
        height: 60px;
        width: auto;
    }
    
    .header-title {
        text-align: center;
        color: #1E293B;
        font-size: 28px;
        font-weight: 700;
        margin: 0;
    }
    
    .header-subtitle {
        text-align: center;
        color: #000000;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        margin-top: 8px;
    }
    
    /* Card styling */
    .card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 0;
        box-shadow: none;
        border: 1px solid #E2E8F0;
        overflow: hidden;
    }
    
    .card-header {
        padding: 14px 20px;
        border-bottom: none;
        font-size: 16px;
        font-weight: 700;
        margin: 0;
    }
    
    /* Chola header - Blue */
    .card-header-chola {
        background-color: #D4E9F7;
        color: #214A82;
    }
    
    /* New Bank header - Pink/Red */
    .card-header-nb {
        background-color: #F8D7E6;
        color: #980045;
    }
    
    .card-content {
        padding: 20px;
    }
    
    /* Full-width cards */
    .full-width-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 30px;
        box-shadow: none;
        border: 1px solid #E2E8F0;
    }
    
    .card-title {
        font-size: 16px;
        font-weight: 700;
        color: #214A82;
        margin: 0 0 16px 0;
        padding: 0;
    }
    
    .card-title-dark {
        font-size: 16px;
        font-weight: 700;
        color: #0B3B9E;
        margin: 0 0 16px 0;
        padding: 0;
    }
    
    /* Section headers */
    .section-header {
        font-size: 16px;
        font-weight: 700;
        color: #1D4481;
        margin: 16px 0 12px 0;
        padding: 0;
    }
    
    /* Grid layouts */
    .input-grid-2 {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
    }
    
    .input-grid-3 {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 16px;
    }
    
    /* Input field styling */
    .stNumberInput input, .stTextInput input {
        background-color: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        padding: 10px 12px !important;
        font-size: 0.95rem !important;
        color: #1E293B !important;
        min-height: 42px !important;
        box-shadow: none !important;
    }
    
    .stNumberInput input:focus, .stTextInput input:focus {
        border-color: #214A82 !important;
        box-shadow: none !important;
    }
    
    /* Widget labels */
    .stNumberInput label, .stTextInput label {
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        color: #334155 !important;
    }
    
    /* Radio buttons horizontal, pill-like spacing */
    .stRadio [role="radiogroup"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: wrap !important;
        gap: 24px !important;
        align-items: center !important;
        margin-top: 4px !important;
    }
    
    .stRadio > label {
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        color: #334155 !important;
    }
    
    /* Bigger, better-spaced radio dots and checkbox boxes, with proper gap to their label text */
    input[type="radio"] {
        width: 20px !important;
        height: 20px !important;
        cursor: pointer !important;
    }
    
    input[type="checkbox"] {
        width: 20px !important;
        height: 20px !important;
        border-radius: 5px !important;
        cursor: pointer !important;
    }
    
    .stRadio [role="radiogroup"] > label,
    .stCheckbox > label {
        display: flex !important;
        align-items: center !important;
        gap: 10px !important;
    }
    
    .stCheckbox > label > div:first-child,
    .stRadio [role="radiogroup"] > label > div:first-child {
        display: flex !important;
        align-items: center !important;
    }
    
    /* Hide number spinners */
    input[type="number"]::-webkit-inner-spin-button,
    input[type="number"]::-webkit-outer-spin-button {
        -webkit-appearance: none !important;
        display: none !important;
    }
    
    input[type="number"] {
        -moz-appearance: textfield !important;
    }
    
    button[data-testid="stNumberInputStepDown"],
    button[data-testid="stNumberInputStepUp"] {
        display: none !important;
    }
    
    /* Checkbox and radio styling */
    .stCheckbox label {
        font-weight: 600 !important;
        color: #1E293B !important;
        font-size: 0.95rem !important;
    }
    
    .stRadio label {
        font-weight: 500 !important;
        color: #333333 !important;
    }
    
    /* Info box styling */
    .info-box {
        background-color: #FFF5FA;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 16px;
    }
    
    .info-label {
        font-size: 0.85rem;
        font-weight: 500;
        color: #666666;
        margin-bottom: 4px;
    }
    
    .info-value {
        font-size: 1rem;
        font-weight: 700;
        color: #980045;
    }
    
    /* Inner panel styling */
    .inner-panel {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px;
        margin-top: 16px;
    }
    
    .inner-title {
        font-size: 14px;
        font-weight: 700;
        color: #214A82;
        margin: 0 0 12px 0;
        padding: 0;
    }
    
    /* Summary table */
    .summary-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.9rem;
    }
    
    .summary-table thead tr {
        background-color: #E6F2F8;
        border-bottom: 1px solid #E2E8F0;
    }
    
    .summary-table th {
        padding: 12px;
        text-align: left;
        color: #000000;
        font-weight: 600;
    }
    
    .summary-table td {
        padding: 12px;
        border-bottom: 1px solid #E5E7EB;
        color: #333333;
    }
    
    .summary-table tbody tr td:first-child {
        color: #1D4481 !important;
        font-weight: 700 !important;
    }
    
    .summary-table tbody tr:nth-child(even) {
        background-color: #FAFAFA;
    }
    
    .metric-cell {
        color: #1D4481;
        font-weight: 600;
        text-align: left;
    }
    
    .value-cell {
        text-align: right;
        font-family: monospace;
        color: #333333;
    }
    
    /* Recommendation cards */
    .rec-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 12px 16px;
        border: 1px solid;
        box-shadow: none;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .rec-card-green {
        border-color: #D1E7DD;
        background-color: #ECFDF3;
    }
    
    .rec-card-amber {
        border-color: #FFE8A0;
        background-color: #FFFBEB;
    }
    
    .rec-title {
        font-size: 0.9rem;
        font-weight: 700;
        color: #333333;
        margin: 0;
        padding: 0;
        white-space: nowrap;
    }
    
    .rec-text {
        font-size: 0.9rem;
        color: #333333;
        margin: 0;
        padding: 0;
        white-space: nowrap;
    }
    
    .rec-amount-green {
        font-size: 1rem;
        font-weight: 700;
        color: #16A34A;
        white-space: nowrap;
    }
    
    .rec-amount-amber {
        font-size: 1rem;
        font-weight: 700;
        color: #F59E0B;
        white-space: nowrap;
    }
    
    /* Recommendations grid */
    .rec-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        margin-bottom: 30px;
    }
    
    /* Chart container */
    .chart-container {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 30px;
        box-shadow: none;
        border: 1px solid #E2E8F0;
    }
    
    /* Two-column input area */
    .input-area {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        margin-bottom: 30px;
    }
    
    /* Expander styling - CLEAN SINGLE BORDER */
    .stExpander {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        box-shadow: none !important;
    }
    
    .stExpander label {
        font-weight: 600 !important;
        color: #214A82 !important;
        font-size: 0.95rem !important;
    }
    
    /* Container styling for card-like appearance */
    [data-testid="stContainer"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        box-shadow: none !important;
        padding: 20px !important;
        outline: none !important;
    }
    
    /* Responsive design */
    @media (max-width: 1024px) {
        .input-area {
            grid-template-columns: 1fr;
        }
        
        .rec-grid {
            grid-template-columns: 1fr;
        }
        
        .input-grid-3 {
            grid-template-columns: 1fr 1fr;
        }
    }
    
    @media (max-width: 640px) {
        .header-container {
            padding: 15px 20px;
        }
        
        .header-logo {
            display: none;
        }
        
        .input-grid-2, .input-grid-3 {
            grid-template-columns: 1fr;
        }
    }
</style>
""", unsafe_allow_html=True)
 
# Helper functions (ALL CALCULATIONS UNCHANGED)
def pmt(rate_m: float, nper: int, pv: float) -> float:
    if nper <= 0:
        return 0.0
    if abs(rate_m) < 1e-12:
        return pv / nper
    return pv * rate_m / (1 - (1 + rate_m) ** (-nper))
 
def nper_from_emi(rate_m: float, emi: float, pv: float) -> int:
    if emi <= 0:
        return 1
    if abs(rate_m) < 1e-12:
        return int(math.ceil(pv / emi))
    x = 1 - pv * rate_m / emi
    if x <= 0:
        return 1
    n = -math.log(x) / math.log(1 + rate_m)
    return int(math.ceil(max(n, 1)))
 
def pos_after_emis(principal: float, rate_annual_pct: float, tenor_m: int, emis_paid: int) -> float:
    rate_m = rate_annual_pct / 12 / 100
    emi = pmt(rate_m, tenor_m, principal)
    bal = principal
    for _ in range(min(emis_paid, tenor_m)):
        interest = bal * rate_m
        bal -= (emi - interest)
    return max(bal, 0.0)
 
def total_interest_forward(rate_annual_pct: float, tenor_m: int, principal: float) -> float:
    rate_m = rate_annual_pct / 12 / 100
    emi = pmt(rate_m, tenor_m, principal)
    return max(emi * tenor_m - principal, 0.0)
 
def cumulative_principal_paid_single_loan(principal_start: float, rate_annual_pct: float, tenor_m_used: int, num_months: int) -> float:
    if principal_start <= 0 or num_months <= 0 or tenor_m_used <= 0:
        return 0.0
    rate_m = rate_annual_pct / 12 / 100
    emi = pmt(rate_m, tenor_m_used, principal_start)
    cumulative_principal = 0.0
    bal = principal_start
    for _ in range(min(num_months, tenor_m_used)):
        if bal <= 0:
            break
        interest = bal * rate_m
        principal_paid = emi - interest
        if bal < principal_paid:
            principal_paid = bal
        bal -= principal_paid
        cumulative_principal += principal_paid
    return max(cumulative_principal, 0.0)
 
def fmt_indian_int(n: float) -> str:
    try:
        s = f"{int(round(n))}"
    except Exception:
        return "0"
    sign = "" if n >= 0 else "-"
    s = s.lstrip("-")
    if len(s) <= 3:
        return sign + s
    last3 = s[-3:]
    rest = s[:-3]
    parts = []
    while len(rest) > 2:
        parts.insert(0, rest[-2:])
        rest = rest[:-2]
    if rest:
        parts.insert(0, rest)
    return sign + ",".join(parts + [last3])
 
def fmt_inr(n: float) -> str:
    return f"₹ {fmt_indian_int(abs(n))}"
 
def fmt_pct(x: float) -> str:
    return f"{x:.2f}%"
 
# Header
try:
    with open('Chola.png', 'rb') as f:
        logo_data = __import__('base64').b64encode(f.read()).decode()
    header_html = f"""
    <div class="header-container">
        <img src="data:image/png;base64,{logo_data}" alt="Logo" class="header-logo">
        <div style="text-align: center;">
            <h1 class="header-title">Foreclosure Scenario Calculator</h1>
            <p class="header-subtitle">NB Fees inside right column + Colored Recommendations</p>
        </div>
    </div>
    """
except Exception:
    header_html = """
    <div class="header-container">
        <div style="text-align: center;">
            <h1 class="header-title">Foreclosure Scenario Calculator</h1>
            <p class="header-subtitle">NB Fees inside right column + Colored Recommendations</p>
        </div>
    </div>
    """
 
st.markdown(header_html, unsafe_allow_html=True)
 
# Session state
if 'topup_amt_val' not in st.session_state:
    st.session_state['topup_amt_val'] = 0.0
if 'ch_topup_rate' not in st.session_state:
    st.session_state['ch_topup_rate'] = 13.00
if 'x_months_input' not in st.session_state:
    st.session_state['x_months_input'] = 12
 
# Two-column input layout
col_chola, col_nb = st.columns(2, gap="large")
 
with col_chola:
  with st.container(key="chola_card"):
    st.markdown('<div class="panel-header-banner panel-header-chola">Chola (Existing Loan)</div>', unsafe_allow_html=True)
    
    # Chola main inputs - 2x2 grid
    l1, l2 = st.columns(2, gap="small")
    with l1:
        ch_principal = st.number_input("Loan Amount", value=1000000.0, format="%f")
        ch_tenor_m = st.number_input("Total Tenure (Months)", value=120, format="%d")
    with l2:
        ch_rate = st.number_input("Current Rate (%)", value=13.00, format="%.2f")
        emis_paid = st.number_input("EMIs Paid (Months)", value=24, format="%d")
 
    balance_tenure = max(ch_tenor_m - emis_paid, 0)
    pos_today = pos_after_emis(ch_principal, ch_rate, ch_tenor_m, emis_paid)
 
    # Foreclosure & Rate Reset - bordered section
    with st.expander("Foreclosure & Rate Reset", expanded=True):
        rr1, rr2, rr3 = st.columns(3, gap="small")
        with rr1:
            fc_pct = st.number_input("Foreclosure Charge (%)", value=4.00, format="%.2f")
        with rr2:
            rr_delta_pct = st.number_input("Revised Rate (%)", value=12.00, format="%.2f")
        with rr3:
            rr_fee_pct = st.number_input("Reset Fee (%)", value=1.00, format="%.2f")
        rr_mode = st.radio("Reset Mode", ["Keep EMI same", "Keep Tenure same"], index=0, horizontal=True)
 
with col_nb:
  with st.container(key="nb_card"):
    foreclosure_inr = pos_today * (fc_pct / 100)
    prefill_nb_loan_amt_base = pos_today + foreclosure_inr
 
    st.markdown('<div class="panel-header-banner panel-header-nb">New Bank (Shift)</div>', unsafe_allow_html=True)
    
    # New Bank main inputs - full-width stacked layout
    auto_nb_prefill = st.checkbox("Auto-calc Loan Amt (POS + Foreclosure Fee)", value=True)
    
    if auto_nb_prefill:
        nb_loan_amt_input = float(prefill_nb_loan_amt_base)
        st.markdown(f"""
        <div style="background: #FFF0F5; border: 1px solid #FBCFE8; border-radius: 12px; padding: 16px; margin: 12px 0 16px 0;">
            <div style="font-weight: 700; font-size: 1rem; color: #9D174D;">Loan Amt (POS + FC): {fmt_inr(nb_loan_amt_input)}</div>
            <div style="color: #6B7280; font-size: 13px; margin-top: 4px;">Auto-calculated NB Loan Amount (POS + FC). Top-up is separate.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        nb_loan_amt_input = st.number_input("NB Loan Amt (POS + FC)", value=prefill_nb_loan_amt_base, format="%f")
    
    nb_rate = st.number_input("New Bank Rate (%)", value=11.00, format="%.2f")
    
    st.markdown('<div style="font-size: 0.85rem; font-weight: 600; color: #334155; margin-bottom: 4px;">NB Calculation Mode</div>', unsafe_allow_html=True)
    nb_mode_sel = st.radio("NB Calculation Mode", ["Keep Tenure same", "Keep EMI same", "Manual Tenure"], horizontal=True, label_visibility="collapsed")
    if nb_mode_sel == "Manual Tenure":
        nb_manual_tenor = st.number_input("Manual Tenure (Months)", value=int(balance_tenure), step=1, format="%d")
    
    # NB Fees expander
    with st.expander("NB Fees", expanded=False):
        f1, f2, f3 = st.columns(3, gap="small")
        with f1:
            nb_admin_pct = st.number_input("Admin Fee (%)", value=1.00, format="%.2f")
        with f2:
            nb_cross_sell_pct = st.number_input("Cross Sell (%)", value=2.00, format="%.2f")
        with f3:
            nb_modt_fee = st.number_input("MOD/Other (₹)", value=25000.0, format="%f")
 
# Top-up Details & Principal Contribution - own full-width row below both panels, always visible (no dropdown)
with st.container(key="topup_card"):
    st.markdown('<div class="topup-card-title">Top-up Details &amp; Principal Contribution</div>', unsafe_allow_html=True)
    td1, td2, td3 = st.columns(3, gap="small")
    with td1:
        topup_amt = st.number_input("Top-up Amount (₹)", value=st.session_state.get('topup_amt_val', 0.0), format="%f", min_value=0.0, key="topup_amt_key")
        st.session_state['topup_amt_val'] = topup_amt
    with td2:
        ch_topup_rate_final = st.number_input("Chola Top-up Rate%", value=st.session_state.get('ch_topup_rate', 13.00), format="%.2f", key="ch_topup_rate_key")
        st.session_state['ch_topup_rate'] = ch_topup_rate_final
    with td3:
        x_months = st.number_input("Principal Contribution (Months)", value=st.session_state.get('x_months_input', 12), min_value=1, format="%d", key="x_months_input")
 
    # Placeholder for NB Principal Total display
    topup_info_placeholder = st.empty()
 
# CALCULATIONS (UNCHANGED)
ch_current_principal_total = pos_today + topup_amt
ch_current_tenure_used = balance_tenure
emi_orig_cur = pmt(ch_rate/12/100, ch_current_tenure_used, pos_today)
emi_topup_cur = pmt(ch_topup_rate_final/12/100, ch_current_tenure_used, topup_amt)
emi_chola_current_final_combined = emi_orig_cur + emi_topup_cur
 
ch_reset_rate = rr_delta_pct
rr_fee_inr = pos_today * (rr_fee_pct / 100)
rr_principal_total = pos_today + topup_amt
r_m_reset = ch_reset_rate / 12 / 100
if rr_mode.startswith("Keep EMI"):
    emi_base_for_reset = emi_chola_current_final_combined
    rr_tenure_m_raw = nper_from_emi(r_m_reset, emi_base_for_reset, rr_principal_total)
    rr_tenure_m = min(rr_tenure_m_raw, balance_tenure)
else:
    rr_tenure_m = balance_tenure
emi_orig_rr = pmt(r_m_reset, rr_tenure_m, pos_today)
emi_topup_rr = pmt(r_m_reset, rr_tenure_m, topup_amt)
emi_chola_rr_final_combined = emi_orig_rr + emi_topup_rr
 
nb_topup_amt = topup_amt if auto_nb_prefill else 0.0
nb_principal_total = nb_loan_amt_input + nb_topup_amt
if nb_mode_sel == "Keep EMI same":
    target_emi_nb = emi_chola_current_final_combined
    nb_tenor_used = nper_from_emi(nb_rate/12/100, target_emi_nb, pv=nb_principal_total)
    emi_nb = target_emi_nb
elif nb_mode_sel == "Manual Tenure":
    nb_tenor_used = nb_manual_tenor
    emi_nb = pmt(nb_rate/12/100, nb_tenor_used, nb_principal_total)
else:
    nb_tenor_used = balance_tenure
    emi_nb = pmt(nb_rate/12/100, nb_tenor_used, nb_principal_total)
 
ch_current_total_interest_only = (
    total_interest_forward(ch_rate, ch_current_tenure_used, pos_today)
    + total_interest_forward(ch_topup_rate_final, ch_current_tenure_used, topup_amt)
)
current_other_costs = "—"
chola_current_total_cost = ch_current_total_interest_only
 
rr_total_interest_only = (
    total_interest_forward(ch_reset_rate, rr_tenure_m, pos_today)
    + total_interest_forward(ch_reset_rate, rr_tenure_m, topup_amt)
)
rr_total_cost = rr_total_interest_only + rr_fee_inr
 
nb_admin_fee = nb_principal_total * (nb_admin_pct / 100)
nb_cross_sell_fee = nb_principal_total * (nb_cross_sell_pct / 100)
nb_total_fees_base = nb_admin_fee + nb_cross_sell_fee + nb_modt_fee
nb_interest_total = total_interest_forward(nb_rate, nb_tenor_used, nb_principal_total)
 
if auto_nb_prefill:
    shift_cost_total = nb_interest_total + nb_total_fees_base
    nb_fees_breakdown = f"{fmt_inr(nb_total_fees_base)} (Fees)"
else:
    shift_cost_total = nb_interest_total + nb_total_fees_base + foreclosure_inr
    nb_fees_breakdown = f"{fmt_inr(nb_total_fees_base)} (Fees) + {fmt_inr(foreclosure_inr)} (FC Paid to Chola)"
 
principal_contrib_cur = cumulative_principal_paid_single_loan(ch_current_principal_total, ch_rate, ch_current_tenure_used, x_months)
principal_contrib_rr = cumulative_principal_paid_single_loan(rr_principal_total, ch_reset_rate, rr_tenure_m, x_months)
principal_contrib_nb = cumulative_principal_paid_single_loan(nb_principal_total, nb_rate, nb_tenor_used, x_months)
 
# Display NB Principal Total
topup_info_placeholder.markdown(f'''
<div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 16px; margin-top: 12px; margin-bottom: 30px; width: 100%;">
    <div style="font-size: 0.9rem; font-weight: 600; color: #666666; display: inline;">NB Principal Total (incl. Top-up):</div>
    <div style="font-size: 0.95rem; font-weight: 700; color: #E7262B; display: inline; margin-left: 8px;">{fmt_inr(nb_principal_total)}</div>
</div>
''', unsafe_allow_html=True)
 
chola_original_emi = pmt(ch_rate/12/100, ch_tenor_m, ch_principal)
emis_paid_total = emis_paid * chola_original_emi
principal_paid_to_date = ch_principal - pos_today
interest_paid_to_date = emis_paid_total - principal_paid_to_date
emi_paid_td_text = f"{fmt_inr(emis_paid_total)} ({fmt_indian_int(principal_paid_to_date)} P + {fmt_indian_int(interest_paid_to_date)} I)"
 
rr_other_costs_text = f"{fmt_inr(rr_fee_inr)} (RR Fee)"
emi_lbl_cur = fmt_inr(emi_chola_current_final_combined) + f" [{fmt_indian_int(emi_orig_cur)} Orig + {fmt_indian_int(emi_topup_cur)} Top]"
emi_lbl_rr = fmt_inr(emi_chola_rr_final_combined) + f" [{fmt_indian_int(emi_orig_rr)} Orig + {fmt_indian_int(emi_topup_rr)} Top]"
 
if rr_tenure_m < ch_current_tenure_used:
    tenure_saved = ch_current_tenure_used - rr_tenure_m
    emi_saved_value = tenure_saved * emi_chola_rr_final_combined
    rr_other_costs_text = f"{fmt_inr(rr_fee_inr)}\n(RR Fee)\n\nBenefit:\n{fmt_inr(emi_saved_value)}\n(over {tenure_saved}M)"
 
delta_vs_current = chola_current_total_cost - shift_cost_total
delta_vs_reset = rr_total_cost - shift_cost_total
 
if delta_vs_current > 0:
    delta_current_display = f"₹ -{fmt_indian_int(delta_vs_current)}"
else:
    delta_current_display = f"₹ +{fmt_indian_int(abs(delta_vs_current))}"
 
if delta_vs_reset > 0:
    delta_rr_display = f"₹ -{fmt_indian_int(delta_vs_reset)}"
else:
    delta_rr_display = f"₹ +{fmt_indian_int(abs(delta_vs_reset))}"
 
# SUMMARY TABLE
rate_reset_result = fmt_pct(ch_reset_rate)
 
rows_data = [
    ("Loan Value", fmt_inr(ch_current_principal_total), fmt_inr(rr_principal_total), fmt_inr(nb_principal_total)),
    ("Rate %", fmt_pct(ch_rate), rate_reset_result, fmt_pct(nb_rate)),
    ("Future Tenure", f"{ch_current_tenure_used} M", f"{rr_tenure_m} M", f"{nb_tenor_used} M"),
    ("EMI Paid Till Date", emi_paid_td_text, emi_paid_td_text, "—"),
    (f"Principal Contrib. (Next {x_months} M)", fmt_inr(principal_contrib_cur), fmt_inr(principal_contrib_rr), fmt_inr(principal_contrib_nb)),
    ("EMI (Combined)", emi_lbl_cur, emi_lbl_rr, fmt_inr(emi_nb)),
    ("Future Interest", fmt_inr(ch_current_total_interest_only), fmt_inr(rr_total_interest_only), fmt_inr(nb_interest_total)),
    ("Other Costs", current_other_costs, rr_other_costs_text, nb_fees_breakdown),
    ("Total Cost", fmt_inr(chola_current_total_cost), fmt_inr(rr_total_cost), fmt_inr(shift_cost_total)),
    ("Delta vs NB", delta_current_display, delta_rr_display, "—"),
]
 
# Build table HTML as complete string
table_html = '<div class="full-width-card"><h3 class="card-title">Summary</h3><table class="summary-table"><thead><tr><th>Metric</th><th>Chola (Current)</th><th>Chola (Rate Reset)</th><th>New Bank</th></tr></thead><tbody>'
for metric, val_current, val_reset, val_nb in rows_data:
    table_html += f'<tr><td style="color: #1D4481 !important; font-weight: 600; text-align: left; padding: 12px;">{metric}</td><td class="value-cell">{val_current}</td><td class="value-cell">{val_reset}</td><td class="value-cell">{val_nb}</td></tr>'
table_html += '</tbody></table></div>'
 
st.markdown(table_html, unsafe_allow_html=True)
 
# RECOMMENDATIONS
cost_current = chola_current_total_cost
cost_shift = shift_cost_total
cost_rr = rr_total_cost
 
delta_current = cost_current - cost_shift
if delta_current > 0:
    rec_current_recommendation = "SHIFT to New Bank"
    rec_current_savings = fmt_inr(delta_current)
else:
    rec_current_recommendation = "STAY with Chola"
    rec_current_savings = fmt_inr(abs(delta_current))
 
delta_rr = cost_rr - cost_shift
if delta_rr > 0:
    rec_rr_recommendation = "SHIFT to New Bank"
    rec_rr_benefit = fmt_inr(delta_rr)
else:
    rec_rr_recommendation = "STAY with Chola"
    rec_rr_benefit = fmt_inr(abs(delta_rr))
 
st.markdown(f'''
<div class="rec-grid">
    <div class="rec-card rec-card-amber">
        <div class="rec-title">Chola Current vs New Bank:</div>
        <div class="rec-text">{rec_current_recommendation}</div>
        <div class="rec-amount-amber">{rec_current_savings}</div>
    </div>
    <div class="rec-card rec-card-green">
        <div class="rec-title">Chola Rate Reset vs New Bank:</div>
        <div class="rec-text">{rec_rr_recommendation}</div>
        <div class="rec-amount-green">{rec_rr_benefit}</div>
    </div>
</div>
''', unsafe_allow_html=True)
 
# COST CHART
with st.expander("📊 Cost Composition Chart", expanded=False):
    scenarios = ["Chola Current", "Chola Rate Reset", "New Bank"]
    int_vals = [ch_current_total_interest_only, rr_total_interest_only, nb_interest_total]
    fees_rr = rr_fee_inr
    fees_current = 0.0
    fees_nb = nb_total_fees_base
    fee_vals = [fees_current, fees_rr, fees_nb]
    
    fig = go.Figure()
    fig.add_bar(name="Future Interest", x=scenarios, y=int_vals, marker_color="#0B3B9E",
                text=[fmt_inr(v) for v in int_vals], textposition="inside")
    fig.add_bar(name="Fees/Other Costs", x=scenarios, y=fee_vals, marker_color="#F58518",
                text=[fmt_inr(v) for v in fee_vals], textposition="inside")
    fig.update_layout(barmode='stack', title_text="Total Cost Composition", yaxis_title="Cost (₹)", height=450, margin=dict(t=80, b=60, l=80, r=60), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(248,249,250,1)")
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(200,200,200,0.2)")
    totals = [chola_current_total_cost, rr_total_cost, shift_cost_total]
    fig.update_layout(annotations=[
        dict(x=scenarios[i], y=totals[i], text=fmt_inr(totals[i]), showarrow=False, yshift=15, font=dict(size=12, color="#0B3B9E", family="sans-serif"))
        for i in range(3)
    ])
    st.plotly_chart(fig, use_container_width=True)
 
 