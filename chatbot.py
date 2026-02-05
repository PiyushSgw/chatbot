import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain_core.prompts import PromptTemplate

# Load env
load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file")

# OpenAI client
client = OpenAI(api_key=OPENAI_KEY)

# ---- Mock company data (aligns with RUD) ----
financial = {
    "revenue": 1200000,
    "expenses": 850000,
    "profit": 350000,
}

sales = {
    "monthly_sales": [120, 150, 180, 210],
    "growth_rate": "12%",
    "customer_satisfaction_change": "+18%",  # from example
}

employees = {
    "total_employees": 85,
    "attrition_rate": "4%",
    "high_risk_example": "Instructor #28 (85% probability of leaving)",
}

# Simple alert derivation
alerts = []
if financial["profit"] < financial["revenue"] * 0.2:
    alerts.append("Profit margin below 20%.")
if int(employees["attrition_rate"].strip("%")) > 5:
    alerts.append("Attrition higher than 5%.")
if sales["monthly_sales"][-1] < sales["monthly_sales"][-2]:
    alerts.append("Latest month sales dropped vs previous month.")

alerts_str = "; ".join(alerts) if alerts else "No critical alerts in current snapshot."

# ---- Prompt template that follows your RUD ----
ceo_prompt = PromptTemplate(
    input_variables=["finance", "sales", "employees", "alerts", "question"],
    template="""
You are a CEO Dashboard Conversational AI for executives.

Product requirements you must follow:
- Give quick, concise summaries of day-to-day operations.
- Surface KPIs and alerts from financial, sales, and HR data.
- Highlight risks and opportunities with recommended actions.
- Support follow-up questions and keep context conceptually.
- Respond in short executive language.

Available mock data:
Finance KPIs:
{finance}

Sales / Operations KPIs:
{sales}

Employees / HR KPIs:
{employees}

Current alerts (pre-computed from data):
{alerts}

When you answer:
- Start with a brief **Overview** (1–3 sentences).
- Then use sections:
  - **Finance**
  - **Sales / Operations**
  - **Employees / HR**
  - **Alerts & Opportunities** (only if something important)
- Under each section, use short bullet points with numbers.
- Always include:
  - 1–2 key KPIs.
  - 1–3 risks or alerts (if any).
  - 1–3 concrete recommended actions.
- Tone: concise, executive, no technical or implementation details.

Example behaviours:
- For "60-second overview", summarise key KPIs, number of alerts, and opportunities.
- For "Who might leave next month?", talk about high-risk employees, reasons, and retention vs replacement cost.
- For "Where are we wasting money?", list top cost leakages with approximate amounts and actions.

CEO question:
{question}
""",
)

def ask_chatbot(question: str) -> str:
    finance_str = (
        f"Revenue: ${financial['revenue']:,}, "
        f"Expenses: ${financial['expenses']:,}, "
        f"Profit: ${financial['profit']:,}"
    )
    sales_str = (
        f"Monthly sales: {sales['monthly_sales']}, "
        f"Growth rate: {sales['growth_rate']}, "
        f"Customer satisfaction change: {sales['customer_satisfaction_change']}"
    )
    employees_str = (
        f"Total employees: {employees['total_employees']}, "
        f"Attrition rate: {employees['attrition_rate']}, "
        f"High-risk example: {employees['high_risk_example']}"
    )

    prompt = ceo_prompt.format(
        finance=finance_str,
        sales=sales_str,
        employees=employees_str,
        alerts=alerts_str,
        question=question,
    )

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",  # or "gpt-4o"
            messages=[
                {"role": "system", "content": "You are a concise executive assistant for a CEO dashboard."},
                {"role": "user", "content": prompt},
            ],
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"Error talking to AI: {e}"

if __name__ == "__main__":
    print(ask_chatbot("CEO, here's your 60-second overview"))
