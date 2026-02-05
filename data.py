import pandas as pd
import random

# =========================
# Financial Overview
# =========================
def get_financial_data():
    return {
        "revenue": round(random.uniform(2.2, 3.2), 2),      # million QAR
        "profit_margin": random.randint(18, 28),
        "expenses": round(random.uniform(1.7, 2.2), 2),
        "profit": round(random.uniform(0.4, 0.9), 2),
    }


# =========================
# Revenue Trend
# =========================
def get_revenue_trend_data():
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"]
    revenue = [random.randint(10000, 30000) for _ in months]
    profit = [r - random.randint(2000, 6000) for r in revenue]

    return pd.DataFrame({
        "Month": months,
        "Revenue": revenue,
        "Profit": profit,
    })


# =========================
# Employee Data
# =========================
def get_employee_data():
    return {
        "total_employees": 240,
        "active_employees": 228,
        "attrition_rate": 6.2,
        "engagement_score": 78,
        "avg_tenure": 4.3,
        "new_hires_ytd": 22,
        "exits_ytd": 14,
        "payroll_monthly": 3_450_000,

        "department_wise_count": {
            "Sales": 70,
            "Operations": 60,
            "HR": 20,
            "Finance": 25,
            "IT": 65,
        },

        "high_risk_employees": [
            {"name": "Sarah J.", "department": "Sales", "risk": 85, "reason": "Salary below market"},
            {"name": "Mike R.", "department": "Operations", "risk": 78, "reason": "High workload"},
            {"name": "Ahmed K.", "department": "IT", "risk": 73, "reason": "Low engagement score"},
            {"name": "Priya S.", "department": "HR", "risk": 72, "reason": "Limited career growth"},
            {"name": "John M.", "department": "Finance", "risk": 70, "reason": "Role stagnation"},
            {"name": "Fatima A.", "department": "Sales", "risk": 82, "reason": "Commission targets unrealistic"},
            {"name": "Ravi P.", "department": "IT", "risk": 76, "reason": "Long overtime hours"},
            {"name": "Omar H.", "department": "Operations", "risk": 74, "reason": "Shift burnout"},
            {"name": "Lina Z.", "department": "HR", "risk": 71, "reason": "Manager feedback issues"},
            {"name": "Daniel C.", "department": "Finance", "risk": 69, "reason": "Low performance incentives"},
            {"name": "Sanjay N.", "department": "IT", "risk": 80, "reason": "Market demand for skills"},
            {"name": "Ayesha R.", "department": "Sales", "risk": 77, "reason": "High client pressure"},
            {"name": "Khalid B.", "department": "Operations", "risk": 75, "reason": "Process inefficiencies"},
            {"name": "Neha T.", "department": "HR", "risk": 68, "reason": "Work-life balance"},
            {"name": "Victor L.", "department": "Finance", "risk": 66, "reason": "Limited promotion cycle"},
            {"name": "Mohammed S.", "department": "IT", "risk": 79, "reason": "Better external offers"},
            {"name": "Anita D.", "department": "Sales", "risk": 83, "reason": "Territory imbalance"},
            {"name": "Yusuf E.", "department": "Operations", "risk": 72, "reason": "Physical fatigue"},
        ],
    }


# =========================
# CEO Summary
# =========================
def get_ceo_summary():
    return (
        "Business performance is stable. Revenue trend is positive, "
        "but employee engagement and payroll efficiency need monitoring. "
        "Recommended focus on retention and cost control."
    )
