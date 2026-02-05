# lang.py

LANGUAGES = ["English", "Arabic"]

TEXTS = {
    "English": {
        "dashboard_title": " CEO Analytic Dashboard",
        "dashboard_caption": "Comprehensive CEO-level business overview",
        "financial_overview": " Financial Overview",
        "revenue_vs_expenses": "Revenue vs Expenses",
        "yaxis_millions": "Millions",
        "revenue_label": "Revenue",
        "expenses_label": "Expenses",
        "revenue_trend": "📈 Revenue & Profit Trend",
        "workforce_overview": " Workforce Overview",
        "active_inactive": "Active vs Inactive Employees",
        "ceo_insight": "🧠 CEO Insight",
        "ai_sidebar_title": "🤖 CEO AI Assistant",
        "ai_sidebar_caption": "Ask natural language questions",
        "quick_questions": [
            "CEO 60-second overview",
            "Who might leave next month?",
            "Financial health",
            "Growth opportunities"
        ],
        "clear_chat": " Clear Chat",
        "chat_input": "Ask a business question...",
        "analyzing": "AI analyzing...",
        "footer": " Confidential | For Executive Use Only"
    },
    "Arabic": {
        "dashboard_title": " لوحة تحليلات المدير التنفيذي",
        "dashboard_caption": "نظرة شاملة على أداء الشركة على مستوى المدير التنفيذي",
        "financial_overview": " النظرة المالية",
        "revenue_vs_expenses": "الإيرادات مقابل المصاريف",
        "yaxis_millions": "بالملايين",
        "revenue_label": "الإيرادات",
        "expenses_label": "المصاريف",
        "revenue_trend": "📈 اتجاه الإيرادات والأرباح",
        "workforce_overview": " نظرة عامة على الموظفين",
        "active_inactive": "الموظفون النشطون مقابل غير النشطين",
        "ceo_insight": " ملخص تنفيذي",
        "ai_sidebar_title": "🤖 مساعد المدير التنفيذي",
        "ai_sidebar_caption": "اسأل أسئلة بلغة طبيعية",
        "quick_questions": [
            "نظرة عامة خلال 60 ثانية",
            "من قد يغادر الشهر القادم؟",
            "الصحة المالية",
            "فرص النمو"
        ],
        "clear_chat": " مسح الدردشة",
        "chat_input": "اكتب سؤالك هنا...",
        "analyzing": "جاري التحليل...",
        "footer": " سري | للاستخدام التنفيذي فقط"
    }
}

def get_text(lang: str):
    """
    Returns the dictionary of texts for the selected language.
    Defaults to English if language not found.
    """
    return TEXTS.get(lang, TEXTS["English"])
