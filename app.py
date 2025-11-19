import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
import os

# 1. AGENCY BRANDING SETUP
st.set_page_config(
    page_title="Lou's Agency | Intelligence Engine", 
    layout="wide",
    page_icon="🚀",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS STYLING (The "Premium" Look) ---
def apply_custom_style():
    st.markdown("""
        <style>
        /* IMPORT FONT */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
        
        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif;
            background-color: #0E1117; 
            color: #FAFAFA;
        }
        
        /* SIDEBAR STYLE */
        [data-testid="stSidebar"] {
            background-color: #161B22;
            border-right: 1px solid #30363D;
        }
        
        /* METRIC CARDS (Glassmorphism) */
        div[data-testid="stMetric"] {
            background: rgba(30, 30, 30, 0.5);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            transition: transform 0.2s ease-in-out;
        }
        div[data-testid="stMetric"]:hover {
            transform: translateY(-5px);
            border-color: #00CC96; /* Brand Green Accent */
            box-shadow: 0 8px 24px rgba(0, 204, 150, 0.2);
        }
        
        /* KEY METRIC LABEL STYLE */
        [data-testid="stMetricLabel"] {
            font-size: 14px;
            color: #9CA3AF;
            font-weight: 500;
        }
        [data-testid="stMetricValue"] {
            font-size: 32px;
            font-weight: 700;
            color: #FFFFFF;
        }

        /* BUTTON STYLE (Gradient CTA) */
        div.stButton > button {
            background: linear-gradient(90deg, #00CC96 0%, #00a87b 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 16px;
            transition: all 0.3s ease;
            width: 100%;
            box-shadow: 0 4px 14px rgba(0, 204, 150, 0.4);
        }
        div.stButton > button:hover {
            background: linear-gradient(90deg, #00a87b 0%, #008c66 100%);
            box-shadow: 0 6px 20px rgba(0, 204, 150, 0.6);
            transform: scale(1.02);
        }
        
        /* DATAFRAME/TABLE CLEANUP */
        [data-testid="stDataFrame"] {
            border: 1px solid #30363D;
            border-radius: 8px;
        }
        
        /* HEADERS */
        h1, h2, h3 {
            letter-spacing: -0.02em;
        }
        </style>
    """, unsafe_allow_html=True)

# Apply the style
apply_custom_style()

# 2. DATA ENGINE
@st.cache_data
def load_data():
    # Load the CSV you generated
    df = pd.read_csv('social_data.csv')
    df['date'] = pd.to_datetime(df['date'])
    # Engagement Score Logic
    df['engagement_score'] = df['likes'] + (df['comments'] * 2) + (df['shares'] * 3)
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"System Error: {e}")
    st.stop()

# --- HERO SECTION ---
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🚀 Lou's Agency: FanLens")
    st.caption("PROPRIETARY INTELLIGENCE ENGINE v1.0")
    
    st.markdown("### Turning Viral Noise into Business Strategy.")
    st.markdown("""
    **The Problem:** In the WNBA's current hyper-growth cycle, standard metrics (Likes/Views) are vanity numbers. They fail to tell an agency if a viral moment is a **commercial opportunity** or a **reputational risk**.
    
    **The FanLens Solution:** This engine allows account managers to answer three critical client questions:
    1.  **💰 Sponsorship Validation:** Prove to brands that engagement is deep & emotional, not just passive scrolling.
    2.  **📉 Risk Detection:** Instantly spot negative sentiment shifts before they become PR crises.
    3.  **🛍️ Merch Prediction:** Identify rising cultural trends to capitalize on real-time demand.
    """)

with col2:
    st.info(
        "**Built by Louis**\n\n"
        "Full-Stack Developer & \n"
        "Political Science Major\n\n"
        "Open for Roles: 2025"
    )

# INSTRUCTIONS
st.success("""
**👇 Workflow:**
* **🟢 Start:** Select one or more client accounts in the sidebar to **compare performance** or isolate specific data.
* **🔎 Analyze:** Review the **Engagement Breakdowns** below to measure the *quality* of fan engagment (Likes vs. Shares).
* **🔭 Discover:** Scroll down to use **Gemini AI** to extract specific, implementable takeaways from the fan conversation.
""")

st.divider()

# 3. SIDEBAR: CLIENT MANAGEMENT
st.sidebar.header("📂 Client Workspace")
selected_brand = st.sidebar.multiselect(
    "Select Client Account",
    options=df['brand'].unique(),
    default=[], # <--- DEFAULT IS NOW EMPTY
    help="Select the client accounts you wish to analyze."
)

# --- GUARD CLAUSE (Stops the app if nothing selected) ---
if not selected_brand:
    st.info("👈 **Welcome, Strategist.** Please select a Client Account in the sidebar to generate the dashboard.")
    st.stop() # <--- Stops the code here. Nothing below runs until they pick a team.

filtered_df = df[df['brand'].isin(selected_brand)]

st.sidebar.markdown("---")

# --- SECURE AI CONNECTION ---
st.sidebar.header("🔐 Security & Access")
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except Exception:
    api_key = None

if not api_key:
    st.sidebar.warning("⚠️ Enter Consultant Key")
    api_key = st.sidebar.text_input("Gemini API Key", type="password")
# 4. QUANTITATIVE METRICS
st.subheader("📊 Market Signals (Quantitative)")
st.caption("Real-time volume and engagement velocity.")

c1, c2, c3 = st.columns(3)
c1.metric("Total Volume", len(filtered_df), help="Total posts in dataset.")
c2.metric("Total Engagement Impact", f"{filtered_df['engagement_score'].sum():,.0f}", help="Weighted engagement score.")
c3.metric("Avg. Impact per Post", f"{filtered_df['engagement_score'].mean():,.0f}")

st.markdown("---")

# 5. TREND VISUALIZATION
chart1, chart2 = st.columns(2)

with chart1:
    st.markdown("##### 📅 Post Volume (Weekly)")
    st.caption(
        "Tracks the volume of **fan mentions, hashtags, and discussions** over time. "
        "We group data by **Week** to smooth out daily noise, making it easier to spot real trends and momentum shifts."
    )
    
    weekly_counts = filtered_df.set_index('date').resample('W').size().reset_index(name='count')
    
    fig = px.line(
        weekly_counts, 
        x='date', 
        y='count', 
        markers=True,
        labels={"count": "Weekly Fan Mentions", "date": "Timeline"},
        line_shape="spline",
        render_mode="svg"
    )
    # Apply the Brand Green color to the chart line/area
    fig.update_traces(fill='tozeroy', line_color='#00CC96') 
    st.plotly_chart(fig, use_container_width=True)

with chart2:
    st.markdown("##### 🏆 Engagement Breakdown")
    
    # UPDATED CAPTION: Explicitly explains the weighting logic
    st.caption(
        "A granular view of engagement quality. We apply a **weighted score** to prioritize high-effort interactions: "
        "**Likes (1x)** < **Comments (2x)** < **Shares (3x)**. This reveals which brands are driving deep advocacy versus just passive reach."
    )
    
    # DATA PREP FOR STACKED CHART
    metrics_df = filtered_df[['brand', 'likes', 'comments', 'shares']]
    metrics_grouped = metrics_df.groupby('brand').sum().reset_index()
    
    melted_df = metrics_grouped.melt(
        id_vars='brand', 
        value_vars=['likes', 'comments', 'shares'],
        var_name='Interaction Type',
        value_name='Count'
    )
    
    melted_df['Interaction Type'] = melted_df['Interaction Type'].str.capitalize()
    
    fig = px.bar(
        melted_df, 
        x='brand', 
        y='Count', 
        color='Interaction Type',
        labels={"brand": "Organization"},
        # Custom "Dark Mode" Palette
        color_discrete_map={
            'Likes': '#4C6EF5',    # Cool Blue
            'Comments': '#FA5252', # Red-Orange
            'Shares': '#00CC96'    # Brand Green
        }
    )
    
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>%{data.name}: %{y:,.0f}<extra></extra>"
    )
    
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# 6. AI STRATEGIST (The "Why")
st.subheader("🧠 Strategic Decoder (Qualitative)")
st.info(
    "**Agency Insight:** This module analyzes the **Top 50 Viral Posts** to decode the cultural context. "
    "It weighs the *type* of engagement (Share vs. Like) to distinguish between passive reach and active advocacy."
)

if st.button("✨ Run Strategic Analysis", type="primary"):
    if not api_key:
        st.error("System Error: Missing API Access Key.")
    else:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # 1. PREPARE DATA (Now including the Breakdown!)
        sorted_df = filtered_df.sort_values(by='engagement_score', ascending=False)
        
        # We pass 'likes', 'comments', 'shares' so the AI can analyze the ratio
        top_posts = sorted_df.head(50)[['text', 'likes', 'comments', 'shares']].to_string(index=False)
        
        general_sample = sorted_df.sample(min(50, len(sorted_df)))['text'].tolist()
        general_text = "\n".join(general_sample)
        
        # 2. DETERMINE MODE
        teams_list = ", ".join(selected_brand)
        if len(selected_brand) > 1:
            mode_instruction = f"User has selected MULTIPLE teams ({teams_list}). Compare their engagement styles."
        else:
            mode_instruction = f"User has selected ONE team ({teams_list}). Deep dive into their specific fan behaviors."

        # 3. THE "INTERACTION INTELLIGENCE" PROMPT
        prompt = f"""
        Act as a Senior Data Strategist at Lou's Agency.
        
        CONTEXT:
        {mode_instruction}
        
        DATASET 1: VIRAL HITS (Top posts by engagement)
        {top_posts}
        
        DATASET 2: GENERAL CHATTER (Random sample)
        {general_text}
        
        **ANALYSIS LOGIC (The "Commitment Index"):**
        * High **Share Ratio** (>15%) = Advocacy & Virality.
        * High **Comment Ratio** (>5%) = Debate & Friction.
        * High **Like Volume** with low ratios = Passive Approval.
        
        Analyze the text AND the engagement ratios to decode the cultural moment.
        
        **IMPORTANT RULES:**
        1. **Format Ratios as Percentages:** (e.g., convert 0.128 to **12.8%**).
        2. **Be "Skimmable":** Use **bolding** for key metrics, specific quotes, and team names.
        3. DO NOT include an introduction. Start directly with the headers.
        
        Output structure:
        
        ### 📈 The Dominant Trend
        (What is the biggest topic? explicitly mention if it is being driven by **Debate** (Comments) or **Hype** (Shares). Cite specific viral posts.)
        
        ### 🧠 The "Why" (Cultural Driver)
        (Why is this trending? Is it Pride, Anger, or FOMO? Use the **engagement %** to prove your point mathematically.)
        
        ### 🎯 Strategic Opportunity
        (Actionable advice. e.g., "Since Share Rate is high (25%), launch a merch drop" or "Since Comment Rate is high (10%), start a poll.")
        """
        
        with st.spinner(f"Decoding engagement signals for: {teams_list}..."):
            try:
                response = model.generate_content(prompt)
                st.success("Analysis Complete")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Connection Error: {e}")
# 7. DATA TRANSPARENCY
with st.expander("📂 View Source Data Ledger"):
    st.dataframe(filtered_df)