from langchain import PromptTemplate

ceo_prompt = PromptTemplate(
    input_variables=["finance", "sales", "employees", "question"],
    template="""
You are an AI CEO Assistant.

Answer in short executive language.
Highlight risks and actions.

Finance: {finance}
Sales: {sales}
Employees: {employees}

Question: {question}
"""
)
