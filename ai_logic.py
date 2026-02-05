# ai_logic.py
import random
from typing import List, Dict

from data import get_financial_data, get_employee_data, get_sales_data
from llm_client import ask_llm


def _business_intent_answer(question_lower: str) -> str | None:
    """Return business answer if any intent matches, else None."""
    financial = get_financial_data()
    employees = get_employee_data()
    sales = get_sales_data()

    # CEO Overview
    if any(word in question_lower for word in ["overview", "60-second", "summary", "snapshot"]):
        return f"""**Executive Overview**

**Revenue:** QAR {financial['revenue']}M this month

**Attrition Risk:** {employees['attrition_rate']}% ({employees['at_risk']} employees at risk)

**Customer Satisfaction:** {sales['customer_satisfaction']}%

**Key Alert:** High-risk employee retention requires attention.

**Recommended Focus:**
- Review retention strategy for {employees['high_risk_employees'][0]['name']}
- Leverage strong customer satisfaction for upsell and referrals
- Monitor revenue growth sustainability"""

    # Employee attrition questions
    if any(word in question_lower for word in ["leaving", "attrition", "risk", "quit", "turnover"]):
        emp = employees["high_risk_employees"][0]
        return f"""**Employee Attrition Risk**

**Top Risk Profile**
- Role: Instructor #{random.randint(20, 35)}
- Probability of leaving: {emp['risk']}%

**Primary Reason**
- {emp['reason']}

**Financial Impact**
- Retention cost: QAR {emp['retention_cost']:,}
- Replacement cost: QAR {emp['replacement_cost']:,}

**Recommendation**
- A targeted 10% raise is materially cheaper than replacement.

**Other At-Risk Employees**
- {employees['high_risk_employees'][1]['name']} – {employees['high_risk_employees'][1]['risk']}%
- {employees['high_risk_employees'][2]['name']} – {employees['high_risk_employees'][2]['risk']}%"""

    # Financial questions
    if any(word in question_lower for word in ["revenue", "profit", "financial", "money", "income"]):
        return f"""**Financial Performance**

**Current Month**
- Revenue: QAR {financial['revenue']}M
- Profit margin: {financial['profit_margin']}%
- Expenses: QAR {financial['expenses']}M
- Net profit: QAR {financial['profit']}M

**Trend**
- Revenue is up approximately 12% vs last month.
- Profit margins are currently stable.

**Insight**
- Services (50% of total revenue) are the strongest growth driver."""

    # Customer / Sales questions
    if any(word in question_lower for word in ["customer", "sales", "satisfaction", "enrollment"]):
        return f"""**Sales & Customer Insights**

**Volume**
- New enrollments: {sales['new_enrollments']} ({sales['enrollment_growth']} vs previous period)

**Experience**
- Customer satisfaction: {sales['customer_satisfaction']}%

**Revenue Mix**
- Services: 50%
- Product sales: 30%
- Other: 20%

**Recommendation**
- Use high satisfaction as a base for upsell and structured referral programs."""

    # Waste / efficiency questions
    if any(word in question_lower for word in ["waste", "wasting", "efficiency", "cut costs"]):
        total_replacement = sum(emp["replacement_cost"] for emp in employees["high_risk_employees"][:3])
        total_retention = sum(emp["retention_cost"] for emp in employees["high_risk_employees"][:3])
        return f"""**Efficiency & Cost Control**

**1. Talent Replacement Risk**
- Replacement cost exposure: QAR {total_replacement:,}
- Retention investment: QAR {total_retention:,}
- Retention is materially cheaper than turnover.

**2. Capacity Utilization**
- Service utilization at peak hours is around 50%.
- Dynamic pricing and better scheduling could lift revenue by 15–20%.

**3. Acquisition Cost**
- Customer acquisition cost is above industry norms.
- Strengthen referral programs to reduce paid acquisition reliance."""

    # Growth questions
    if any(word in question_lower for word in ["growth", "expand", "scale", "opportunity"]):
        return f"""**Growth Opportunities**

1. Customer Base Expansion
   - Leverage {sales['customer_satisfaction']}% satisfaction with a structured referral and loyalty program.

2. Service Line Development
   - Services already contribute 50% of revenue and are margin-accretive.
   - Consider premium tiers and add-on services.

3. Retention as a Growth Lever
   - Reducing attrition from {employees['attrition_rate']}% to 8% frees budget for growth initiatives."""

    return None


def generate_ai_response(question: str, history: List[Dict[str, str]] | None = None) -> str:
    """
    Try business intents first; if no match, call the LLM with only recent history.
    """
    q_lower = question.lower()

    # 1) Fast rule-based answer (no network)
    business_answer = _business_intent_answer(q_lower)
    if business_answer:
        return business_answer

    # 2) LLM fallback (slower – optimize prompt size)
    messages: List[Dict[str, str]] = [
        {
            "role": "system",
            "content": (
                "You are a helpful AI assistant embedded in a CEO analytics dashboard. "
                "Answer any question clearly. When it makes sense, connect ideas to "
                "business, leadership, or data-driven decision making."
            ),
        }
    ]

    # Keep only the last few turns to keep prompt small (faster & cheaper)
    if history:
        trimmed_history = history[-6:]
        for m in trimmed_history:
            messages.append({"role": m["role"], "content": m["content"]})

    messages.append({"role": "user", "content": question})

    return ask_llm(messages)
