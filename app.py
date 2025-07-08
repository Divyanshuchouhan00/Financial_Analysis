import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Financial Market Dashboard", layout="wide")

# Load and clean data
@st.cache_data
def load_data():
    df = pd.read_csv("Financial_Analysis.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# Sidebar filters
st.sidebar.title("📊 Filter Options")
market_caps = st.sidebar.multiselect("Market Cap Category", options=df["Market_Cap_Category"].unique(), default=df["Market_Cap_Category"].unique())
sales_cats = st.sidebar.multiselect("Sales Qrt Category", options=df["Sales_Qrt_Category"].unique(), default=df["Sales_Qrt_Category"].unique())
search_company = st.sidebar.text_input("🔍 Search Company Name")
top_n = st.sidebar.slider("Top N Companies (by Market Cap)", 5, 50, 10)

# Apply filters
filtered_df = df[
    (df["Market_Cap_Category"].isin(market_caps)) &
    (df["Sales_Qrt_Category"].isin(sales_cats))
]
if search_company:
    filtered_df = filtered_df[filtered_df["Name"].str.contains(search_company, case=False, na=False)]

filtered_top = filtered_df.sort_values(by="Mar Cap - Crore", ascending=False).head(top_n)

# Dashboard title
st.title("📈 Financial Market Snapshot")
st.markdown("Interactive dashboard for visualizing market capitalization and quarterly sales data of Indian companies.")

# Summary stats
col1, col2, col3 = st.columns(3)
col1.metric("Companies", len(filtered_df))
col2.metric("Avg Market Cap (₹ Cr)", f"{filtered_df['Mar Cap - Crore'].mean():,.2f}")
col3.metric("Avg Sales Qtr (₹ Cr)", f"{filtered_df['Sales Qtr - Crore'].mean():,.2f}")

# Tabs for organization
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📍 Heatmap", "🌳 Treemap", "📋 Raw Data"])

# ➤ Tab 1: Overview Charts
with tab1:
    st.subheader("🏆 Top Companies by Market Cap")
    fig_bar = px.bar(filtered_top, x="Name", y="Mar Cap - Crore", color="Market_Cap_Category", title="Top N Companies by Market Cap")
    st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("📌 Market Cap Category Distribution")
    cap_counts = filtered_df["Market_Cap_Category"].value_counts().reset_index()
    cap_counts.columns = ["Category", "Count"]
    fig_pie = px.pie(cap_counts, values="Count", names="Category", title="Companies by Market Cap Category")
    st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("🔵 Market Cap vs Sales (Bubble Chart)")
    fig_bubble = px.scatter(
        filtered_df,
        x="Sales Qtr - Crore",
        y="Mar Cap - Crore",
        size="Mar Cap - Crore",
        color="Sales_Qrt_Category",
        hover_name="Name",
        size_max=60,
        title="Sales vs Market Cap Bubble Chart"
    )
    st.plotly_chart(fig_bubble, use_container_width=True)

# ➤ Tab 2: Heatmap
with tab2:
    st.subheader("📐 Correlation Heatmap")
    numeric_df = filtered_df[["Mar Cap - Crore", "Sales Qtr - Crore"]]
    corr = numeric_df.corr()

    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", square=True, ax=ax)
    st.pyplot(fig)

# ➤ Tab 3: Treemap
with tab3:
    st.subheader("🌳 Treemap by Market Cap and Sales")
    fig_tree = px.treemap(
        filtered_df,
        path=["Market_Cap_Category", "Sales_Qrt_Category", "Name"],
        values="Mar Cap - Crore",
        color="Sales_Qrt_Category",
        hover_data={"Sales Qtr - Crore": True},
        title="Market Cap Treemap (Size = Market Cap)"
    )
    st.plotly_chart(fig_tree, use_container_width=True)

# ➤ Tab 4: Raw Data & Download
with tab4:
    st.subheader("📋 Filtered Company Data")
    st.dataframe(filtered_top)

    csv = filtered_top.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Data as CSV", data=csv, file_name="filtered_companies.csv", mime="text/csv")

# Footer
st.markdown("---")
st.caption("Built with 💙 by Divyanshu | [GitHub Repo](https://github.com/Divyanshuchouhan00/Financial_Analysis)")
