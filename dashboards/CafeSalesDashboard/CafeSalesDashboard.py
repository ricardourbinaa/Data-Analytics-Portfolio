import streamlit as st
import pandas as pd
import plotly.express as px

#loading file
df = pd.read_csv("cleaned_cafe_sales.csv")
df['transaction_date'] = pd.to_datetime(df['transaction_date'])

# Sidebar filters
st.sidebar.title("Filters")

item_filter = st.sidebar.selectbox("Select Item", df["item"].unique())

payment_filter = st.sidebar.multiselect(
    "Payment Method",
    df["payment_method"].unique(),
    default=df["payment_method"].unique()
)

start_date = st.sidebar.date_input("Start Date", df["transaction_date"].min())
end_date = st.sidebar.date_input("End Date", df["transaction_date"].max())

# Apply filters
mask = (
    (df["payment_method"].isin(payment_filter)) &
    (df["transaction_date"].dt.date >= start_date) &
    (df["transaction_date"].dt.date <= end_date)
)

df_filtered = df[mask]

# KPIs
total_revenue = df_filtered["total_spent"].sum()
total_transactions = df_filtered.shape[0]
avg_order_value = df_filtered["total_spent"].mean()

# Charts
fig_items = px.bar(
    df_filtered.groupby('item')['total_spent'].sum().reset_index(),
    x="item",
    y="total_spent",
    title="Revenue by Item"
)

filtered_item = df_filtered[df_filtered['item'] == item_filter]
daily = filtered_item.groupby(filtered_item['transaction_date'].dt.date)['total_spent'].sum().reset_index()

fig_trend = px.line(
    daily,
    x="transaction_date",
    y="total_spent",
    title=f"Daily Revenue Trend for {item_filter}"
)

payment_method = df_filtered.groupby("payment_method")["total_spent"].sum().reset_index()

fig_payment = px.pie(
    payment_method,
    names="payment_method",
    values="total_spent",
    title="Revenue by Payment Method"
)

top_items = (
    df_filtered.groupby("item")["total_spent"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

fig_top5 = px.bar(
    top_items,
    x="item",
    y="total_spent",
    title="Top 5 Items by Revenue",
    text_auto=True
)

#title
st.title("Cafe Sales Dashboard")
st.write("This dashboard provides an overview of sales performance, customer behavior, and revenue trends for the cafe")
st.divider()
#Tabs
tab1, tab2, tab3, tab4 =st.tabs(["Overview", "Items", "Payments", "Trends"])

with tab1:
    st.subheader("Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"{total_revenue:,.2f}")
    col2.metric("Total Transactions", total_transactions)
    col3.metric("Avg Order Value", f"${avg_order_value:,.2f}")

with tab2:
    st.subheader("Item Performance")
    st.plotly_chart(fig_items, key="items_chart")
    st.write("Filtered Item", item_filter)
    st.plotly_chart(fig_top5, key="top5_chart")

with tab3:
    st.subheader("Payment Methods")
    st.plotly_chart(fig_payment, key="payment_chart")

with tab4:
    st.subheader("Revenue Trend")
    st.plotly_chart(fig_trend, key="trend_chart")




#side KPIs
st.sidebar.subheader("Summary")
st.sidebar.metric("Total Transactions", df_filtered.shape[0])
st.sidebar.metric("Avg Order Value", f"${df_filtered['total_spent'].mean():.2f}")