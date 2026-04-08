import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Ethnic Wear Dashboard", layout="wide")

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
.kpi-card {
    background: linear-gradient(135deg, #1f2937, #111827);
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    text-align: left;
    border: 1px solid rgba(255,255,255,0.05);
}

.kpi-title {
    font-size: 13px;
    color: #9CA3AF;
}

.kpi-value {
    font-size: 28px;
    font-weight: 600;
    color: white;
}
</style>
""", unsafe_allow_html=True)
# -------------------- LOAD DATA --------------------
df = pd.read_csv("data/cleaned_business.csv")

# -------------------- CLEANING --------------------
df["City"] = df["City"].str.lower().replace({
    "bengaluru": "Bangalore",
    "bangalore": "Bangalore",
    "hyd": "Hyderabad",
    "hyderabad": "Hyderabad"
})

df["Profit Flag"] = df["Profit"].apply(lambda x: "Loss" if x < 0 else "Profit")
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

# -------------------- SIDEBAR --------------------
st.sidebar.title("🔍 Filters")

category = st.sidebar.multiselect("Category", df["Product_Category"].unique())
city = st.sidebar.multiselect("City", df["City"].unique())
segment = st.sidebar.multiselect("Segment", df["Segment"].unique())

filtered_df = df.copy()

if category:
    filtered_df = filtered_df[filtered_df["Product_Category"].isin(category)]
if city:
    filtered_df = filtered_df[filtered_df["City"].isin(city)]
if segment:
    filtered_df = filtered_df[filtered_df["Segment"].isin(segment)]

# -------------------- KPIs --------------------
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order_ID"].count()
units_sold = filtered_df["Units_Sold"].sum()
avg_profit = total_profit / total_orders if total_orders != 0 else 0
loss_orders = filtered_df[filtered_df["Profit"] < 0].shape[0]

# -------------------- HEADER --------------------
st.markdown("## 🧵 Ethnic Wear Sales Dashboard")

# -------------------- KPI ROW --------------------
k1, k2, k3, k4, k5 = st.columns(5)

def kpi(title, value):
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

with k1:
    kpi("Total Profit", f"₹{total_profit:,.0f}")
with k2:
    kpi("Total Orders", total_orders)
with k3:
    kpi("Units Sold", units_sold)
with k4:
    kpi("Avg Profit/Order", f"₹{avg_profit:,.0f}")
with k5:
    kpi("Loss Orders", loss_orders)

st.markdown("---")

# -------------------- TABS (LIKE POWER BI PAGES) --------------------
tab1, tab2, tab3 = st.tabs(["📊 Overview", "📦 Products", "🌍 Geography"])

# ==================== TAB 1 ====================
with tab1:
    col1, col2 = st.columns(2)

    monthly = filtered_df.groupby(filtered_df["Order_Date"].dt.to_period("M"))["Profit"].sum().reset_index()
    monthly["Order_Date"] = monthly["Order_Date"].astype(str)

    fig1 = px.line(monthly, x="Order_Date", y="Profit", title="Monthly Profit Trend",
                   template="simple_white")
    col1.plotly_chart(fig1, use_container_width=True)

    fig2 = px.pie(filtered_df, names="Profit Flag", title="Profit vs Loss",
                  color="Profit Flag",
                  color_discrete_map={"Profit": "green", "Loss": "red"})
    col2.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    fig3 = px.bar(filtered_df, x="Segment", y="Profit", title="Profit by Segment",
                  template="simple_white")
    col3.plotly_chart(fig3, use_container_width=True)

    cat_df = filtered_df.groupby("Product_Category").agg({
        "Order_ID": "count",
        "Units_Sold": "sum"
    }).reset_index()

    fig4 = px.bar(cat_df, x="Product_Category", y=["Order_ID", "Units_Sold"],
                  barmode="group", title="Orders & Units by Category")
    col4.plotly_chart(fig4, use_container_width=True)

# ==================== TAB 2 ====================
with tab2:
    col5, col6 = st.columns(2)

    cat_profit = filtered_df.groupby("Product_Category")["Profit"].sum().reset_index()
    fig5 = px.bar(cat_profit, x="Profit", y="Product_Category", orientation="h",
                  title="Profit by Category")
    col5.plotly_chart(fig5, use_container_width=True)

    top_products = filtered_df.groupby("Product_Name")["Profit"].sum().nlargest(10).reset_index()
    fig6 = px.bar(top_products, x="Profit", y="Product_Name", orientation="h",
                  title="Top 10 Products")
    col6.plotly_chart(fig6, use_container_width=True)

    col7, col8 = st.columns(2)

    fig7 = px.scatter(filtered_df, x="Discount_%", y="Profit",
                      title="Discount vs Profit",
                      hover_data=["Product_Name"])
    col7.plotly_chart(fig7, use_container_width=True)

    pivot = filtered_df.pivot_table(index="Product_Category",
                                    values=["Profit", "Discount_%", "Order_ID"],
                                    aggfunc={"Profit": "sum",
                                             "Discount_%": "mean",
                                             "Order_ID": "count"})
    col8.dataframe(pivot, use_container_width=True)

# ==================== TAB 3 ====================
with tab3:
    col9, col10 = st.columns(2)

    city_profit = filtered_df.groupby("City")["Profit"].sum().reset_index()
    fig8 = px.bar(city_profit, x="City", y="Profit", title="Profit by City")
    col9.plotly_chart(fig8, use_container_width=True)

    city_segment = filtered_df.groupby(["City", "Segment"])["Order_ID"].count().reset_index()
    fig9 = px.bar(city_segment, x="City", y="Order_ID", color="Segment",
                  title="Orders by City & Segment")
    col10.plotly_chart(fig9, use_container_width=True)

# -------------------- INSIGHTS --------------------
st.markdown("---")
st.markdown("### 💡 Key Insights")

st.info(f"""
• ₹{total_profit:,.0f} total profit generated  
• {loss_orders} orders are loss-making  
• Top category: {cat_profit.sort_values(by='Profit', ascending=False).iloc[0]['Product_Category']}  
• Best city: {city_profit.sort_values(by='Profit', ascending=False).iloc[0]['City']}  
""")
