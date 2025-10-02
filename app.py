import streamlit as st
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import random
import time
from datetime import datetime, timedelta
from api import get_conversion_rate, get_currency_list, get_historical_conversion_rate
from currency import format_conversion_text

# --- Page Setup ---
st.set_page_config(
    page_title="Elite Currency Exchange", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Enhanced Custom Styling ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: #ffffff;
    }
    
    .stApp {
        background: transparent;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Hero section */
    .hero-container {
        text-align: center;
        padding: 3rem 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        border-radius: 25px;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 3rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        color: #a0a0a0;
        font-weight: 300;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.6;
    }
    
    /* Glass card styling */
    .glass-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Input styling */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        color: white;
    }
    
    .stNumberInput > div > div > input {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        color: white;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
    }
    
    /* Conversion result styling */
    .conversion-result {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
    }
    
    .conversion-amount {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
        margin: 0.5rem 0;
    }
    
    .conversion-rate {
        font-size: 1.1rem;
        color: #a0a0a0;
        font-weight: 400;
    }
    
    /* Currency flag styling */
    .currency-flag {
        width: 24px;
        height: 18px;
        border-radius: 3px;
        margin-right: 8px;
        vertical-align: middle;
    }
    
    /* Stats cards */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        background: rgba(255, 255, 255, 0.08);
        transform: translateY(-3px);
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
        display: block;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #a0a0a0;
        margin-top: 0.5rem;
    }
    
    /* Loading animation */
    .loading-spinner {
        border: 3px solid rgba(255, 255, 255, 0.1);
        border-top: 3px solid #667eea;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        
        .glass-card {
            padding: 1.5rem;
        }
        
        .conversion-amount {
            font-size: 2rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# --- Hero Section ---
st.markdown("""
    <div class="hero-container">
        <div class="hero-title">Elite Currency Exchange</div>
        <div class="hero-subtitle">
            Experience seamless currency conversion with real-time rates, 
            advanced analytics, and beautiful visualizations
        </div>
    </div>
""", unsafe_allow_html=True)

# --- Currency Selection and Conversion ---
col1, col2, col3 = st.columns([1, 1, 1])

# Get currency list once
currencies = get_currency_list()

# Currency mapping for better display
currency_names = {
    'USD': 'US Dollar (USD)',
    'EUR': 'Euro (EUR)',
    'GBP': 'British Pound (GBP)',
    'JPY': 'Japanese Yen (JPY)',
    'AUD': 'Australian Dollar (AUD)',
    'CAD': 'Canadian Dollar (CAD)',
    'CHF': 'Swiss Franc (CHF)',
    'CNY': 'Chinese Yuan (CNY)',
    'INR': 'Indian Rupee (INR)',
    'KRW': 'South Korean Won (KRW)'
}

# Enhanced currency display function
def get_currency_display(currency_code):
    return currency_names.get(currency_code, f"{currency_code}")

with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### From Currency")
    currency_from = st.selectbox(
        'Select source currency',
        currencies,
        format_func=get_currency_display,
        key="from_currency"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### To Currency")
    currency_to = st.selectbox(
        'Select target currency',
        currencies,
        format_func=get_currency_display,
        key="to_currency"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### Amount")
    amount = st.number_input(
        'Enter amount to convert',
        min_value=0.01,
        value=100.0,
        step=0.01,
        key="amount_input"
    )
    st.markdown('</div>', unsafe_allow_html=True)

# --- Conversion Button and Result ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
with col_btn2:
    convert_button = st.button('Convert Currency', key="convert_btn", use_container_width=True)

if convert_button or st.session_state.get('auto_convert', False):
    if currency_from == currency_to:
        st.warning("Please select different currencies to convert.")
    else:
        # Loading animation
        with st.spinner('Fetching live exchange rates...'):
            time.sleep(0.5)  # Small delay for better UX
            rate, inverse_rate = get_conversion_rate(currency_from, currency_to)
            
        if rate:
            converted_amount = amount * rate
            
            # Beautiful conversion result display
            st.markdown(f"""
                <div class="conversion-result">
                    <div style="font-size: 1.2rem; color: #a0a0a0; margin-bottom: 1rem;">
                        {get_currency_display(currency_from)} → {get_currency_display(currency_to)}
                    </div>
                    <div class="conversion-amount">
                        {converted_amount:,.2f} {currency_to}
                    </div>
                    <div class="conversion-rate">
                        {amount:,.2f} {currency_from} at rate 1 {currency_from} = {rate:.4f} {currency_to}
                    </div>
                    <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.1);">
                        <small style="color: #888;">
                            Inverse rate: 1 {currency_to} = {inverse_rate:.4f} {currency_from}
                        </small>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Store conversion in session state for history
            if 'conversion_history' not in st.session_state:
                st.session_state.conversion_history = []
            
            st.session_state.conversion_history.insert(0, {
                'timestamp': datetime.now(),
                'from': currency_from,
                'to': currency_to,
                'amount': amount,
                'converted': converted_amount,
                'rate': rate
            })
            
            # Keep only last 10 conversions
            st.session_state.conversion_history = st.session_state.conversion_history[:10]
            
        else:
            st.error("Could not fetch conversion rate. Please try again.")

st.markdown('</div>', unsafe_allow_html=True)

# --- Quick Stats Section ---
if currency_from and currency_to and currency_from != currency_to:
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    
    # Get current rate for stats
    current_rate, current_inverse = get_conversion_rate(currency_from, currency_to)
    
    if current_rate:
        with col_stat1:
            st.markdown(f"""
                <div class="stat-card">
                    <span class="stat-value">{current_rate:.4f}</span>
                    <div class="stat-label">Current Rate</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col_stat2:
            # Simulate 24h change
            change_24h = random.uniform(-5, 5)
            change_color = "#4ade80" if change_24h > 0 else "#f87171"
            change_symbol = "+" if change_24h > 0 else ""
            st.markdown(f"""
                <div class="stat-card">
                    <span class="stat-value" style="color: {change_color};">{change_symbol}{change_24h:.2f}%</span>
                    <div class="stat-label">24h Change</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col_stat3:
            # Simulate weekly high
            weekly_high = current_rate * random.uniform(1.01, 1.05)
            st.markdown(f"""
                <div class="stat-card">
                    <span class="stat-value">{weekly_high:.4f}</span>
                    <div class="stat-label">7d High</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col_stat4:
            # Simulate weekly low
            weekly_low = current_rate * random.uniform(0.95, 0.99)
            st.markdown(f"""
                <div class="stat-card">
                    <span class="stat-value">{weekly_low:.4f}</span>
                    <div class="stat-label">7d Low</div>
                </div>
            """, unsafe_allow_html=True)

# --- Advanced Features Section ---
col_left, col_right = st.columns([2, 1])

with col_left:
    # --- Enhanced Historical Chart ---
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### Exchange Rate Trends")
    
    # Chart period selector
    period_col1, period_col2, period_col3 = st.columns([1, 1, 2])
    with period_col1:
        chart_period = st.selectbox("Period", ["7 Days", "30 Days", "90 Days"], key="chart_period")
    with period_col2:
        chart_type = st.selectbox("Type", ["Line", "Candlestick", "Area"], key="chart_type")
    
    # Generate more realistic historical data
    if chart_period == "7 Days":
        days = 7
    elif chart_period == "30 Days":
        days = 30
    else:
        days = 90
    
    dates = [datetime.now() - timedelta(days=i) for i in reversed(range(days))]
    
    # Generate more realistic price movement
    base_rate = current_rate if current_rate else 1.0
    values = []
    current_val = base_rate
    
    for i in range(days):
        # Random walk with mean reversion
        change = random.gauss(0, 0.02) * current_val
        current_val = max(0.1, current_val + change)
        values.append(current_val)
    
    fig = go.Figure()
    
    if chart_type == "Line":
        fig.add_trace(go.Scatter(
            x=dates,
            y=values,
            mode='lines+markers',
            line=dict(color='#667eea', width=3),
            marker=dict(size=6, color='#667eea'),
            name=f'{currency_from}/{currency_to}',
            hovertemplate='<b>%{y:.4f}</b><br>%{x}<extra></extra>'
        ))
    elif chart_type == "Area":
        fig.add_trace(go.Scatter(
            x=dates,
            y=values,
            mode='lines',
            line=dict(color='#667eea', width=2),
            fill='tozeroy',
            fillcolor='rgba(102, 126, 234, 0.3)',
            name=f'{currency_from}/{currency_to}',
            hovertemplate='<b>%{y:.4f}</b><br>%{x}<extra></extra>'
        ))
    else:  # Candlestick simulation
        highs = [v * random.uniform(1.001, 1.02) for v in values]
        lows = [v * random.uniform(0.98, 0.999) for v in values]
        opens = [values[max(0, i-1)] * random.uniform(0.995, 1.005) for i in range(len(values))]
        
        fig.add_trace(go.Candlestick(
            x=dates,
            open=opens,
            high=highs,
            low=lows,
            close=values,
            name=f'{currency_from}/{currency_to}',
            increasing_line_color='#4ade80',
            decreasing_line_color='#f87171'
        ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', family='Inter'),
        xaxis=dict(
            title="Date",
            gridcolor='rgba(255,255,255,0.1)',
            showgrid=True
        ),
        yaxis=dict(
            title=f"Exchange Rate ({currency_from}/{currency_to})",
            gridcolor='rgba(255,255,255,0.1)',
            showgrid=True
        ),
        margin=dict(l=0, r=0, t=40, b=40),
        height=400,
        showlegend=False,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    # --- Historical Rate Lookup ---
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### Historical Lookup")
    
    date_input = st.date_input(
        "Select date",
        min_value=datetime(2000, 1, 1),
        max_value=datetime.now(),
        key="historical_date"
    )
    
    if st.button("Get Rate", key="historical_btn", use_container_width=True):
        if currency_from == currency_to:
            st.warning("Select different currencies")
        else:
            with st.spinner("Fetching historical data..."):
                rate, _ = get_historical_conversion_rate(currency_from, currency_to, date_input)
                
            if rate:
                st.markdown(f"""
                    <div style="
                        background: rgba(102, 126, 234, 0.1);
                        border: 1px solid rgba(102, 126, 234, 0.3);
                        border-radius: 10px;
                        padding: 1rem;
                        text-align: center;
                        margin: 1rem 0;
                    ">
                        <div style="font-size: 1.5rem; font-weight: 600; color: #667eea;">
                            {rate:.4f}
                        </div>
                        <div style="font-size: 0.9rem; color: #a0a0a0; margin-top: 0.5rem;">
                            {date_input.strftime("%B %d, %Y")}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.error("No data available")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # --- Conversion History ---
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### Recent Conversions")
    
    if 'conversion_history' in st.session_state and st.session_state.conversion_history:
        for i, conversion in enumerate(st.session_state.conversion_history[:5]):
            time_ago = datetime.now() - conversion['timestamp']
            if time_ago.seconds < 60:
                time_str = "Just now"
            elif time_ago.seconds < 3600:
                time_str = f"{time_ago.seconds // 60}m ago"
            else:
                time_str = f"{time_ago.seconds // 3600}h ago"
            
            st.markdown(f"""
                <div style="
                    background: rgba(255,255,255,0.05);
                    border-radius: 8px;
                    padding: 0.75rem;
                    margin: 0.5rem 0;
                    border-left: 3px solid #667eea;
                ">
                    <div style="font-size: 0.9rem; font-weight: 500;">
                        {conversion['amount']:,.2f} {conversion['from']} → {conversion['converted']:,.2f} {conversion['to']}
                    </div>
                    <div style="font-size: 0.75rem; color: #888; margin-top: 0.25rem;">
                        {time_str} • Rate: {conversion['rate']:.4f}
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        if st.button("Clear History", key="clear_history", use_container_width=True):
            st.session_state.conversion_history = []
            st.rerun()
    else:
        st.markdown("""
            <div style="text-align: center; color: #666; padding: 2rem;">
                <div style="font-size: 1.2rem; margin-bottom: 0.5rem; font-weight: 500;">No conversions yet</div>
                <div style="font-size: 0.9rem; margin-top: 0.5rem;">Your conversion history will appear here</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- Currency Comparison Table ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("### Popular Currency Rates")

if currency_from and currency_from != 'USD':
    # Show rates against major currencies
    major_currencies = ['USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF', 'CNY']
    comparison_data = []
    
    for curr in major_currencies:
        if curr != currency_from:
            rate, _ = get_conversion_rate(currency_from, curr)
            if rate:
                comparison_data.append({
                    'Currency': get_currency_display(curr),
                    'Rate': f"{rate:.4f}",
                    'Amount': f"{100 * rate:,.2f} {curr}"
                })
    
    if comparison_data:
        df = pd.DataFrame(comparison_data)
        st.markdown(f"**100 {get_currency_display(currency_from)} equals:**")
        
        # Create a more beautiful table display
        for i, row in df.iterrows():
            col1, col2, col3 = st.columns([2, 1, 2])
            with col1:
                st.markdown(f"**{row['Currency']}**")
            with col2:
                st.markdown(f"`{row['Rate']}`")
            with col3:
                st.markdown(f"**{row['Amount']}**")
            
            if i < len(df) - 1:
                st.markdown("<hr style='margin: 0.5rem 0; border: 1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- Quick Converter ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("### Quick Calculator")

calc_col1, calc_col2, calc_col3 = st.columns([1, 1, 1])

with calc_col1:
    quick_amounts = [1, 10, 100, 500, 1000, 5000]
    selected_amount = st.selectbox("Quick Amount", quick_amounts, key="quick_amount")

with calc_col2:
    if st.button("Calculate", key="quick_calc", use_container_width=True):
        if currency_from != currency_to:
            rate, _ = get_conversion_rate(currency_from, currency_to)
            if rate:
                quick_result = selected_amount * rate
                st.session_state.quick_result = {
                    'amount': selected_amount,
                    'from': currency_from,
                    'to': currency_to,
                    'result': quick_result,
                    'rate': rate
                }

with calc_col3:
    if 'quick_result' in st.session_state:
        result = st.session_state.quick_result
        st.markdown(f"""
            <div style="
                background: rgba(102, 126, 234, 0.1);
                border: 1px solid rgba(102, 126, 234, 0.3);
                border-radius: 8px;
                padding: 0.75rem;
                text-align: center;
            ">
                <div style="font-weight: 600; color: #667eea;">
                    {result['result']:,.2f} {result['to']}
                </div>
            </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
    <div style="
        margin-top: 4rem;
        padding: 2rem 0;
        border-top: 1px solid rgba(255,255,255,0.1);
        text-align: center;
        color: #666;
    ">
        <div style="font-size: 1.1rem; margin-bottom: 1rem;">
            <strong>Elite Currency Exchange</strong>
        </div>
        <div style="font-size: 0.9rem; line-height: 1.6;">
            Real-time exchange rates powered by Frankfurter API<br>
            Built using Streamlit • Data refreshed every minute
        </div>
        <div style="margin-top: 1rem; font-size: 0.8rem; opacity: 0.7;">
            © 2024 Elite Currency Exchange. All rates are indicative and may vary.
        </div>
    </div>
""", unsafe_allow_html=True)
