import streamlit as st
import pandas as pd
from agent import AICustomerSegmentationAgent

# --- Page Configuration ---
st.set_page_config(
    page_title="Web Analytics & Marketing Dashboard",
    page_icon="📊",
    layout="wide"
)

# --- Professional SaaS Styling ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    h1, h2, h3, h4 {
        color: #0f172a !important;
        font-weight: 700;
    }
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Colorful Metric Cards Styling */
    .metric-card-blue {
        background: linear-gradient(135deg, #0ea5e9, #0284c7);
        color: white; padding: 20px; border-radius: 12px;
        box-shadow: 0 4px 6px rgba(14, 165, 233, 0.2);
    }
    .metric-card-cyan {
        background: linear-gradient(135deg, #06b6d4, #0891b2);
        color: white; padding: 20px; border-radius: 12px;
        box-shadow: 0 4px 6px rgba(6, 182, 212, 0.2);
    }
    .metric-card-green {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white; padding: 20px; border-radius: 12px;
        box-shadow: 0 4px 6px rgba(16, 185, 129, 0.2);
    }
    .metric-card-pink {
        background: linear-gradient(135deg, #f43f5e, #e11d48);
        color: white; padding: 20px; border-radius: 12px;
        box-shadow: 0 4px 6px rgba(244, 63, 94, 0.2);
    }
    
    .metric-title {
        font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.9; margin-bottom: 6px; font-weight: 600;
    }
    .metric-value {
        font-size: 1.7rem; font-weight: 700;
    }

    .dashboard-card {
        background: #ffffff; padding: 20px; border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; margin-bottom: 20px;
    }

    /* Professional Email Simulator Container */
    .email-container {
        background: #ffffff;
        color: #1e293b;
        padding: 30px;
        border-radius: 16px;
        border: 1px solid #cbd5e1;
        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
        margin-top: 15px;
    }
    .email-header {
        background: #f1f5f9;
        padding: 15px;
        border-radius: 10px;
        font-size: 0.9rem;
        color: #475569;
        margin-bottom: 20px;
        border-left: 4px solid #4f46e5;
    }
    </style>
""", unsafe_allow_html=True)

# --- Top Header ---
st.title("📊 Web Analytics & AI Marketing Dashboard")
st.markdown("Autonomous customer segmentation, behavioral analytics, and automated email campaign simulator.")
st.markdown("<br>", unsafe_allow_html=True)

# --- Sidebar File Upload ---
with st.sidebar:
    st.header("📂 Data Ingestion")
    uploaded_file = st.file_uploader("Upload CSV or Excel Dataset", type=["csv", "xlsx", "xls"])
    
    st.markdown("---")
    st.markdown("### 🤖 Agent Status")
    st.success("🟢 Online & Ready")
    st.markdown("<p style='font-size: 0.85rem; color: #64748b;'>Automatic schema mapping enabled.</p>", unsafe_allow_html=True)

# --- Main Dashboard Logic ---
if uploaded_file is not None:
    file_path = uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    with st.spinner("✨ AI Agent is parsing records and running analytics..."):
        agent = AICustomerSegmentationAgent(file_path)
        results = agent.run_pipeline("web_campaign_results.csv")
    
    st.success("✅ Dataset successfully analyzed and loaded!")
    st.markdown("<br>", unsafe_allow_html=True)

    # --- DIVISION SELECTOR ---
    st.markdown("### 🎛️ Select Dashboard Division")
    view_mode = st.radio(
        "Choose which section to display:",
        ["Show All Divisions", "1: Executive Performance Metrics", "2: Behavioral Segment Breakdown & Charts", "3: Demo Automated Email Simulator", "4: Master Dataset & Export Center"],
        horizontal=True
    )
    st.markdown("---")

    # ==========================================
    # DIVISION 1: EXECUTIVE PERFORMANCE METRICS
    # ==========================================
    if view_mode in ["Show All Divisions", "1: Executive Performance Metrics"]:
        st.markdown("### 📈 Division 1: Executive Performance Metrics")
        
        total_customers = len(results)
        total_revenue = results['Monetary'].sum() if 'Monetary' in results.columns else 0
        avg_spend = results['Monetary'].mean() if 'Monetary' in results.columns else 0
        champions_count = len(results[results['Segment'] == 'Champions']) if 'Segment' in results.columns else 0

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"""
                <div class="metric-card-blue">
                    <div class="metric-title">Total Customers</div>
                    <div class="metric-value">{total_customers:,}</div>
                </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
                <div class="metric-card-cyan">
                    <div class="metric-title">Total Revenue</div>
                    <div class="metric-value">${total_revenue:,.2f}</div>
                </div>
            """, unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
                <div class="metric-card-green">
                    <div class="metric-title">Average Spend</div>
                    <div class="metric-value">${avg_spend:,.2f}</div>
                </div>
            """, unsafe_allow_html=True)
        with m4:
            st.markdown(f"""
                <div class="metric-card-pink">
                    <div class="metric-title">VIP Champions</div>
                    <div class="metric-value">{champions_count:,}</div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================
    # DIVISION 2: BEHAVIORAL SEGMENTATION
    # ==========================================
    if view_mode in ["Show All Divisions", "2: Behavioral Segment Breakdown & Charts"]:
        st.markdown("### 🎯 Division 2: Behavioral Segmentation & Distributions")
        
        chart_col1, chart_col2 = st.columns(2, gap="large")
        
        with chart_col1:
            st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
            st.markdown("#### 👥 Customer Segment Breakdown")
            if 'Segment' in results.columns:
                seg_table = results['Segment'].value_counts().reset_index()
                seg_table.columns = ['Segment', 'Count']
                st.dataframe(seg_table, use_container_width=True, hide_index=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with chart_col2:
            st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
            st.markdown("#### 📊 Segment Distribution Chart")
            if 'Segment' in results.columns:
                st.bar_chart(results['Segment'].value_counts(), color="#0284c7")
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================
    # DIVISION 3: DEMO AUTOMATED EMAIL SIMULATOR
    # ==========================================
    if view_mode in ["Show All Divisions", "3: Demo Automated Email Simulator"]:
        st.markdown("### ✉️ Division 3: Demo Automated Email Simulator")
        st.markdown("Select any customer ID to preview the automated outbound email campaign crafted by the AI agent.")
        
        selected_customer = st.selectbox("🔍 Select Customer ID for Email Preview:", results['CustomerID'].tolist())
        
        if selected_customer:
            cust_row = results[results['CustomerID'] == selected_customer].iloc[0]
            c_segment = cust_row['Segment']
            c_discount = cust_row['Assigned_Discount_%']
            c_msg = cust_row['Automated_Message']
            c_monetary = cust_row['Monetary']
            
            # Tailor subject based on segment
            subject_map = {
                "Champions": "👑 Exclusive VIP Perk: Early Access & Rewards",
                "At Risk": "⚠️ We miss you! Enjoy a special discount on your return",
                "New Customers": "🌱 Welcome aboard! Unlock your onboarding voucher",
                "Dormant": "✨ Special comeback offer waiting inside for you"
            }
            email_subject = subject_map.get(c_segment, "✨ Your Special Member Update & Rewards")

            st.markdown(f"""
                <div class="email-container">
                    <div class="email-header">
                        <b>From:</b> AI Marketing Hub &lt;campaigns@marketingagent.ai&gt;<br>
                        <b>To:</b> customer_{selected_customer}@gmail.com &nbsp;|&nbsp; <span style="color: #059669; font-weight: bold;">● Status: Sent Automatically</span><br>
                        <b>Subject:</b> {email_subject}
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #e2e8f0; padding-bottom: 15px; margin-bottom: 20px;">
                        <h2 style="color: #4f46e5 !important; margin: 0; font-size: 1.5rem;">⚡ AI Brand Co.</h2>
                        <span style="background: #e0e7ff; color: #3730a3; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: bold; text-transform: uppercase;">Tier: {c_segment}</span>
                    </div>
                    <p style="font-size: 1.05rem; color: #334155;">Hello Customer <b>#{selected_customer}</b>,</p>
                    <div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 20px; border-radius: 12px; font-style: italic; color: #1e293b; font-size: 1.1rem; line-height: 1.6; margin: 15px 0;">
                        "{c_msg}"
                    </div>
                    <div style="background: linear-gradient(135deg, #4f46e5, #6366f1); color: white; padding: 20px; border-radius: 12px; text-align: center; margin-top: 20px;">
                        <p style="margin: 0; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.9;">Your Automated Dynamic Voucher</p>
                        <h3 style="color: white !important; margin: 8px 0; font-size: 1.8rem;">{c_discount}% OFF</h3>
                        <p style="margin: 0; font-size: 0.8rem; opacity: 0.8;">Applied automatically at checkout via your registered profile.</p>
                    </div>
                    <p style="text-align: center; color: #94a3b8; font-size: 0.75rem; margin-top: 25px; margin-bottom: 0;">
                        You received this automated email because of your recent activity profile. Unsubscribe | Privacy Policy
                    </p>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================
    # DIVISION 4: DATASET TABLE & EXPORT CENTER
    # ==========================================
    if view_mode in ["Show All Divisions", "4: Master Dataset & Export Center"]:
        st.markdown("### 📋 Division 4: Master Dataset & Export Center")
        st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
        st.dataframe(results, use_container_width=True)
        
        st.download_button(
            label="📥 Download Master Campaign Results (CSV)",
            data=results.to_csv(index=False).encode('utf-8'),
            file_name='master_marketing_campaigns.csv',
            mime='text/css',
        )
        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info("👈 **Get Started:** Please upload your customer dataset (.csv or .xlsx) in the left sidebar to render the dashboard.")