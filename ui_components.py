import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------
# Financial Overview
# -----------------------------
def render_financial_overview(t):
    st.subheader(t.get("financial_overview_title", "Financial Overview"))

    # Dummy data – replace with your actual financial data
    financial = {
        "revenue": 4.2,
        "profit": 0.65,
        "runway": 14,
        "revenue_delta": "+8%",
        "profit_delta": "+3%",
        "runway_delta": "+2"
    }

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Revenue", f"${financial['revenue']}M", financial["revenue_delta"])
    with col2:
        st.metric("Profit", f"${financial['profit']}M", financial["profit_delta"])
    with col3:
        st.metric("Runway", f"{financial['runway']} months", financial["runway_delta"])

# -----------------------------
# Revenue Trend
# -----------------------------
def render_revenue_trend(t):
    st.subheader(t.get("revenue_trend_title", "Revenue & Profit Trend"))

    # Dummy data – replace with your dataframe
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    revenue = [400, 420, 450, 430, 470, 500]
    profit = [80, 85, 90, 88, 92, 95]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=months, y=revenue, name="Revenue", marker_color="#2F80ED"))
    fig.add_trace(go.Scatter(x=months, y=profit, name="Profit", mode="lines+markers",
                             line=dict(color="#F2994A", width=3), marker=dict(size=7)))
    fig.update_layout(
        height=350,
        hovermode="x unified",
        legend=dict(orientation="h", y=1.02, x=1),
        margin=dict(l=10, r=10, t=30, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Employee Attrition
# -----------------------------
def render_employee_attrition(t):
    st.subheader(t.get("employee_attrition_title", "Employee Attrition Risk"))

    # Dummy data
    labels = ["Staying", "Leaving"]
    sizes = [88, 12]

    fig = px.pie(values=sizes, names=labels, color_discrete_sequence=["#27AE60", "#EB5757"], hole=0.4)
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(height=300, margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Sales Insights (Donut Chart)
# -----------------------------
def render_sales_insights(t):
    st.subheader(t.get("sales_insights_title", "Sales & Customer Insights"))

    # Dummy revenue breakdown
    revenue_breakdown = {
        "Product A": 40,
        "Product B": 35,
        "Product C": 25
    }

    fig = px.pie(
        values=list(revenue_breakdown.values()),
        names=list(revenue_breakdown.keys()),
        color_discrete_sequence=["#2F80ED", "#F2994A", "#27AE60"],
        hole=0.45
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(height=320, margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig, use_container_width=True)
