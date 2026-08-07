import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="RetailPulse Dashboard", layout="wide")

st.title("📊 RetailPulse - Retail Analytics Dashboard")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

OUTPUTS_DIR = os.path.join(BASE_DIR, "..", "outputs")


df = pd.read_csv(os.path.join(OUTPUTS_DIR, "final_retail_data.csv"))
segments = pd.read_csv(os.path.join(OUTPUTS_DIR, "customer_segments.csv"))
inventory = pd.read_csv(os.path.join(OUTPUTS_DIR, "inventory_risk.csv"))
forecast = pd.read_csv(os.path.join(OUTPUTS_DIR, "demand_forecast.csv"))

st.sidebar.header("Filters")

country = st.sidebar.multiselect(
    "Country",
    df["Country"].unique(),
    default=df["Country"].unique()
)

df = df[df["Country"].isin(country)]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Revenue", f"₹{df['TotalSales'].sum():,.0f}")
col2.metric("Orders", df["InvoiceNo"].nunique())
col3.metric("Customers", df["CustomerID"].nunique())
col4.metric("Products", df["StockCode"].nunique())

st.subheader("Monthly Revenue")

monthly = df.groupby("MonthName")["TotalSales"].sum().reset_index()

fig = px.bar(monthly,
             x="MonthName",
             y="TotalSales")

st.plotly_chart(fig, use_container_width=True)

st.subheader("Top Products")

top = df.groupby("Description")["TotalSales"].sum().nlargest(10).reset_index()

fig2 = px.bar(top,
              x="TotalSales",
              y="Description",
              orientation="h")

st.plotly_chart(fig2, use_container_width=True)

st.subheader("Inventory Recommendation")

fig3 = px.pie(
    inventory,
    names="Recommendation"
)

st.plotly_chart(fig3, use_container_width=True)