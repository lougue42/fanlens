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
    
    st.markdown("### Turning Viral Noise into Business Strategy")
    st.markdown("""
    **The Problem:** In the WNBA's current hyper-growth cycle, standard metrics such as Likes and Views are vanity numbers. They fail to tell an agency if a viral moment is a **commercial opportunity** or a **reputational risk**.
    
    **The Solution:** This engine allows account managers to answer three critical client questions:
    1.  **💰 Sponsorship Validation:** Prove to brands that engagement is deep & emotional, not just passive scrolling.
    2.  **📉 Risk Detection:** Instantly spot negative sentiment shifts before they become PR crises.
    3.  **🛍️ Merch Prediction:** Identify rising cultural trends to capitalize on real-time demand.
    """)


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
st.subheader("📊 Engagement Overview")
st.caption("Real-time volume and engagement velocity, visualized.")

c1, c2, c3 = st.columns(3)
c1.metric("Total Volume", len(filtered_df), help="Total posts in dataset.")
c2.metric("Total Engagement Impact", f"{filtered_df['engagement_score'].sum():,.0f}", help="Weighted engagement score.")
c3.metric("Avg. Impact per Post", f"{filtered_df['engagement_score'].mean():,.0f}")

st.markdown("---")

# 5. TREND VISUALIZATION
chart1, chart2 = st.columns(2)

with chart1:
    st.markdown("##### 📅 Post Volume")
    st.caption(
        "Tracks the volume of **fan mentions, hashtags, and discussions** over time. "
        "Data is grouped by **Week** to smooth out daily noise, making it easier to spot real trends and momentum shifts."
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
    
    # --- UPDATED TOOLTIP (Clean Date & Volume) ---
    # %{x|%b %d, %Y} = Formats date like "Sep 21, 2025"
    # <extra></extra> = Removes the annoying "trace 0" box
    fig.update_traces(
        fill='tozeroy', 
        line_color='#00CC96',
        hovertemplate="<b>Week of %{x|%b %d, %Y}</b><br>Volume: %{y}<extra></extra>"
    )
    
    st.plotly_chart(fig, use_container_width=True)

with chart2:
    st.markdown("##### 🏆 Engagement Breakdown")
    
    # UPDATED CAPTION: Explicitly explains the weighting logic
    st.caption(
        "A granular view of engagement quality. A **weighted score** is applied to prioritize high-effort interactions: "
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
st.subheader("🧠 Strategy Report") 
st.info(
    "**Agency Insight:** This module generates an instant **Gap Analysis**. It compares the 'Viral Hits' (what the algorithm loves) "
    "against 'General Chatter' (what the community is actually feeling) to spot disconnects and opportunities."
)

if st.button("✨ Generate Report", type="primary"):
    if not api_key:
        st.error("System Error: Missing API Access Key.")
    else:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # DATA PREP
        sorted_df = filtered_df.sort_values(by='engagement_score', ascending=False)
        
        # 1. Viral Hits (Top 20)
        top_posts = sorted_df.head(20)[['brand', 'text', 'likes', 'shares']].to_string(index=False)
        
        # 2. General Chatter (Random 20)
        general_sample = sorted_df.sample(min(20, len(sorted_df)))[['brand', 'text']].to_string(index=False)
        
        teams_list = ", ".join(selected_brand)
        
        # CONTEXT LOGIC
        if len(selected_brand) > 2:
            strategy_mode = "COMPARATIVE RANKING. Focus on the disparity between the market leader and the challengers."
        else:
            strategy_mode = "DEEP DIVE. Focus on the specific emotional nuance of this specific fanbase."

        prompt = f"""
        Act as a Lead Strategist at Lou's Agency.
        
        STRATEGY MODE: {strategy_mode}
        TEAMS ANALYZED: {teams_list}
        
        DATASET 1: VIRAL HITS (High Engagement)
        {top_posts}
        
        DATASET 2: GENERAL CHATTER (Organic/Random)
        {general_sample}
        
        **LOGIC FRAMEWORK (The Commitment Index):**
        * **Share Rate** = (Shares / Likes).
        * High Share Rate (>15%) = **Advocacy** (Viral Movement).
        * High General Noise without Virality = **Stagnation**.
        
        Produce a strategic memo using the structure below.
        
        **OUTPUT FORMAT (Strict Markdown):**
        
        ### 📈 The Dominant Trend
        (Synthesize the narrative. Does the 'Viral' story align with the 'Organic' sentiment?
         * **The Verdict:** (One sentence summary.)
         * **The Evidence:** (Group by team. Limit to Top 3 quotes per team.
           **FORMATTING RULES:**
           - Use blockquotes (>) for EVERY quote.
           - **BOLD** the Share Rate stats (e.g. **45% Share Rate**).
           
           * **Team A:**
             * > "Quote" (**44% Share Rate**)
             * > "Quote" (Organic Sentiment)
           * **Team B:**
             * > "Quote" (Organic Sentiment)))
        
        ### 🧠 Cultural Drivers
        (Decode the emotional engine. Is this trend driven by **Validation** (fans projecting identity via Shares) or **Friction** (fans debating controversy via Comments)?
         Use the **calculated Share Rates** to prove which specific emotion is fueling the algorithm.)
        
        ### 🎯 Strategic Opportunity
        (Group recommendations by Team.)
        * **Team A:**
             * **The Pivot:** (1 sentence direction on the angle the brand should adopt)
             * **The Payoff:** (Why this will work for this specific audience)
        * **Team B:**
             * **The Pivot:** (1 sentence direction)
             * **The Payoff:** (Why it works)
        """
        
        with st.spinner(f"Analyzing Narrative Gaps for: {teams_list}..."):
            try:
                response = model.generate_content(prompt)
                st.success("Strategic Memo Generated")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Connection Error: {e}")
# --- FOOTER & TRANSPARENCY ---
st.markdown("---")

# 1. The Disclaimer (Professional Context)
st.caption(
    "**Note:** This dashboard is a functional prototype demonstrating both quantitative + qualitative analytics architecture. "
    "Due to enterprise API constraints (lack of Twitter access), data sources are currently simulated based on real-world 2025 WNBA narratives. "
    "**Concept inspired by Breanna Barksdale's lecture on Brand Strategy.**"
)

# 2. The Raw Data (Hidden in the footer as an appendix)
with st.expander("📂 View System Ledger (Raw Data)"):
    st.markdown("### Source Data Verification")
    st.dataframe(filtered_df, use_container_width=True)
