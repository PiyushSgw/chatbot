import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd
import plotly.express as px  # for charts

from data import (
    get_financial_data,
    get_revenue_trend_data,
    get_employee_data,
    get_ceo_summary,
)
from lang import LANGUAGES, get_text

# =========================
# ENV & OPENAI SETUP
# =========================
load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    st.error("❌ OpenAI API key not found. Please check your .env file.")
    st.stop()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="CEO Analytic Dashboard", layout="wide")

# =========================
# LANGUAGE TOGGLE (ONE GLOBAL OPTION)
# =========================
if "lang" not in st.session_state:
    st.session_state.lang = "English"

lang = st.radio(
    "Select Language / اختر اللغة",
    options=LANGUAGES,
    index=0 if st.session_state.lang=="English" else 1,
    horizontal=True
)

st.session_state.lang = lang
txt = get_text(lang)

# =========================
# LOAD DATA
# =========================
finance = get_financial_data()
trend = get_revenue_trend_data()
employee = get_employee_data()

# =========================
# HEADER
# =========================
st.title(txt["dashboard_title"])
st.caption(txt["dashboard_caption"])

# =========================
# FINANCIAL OVERVIEW
# =========================
st.subheader(txt["financial_overview"])
c1, c2, c3, c4 = st.columns(4)
c1.metric(f"{txt['revenue_label']} (M QAR)", finance["revenue"])
c2.metric("Profit Margin %", finance["profit_margin"])
c3.metric(f"{txt['expenses_label']} (M QAR)", finance["expenses"])
c4.metric("Profit (M QAR)", finance["profit"])

# Bar chart: Revenue vs Expenses
fig_finance = px.bar(
    x=[txt["revenue_label"], txt["expenses_label"]],
    y=[finance["revenue"], finance["expenses"]],
    text=[
        f"{finance['revenue']}M" if lang=="English" else f"{finance['revenue']} مليون",
        f"{finance['expenses']}M" if lang=="English" else f"{finance['expenses']} مليون"
    ],
    color=[txt["revenue_label"], txt["expenses_label"]],
    color_discrete_sequence=px.colors.sequential.Teal,
    title=txt["revenue_vs_expenses"]
)
fig_finance.update_traces(textposition='outside')
fig_finance.update_layout(
    yaxis_title=txt["yaxis_millions"],
    xaxis_title="",
    title_x=0.5,
    showlegend=False
)
st.plotly_chart(fig_finance, use_container_width=True)

# =========================
# REVENUE TREND
# =========================
st.subheader(txt["revenue_trend"])
st.line_chart(trend.set_index("Month"))

# =========================
# EMPLOYEE OVERVIEW
# =========================
st.subheader(txt["workforce_overview"])
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Employees", employee["total_employees"])
c2.metric("Active Employees", employee["active_employees"])
c3.metric("Attrition Rate %", employee["attrition_rate"])
c4.metric("Engagement Score", employee["engagement_score"])
c5.metric("Avg Tenure", employee["avg_tenure"])

inactive_employees = employee["total_employees"] - employee["active_employees"]
fig_employee = px.pie(
    names=["Active", "Inactive"] if lang=="English" else ["نشط", "غير نشط"],
    values=[employee["active_employees"], inactive_employees],
    hole=0.5,
    title=txt["active_inactive"]
)
st.plotly_chart(fig_employee, use_container_width=True)

# =========================
# CEO INSIGHT
# =========================
st.subheader(txt["ceo_insight"])
st.info(get_ceo_summary())

# =========================
# AI EXECUTIVE ASSISTANT
# =========================
def ai_analyze(messages):
    system_prompt = f"""
    You are a CEO Executive Assistant.

    Analyze company data and provide:
    - Clear insights
    - Risks & alerts
    - Actionable recommendations

    Respond in {lang}.

    Financial Data: {finance}
    Employee Data: {employee}
    Revenue Trend: {trend.to_dict()}
    """
    chat = [{"role": "system", "content": system_prompt}] + messages
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=chat,
        temperature=0.4,
        max_tokens=600,
    )
    return response.choices[0].message.content

# =========================
# SIDEBAR – AI CHAT
# =========================
st.sidebar.title(txt["ai_sidebar_title"])
st.sidebar.caption(txt["ai_sidebar_caption"])

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.sidebar.markdown("### Quick Questions")
for q in txt["quick_questions"]:
    if st.sidebar.button(q, key=f"quick_{q}"):
        st.session_state.chat_history.append({"role": "user", "content": q})
        try:
            reply = ai_analyze(st.session_state.chat_history)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.session_state.chat_history.append({"role": "assistant", "content": f"AI Error: {e}"})

# Clear Chat
if st.sidebar.button(txt["clear_chat"], key="clear_chat"):
    st.session_state.chat_history = []

st.sidebar.markdown("---")
if st.session_state.chat_history:
    for msg in st.session_state.chat_history:
        role = "user" if msg["role"]=="user" else "assistant"
        with st.sidebar.chat_message(role):
            st.markdown(msg["content"])

# Chat input
user_input = st.sidebar.chat_input(txt["chat_input"])
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.sidebar.chat_message("assistant"):
        with st.spinner(txt["analyzing"]):
            try:
                reply = ai_analyze(st.session_state.chat_history)
                st.markdown(reply)
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"AI Error: {e}")

# =========================
# FOOTER
# =========================
st.caption(txt["footer"])
